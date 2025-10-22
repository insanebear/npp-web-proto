# ===================================================================
# Local Test Version of Bayesian Simulation (v12 - JSON Output)
# ===================================================================
# This version is for local testing without AWS dependencies
# ===================================================================

# --- 1. Load Required Libraries ---
library("rjags")
library("jsonlite") # For JSON conversion

print("--- LOCAL TEST VERSION (JAGS with JSON Output) ---")

# --- 2. Set Local Test Parameters ---
job_id <- "local-test-job-123"
print(paste("--- Testing with job ID:", job_id, "---"))

# --- 3. Main Simulation Logic (with Error Handling) ---
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
  source("plumber/data.R")
  print("--- Static data loaded. ---")
  
  # --- Read All Inputs from Environment Variables (with defaults for local testing) ---
  print("--- Reading simulation parameters from environment variables... ---")
  fp_input <- getenv_numeric("FP Input", default_val = 50)
  data$SR_FP <- fp_input
  data$SD_FP <- fp_input
  data$IM_FP <- fp_input
  data$ST_FP <- fp_input
  data$IC_FP <- fp_input
  data$SR_SDP_state <- getenv_numeric("Software Development Planning", default_val = 2)
  data$SR_CD_state <- getenv_numeric("Development of Concept", default_val = 2)
  # (Continue to add all your other variables here as per your application's needs)
  print("--- Environment variables read. ---")
  
  # --- Read Simulation Settings (with defaults for local testing) ---
  nChains <- getenv_numeric("nChains", 2)
  nIter <- getenv_numeric("nIter", 1000)  # Reduced for faster local testing
  nBurnin <- getenv_numeric("nBurnin", 500)  # Reduced for faster local testing
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
  model.file <- "plumber/R2WinBUGS_Combined_Model.txt"
  parameters_to_save <- c( 
    "PFD", "SR_Total_Remained_Defect", "SD_Total_Remained_Defect", "IM_Total_Remained_Defect", "ST_Total_Remained_Defect", "IC_Total_Remained_Defect"
    # (Add all other parameters you want to save)
  )
  
  # 로컬 테스트를 위해 더 많은 파라미터 추가
  additional_parameters <- c(
    "SR_DevH_post", "SR_DevM_post", "SR_DevL_post",
    "SD_DevH_post", "SD_DevM_post", "SD_DevL_post", 
    "IM_DevH_post", "IM_DevM_post", "IM_DevL_post",
    "ST_DevH_post", "ST_DevM_post", "ST_DevL_post",
    "IC_DevH_post", "IC_DevM_post", "IC_DevL_post"
  )
  
  # 사용 가능한 파라미터만 추가
  all_parameters <- c(parameters_to_save, additional_parameters)
  
  print("--- Loading JAGS model... ---")
  jags_model <- jags.model(file = model.file, data = data, n.chains = nChains, n.adapt = nBurnin)
  print("--- Updating model... ---")
  update(jags_model, n.iter = nBurnin)
  print("--- Sampling... ---")
  jags_samples <- coda.samples(jags_model, variable.names = all_parameters, n.iter = nIter)
  print("--- Simulation complete. ---")

  # --- 4. Process and Save Results as JSON ---
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
  json_filename <- "local_test_results.json"
  write(json_output, file = json_filename)
  print(paste("--- JSON results saved to", json_filename, "---"))
  
  # --- 5. Display Results Summary ---
  print("--- SIMULATION RESULTS SUMMARY ---")
  print(paste("Job ID:", job_id))
  print(paste("Parameters saved:", length(parameter_names)))
  print("Parameter names:")
  for (param in parameter_names) {
    print(paste("  -", param))
  }
  
  print("--- Local test completed successfully. ---")
  
}, error = function(e) {
  
  # --- This block runs ONLY if an error occurred in the `tryCatch` block ---
  error_message <- paste("Error during simulation:", e$message)
  print(error_message)
  
  # Cause the script to exit with an error code
  quit(status = 1)
})
