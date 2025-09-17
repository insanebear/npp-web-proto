# ===================================================================
# Fargate Job Processor for Bayesian Simulation (v12 - JSON Output)
# ===================================================================
# This version integrates with AWS DynamoDB for status tracking,
# stores simulation results as structured JSON in S3.
# ===================================================================

# --- 1. Load Required Libraries ---
library("rjags")
library("paws")     # AWS SDK for R
library("jsonlite") # For JSON conversion

print("--- SCRIPT VERSION 12 (JAGS with AWS & JSON Output) ---")

# --- 2. Get Job Details & Initialize AWS Clients ---
job_id <- Sys.getenv("JOB_ID")
table_name <- Sys.getenv("JOBS_TABLE_NAME")
s3_bucket_name <- Sys.getenv("S3_BUCKET_NAME")

# Check if essential variables are set
if (job_id == "" || table_name == "" || s3_bucket_name == "") {
  stop("FATAL: Missing essential environment variables (JOB_ID, JOBS_TABLE_NAME, S3_BUCKET_NAME).")
}

# Initialize paws clients. They will automatically use the Fargate Task's IAM Role.
dynamodb <- paws::dynamodb()
s3 <- paws::s3()
print("--- AWS clients initialized. ---")


# --- 3. Update Job Status to "RUNNING" ---
print(paste("--- Updating job", job_id, "to RUNNING... ---"))
dynamodb$update_item(
  TableName = table_name,
  Key = list(jobId = list(S = job_id)),
  UpdateExpression = "SET jobStatus = :s",
  ExpressionAttributeValues = list(":s" = list(S = "RUNNING"))
)

# --- 4. Main Simulation Logic (with Error Handling) ---
# tryCatch ensures that if any part of the simulation fails,
# we can catch the error and update the status to "FAILED".
tryCatch({
  
  # --- Helper Function to Read and Convert Environment Variables ---
  getenv_numeric <- function(var_name, default_val = 2) {
    val <- Sys.getenv(var_name, unset = "")
    if (val == "High") val <- "1"
    if (val == "Medium") val <- "2"
    if (val == "Low") val <- "3"
    if (is.null(val) || val == "") return(default_val)
    return(as.numeric(val))
  }

# Helper function for reading logical (TRUE/FALSE) variables
getenv_logical <- function(var_name, default_val = TRUE) {
  val <- tolower(Sys.getenv(var_name, unset = ""))
  if (val == "") return(default_val)
  return(val == "true")
}
  
  # --- Load Static Data ---
  source("/app/plumber/data.R")
  print("--- Static data loaded. ---")
  
  # --- Read All Inputs from Environment Variables ---
  print("--- Reading simulation parameters from environment variables... ---")
  fp_input <- getenv_numeric("FP Input", default_val = 50)
  data$SR_FP <- fp_input
  data$SD_FP <- fp_input
  data$IM_FP <- fp_input
  data$ST_FP <- fp_input
  data$IC_FP <- fp_input
  data$SR_SDP_state <- getenv_numeric("Software Development Planning")
  data$SR_CD_state <- getenv_numeric("Development of Concept")
  # (Continue to add all your other variables here as per your application's needs)
  print("--- Environment variables read. ---")
  
  # --- Read Simulation Settings ---
  nChains <- getenv_numeric("nChains", 2)
  nIter <- getenv_numeric("nIter", 5000)
  nBurnin <- getenv_numeric("nBurnin", 1000)
  nThin <- getenv_numeric("nThin", 1) 
computeDIC <- getenv_logical("computeDIC", TRUE)
print(paste0(
  "--- Starting JAGS simulation with parameters: ",
  "nChains = ", nChains,
  ", nIter = ", nIter,
  ", nBurnin = ", nBurnin,
  ", nThin = ", nThin,
  ", computeDIC = ", computeDIC,
  " ---"
))

  # --- Run the JAGS Simulation ---
  model.file <- "/app/plumber/R2WinBUGS_Combined_Model.txt"
  parameters_to_save <- c( 
    "PFD", "SR_Total_Remained_Defect", "SD_Total_Remained_Defect", "IM_Total_Remained_Defect", "ST_Total_Remained_Defect", "IC_Total_Remained_Defect"
    # (Add all other parameters you want to save)
  )
  jags_model <- jags.model(file = model.file, data = data, n.chains = nChains, n.adapt = nBurnin)
  update(jags_model, n.iter = nBurnin)
  jags_samples <- coda.samples(jags_model, variable.names = parameters_to_save, n.iter = nIter)
  print("--- Simulation complete. ---")

  # --- 5. Process and Save Results as JSON ---
  print("--- Converting simulation results to JSON... ---")

  # Get summary statistics from the mcmc.list object
  summary_stats <- summary(jags_samples)
  
  # Create a clean, named list to hold the key results for each parameter
  results_list <- list()
  parameter_names <- rownames(summary_stats$statistics)

  for (param in parameter_names) {
    results_list[[param]] <- list(
      mean = summary_stats$statistics[param, "Mean"],
      sd = summary_stats$statistics[param, "SD"],
      median = summary_stats$quantiles[param, "50%"],
      q2_5 = summary_stats$quantiles[param, "2.5%"],
      q97_5 = summary_stats$quantiles[param, "97.5%"]
    )
  }

  # Convert the R list into a nicely formatted JSON string
  json_output <- toJSON(results_list, pretty = TRUE, auto_unbox = TRUE)
  
  # Define the JSON filename and write the file
  json_filename <- "results.json"
  write(json_output, file = json_filename)
  print(paste("--- JSON results saved to", json_filename, "---"))
  
  # --- 6. Upload JSON Results to S3 ---
  s3_object_key <- paste0("results/", job_id, "/", json_filename)
  print(paste("--- Uploading results to s3://", s3_bucket_name, "/", s3_object_key, " ---", sep=""))
  
  s3$put_object(
    Bucket = s3_bucket_name,
    Key = s3_object_key,
    Body = json_filename # Upload the JSON file
  )
  
  # --- 7. Update Job Status to "COMPLETED" ---
  print("--- Upload successful. Updating job status to COMPLETED. ---")
  dynamodb$update_item(
    TableName = table_name,
    Key = list(jobId = list(S = job_id)),
    UpdateExpression = "SET jobStatus = :s, resultsPath = :p",
    ExpressionAttributeValues = list(
      ":s" = list(S = "COMPLETED"),
      ":p" = list(S = s3_object_key)
    )
  )
  
  print("--- Script finished successfully. ---")
  
}, error = function(e) {
  
  # --- This block runs ONLY if an error occurred in the `tryCatch` block ---
  error_message <- paste("Error during simulation:", e$message)
  print(error_message)
  
  # Update job status to FAILED in DynamoDB
  dynamodb$update_item(
    TableName = table_name,
    Key = list(jobId = list(S = job_id)),
    UpdateExpression = "SET jobStatus = :s, errorMessage = :e",
    ExpressionAttributeValues = list(
      ":s" = list(S = "FAILED"),
      ":e" = list(S = error_message)
    )
  )
  
  # Cause the script to exit with an error code
  quit(status = 1)
})