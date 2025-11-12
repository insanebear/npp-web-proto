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
test_mode <- Sys.getenv("TEST_MODE", "false")

# Check if essential variables are set (skip in test mode)
if (test_mode == "true") {
  print("--- RUNNING IN TEST MODE (No AWS) ---")
  job_id <- "test-job-123"
  table_name <- "test-table"
  s3_bucket_name <- "test-bucket"
} else if (job_id == "" || table_name == "" || s3_bucket_name == "") {
  stop("FATAL: Missing essential environment variables (JOB_ID, JOBS_TABLE_NAME, S3_BUCKET_NAME).")
}

# Initialize paws clients only if not in test mode
if (test_mode != "true") {
  dynamodb <- paws::dynamodb()
  s3 <- paws::s3()
  print("--- AWS clients initialized. ---")
} else {
  print("--- Skipping AWS initialization in test mode ---")
}


# --- 3. Update Job Status to "RUNNING" ---
print(paste("--- Updating job", job_id, "to RUNNING... ---"))
if (test_mode != "true") {
  dynamodb$update_item(
    TableName = table_name,
    Key = list(jobId = list(S = job_id)),
    UpdateExpression = "SET jobStatus = :s",
    ExpressionAttributeValues = list(":s" = list(S = "RUNNING"))
  )
} else {
  print("--- Skipping DynamoDB update in test mode ---")
}

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
  includeTraceData <- getenv_logical("includeTraceData", FALSE)
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
  
  # Conditionally add trace parameter based on checkbox
  if (includeTraceData) {
    parameters_to_save <- c( 
      "PFD", "SR_Total_Remained_Defect", "SD_Total_Remained_Defect", "IM_Total_Remained_Defect", "ST_Total_Remained_Defect", "IC_Total_Remained_Defect"
    )
  } else {
    parameters_to_save <- c( 
      "PFD", "SR_Total_Remained_Defect", "SD_Total_Remained_Defect", "IM_Total_Remained_Defect", "ST_Total_Remained_Defect", "IC_Total_Remained_Defect"
    )
  }
  jags_model <- jags.model(file = model.file, data = data, n.chains = nChains, n.adapt = nBurnin)
  update(jags_model, n.iter = nBurnin)
  jags_samples <- coda.samples(jags_model, variable.names = parameters_to_save, n.iter = nIter)
  print("--- Simulation complete. ---")

  # --- 5. Process and Save Results as JSON ---
  print("--- Converting simulation results to JSON... ---")

  # Get summary statistics from the mcmc.list object
  summary_stats <- summary(jags_samples)
  
  # Create a clean, named list to hold the key results for each parameter
  output_list <- list()
  parameter_names <- rownames(summary_stats$statistics)

  for (param in parameter_names) {
    output_list[[param]] <- list(
      mean = summary_stats$statistics[param, "Mean"],
      sd = summary_stats$statistics[param, "SD"],
      median = summary_stats$quantiles[param, "50%"],
      q2_5 = summary_stats$quantiles[param, "2.5%"],
      q97_5 = summary_stats$quantiles[param, "97.5%"]
    )
  }

  # Add trace data if checkbox was checked
  if (includeTraceData) {
    # Add trace data for PFD samples
    pfd_samples <- as.vector(as.matrix(jags_samples)[, "PFD"])
    
    # Store raw MCMC samples for PFD as a numeric array under "traces".
    # This is the exact sample set used to compute the summary statistics above
    # (mean, sd, quantiles). It is included only when includeTraceData == TRUE
    # to support downstream visualization and debugging.
    output_list[["traces"]] <- pfd_samples
    
    print("--- Trace data added to results ---")
  }
  
  # --- Build Complete JSON with Input and Output ---
  print("--- Building complete JSON with input and output... ---")
  
  # Helper function to convert label to code key (matching labelToCode.ts)
  label_to_code <- list(
    FP = list("FP Input" = "FP_Input"),
    "Requirement Dev" = list(
      "Software Development Planning" = "SR_SDP_state",
      "Development of Concept" = "SR_CD_state",
      "Development of SRS" = "SR_SRS_state",
      "Traceability Analysis" = "SR_TA_state",
      "Criticality Analysis" = "SR_CA_state",
      "Hazard Analysis" = "SR_HA_state",
      "Security Analysis" = "SR_SA_state",
      "Risk Analysis" = "SR_RA_state",
      "System Software Qualification" = "SR_SQTPG_state",
      "System Software Acceptance" = "SR_SATPG_state",
      "Configuration Management" = "SR_CM_state",
      "Review and Audit" = "SR_RaA_state"
    ),
    "Requirement V&V" = list(
      "Software Planning" = "SR_SVVP_state",
      "Concept Documentation Evaluation" = "SR_CDE_state",
      "Software User Requirement Allocation Analysis" = "SR_HRAA_state",
      "Software Requirement Evaluation" = "SR_SRE_state",
      "Interface Analysis" = "SR_IAVV_state",
      "Traceability Analysis" = "SR_TAVV_state",
      "Criticality Analysis" = "SR_CAVV_state",
      "Hazard Analysis" = "SR_HAVV_state",
      "Security Analysis" = "SR_SAVV_state",
      "Risk Analysis" = "SR_RAVV_state",
      "System Software Qualification" = "SR_VVSQTPG_state",
      "System Software Acceptance" = "SR_VVSATPG_state",
      "Configuration Management" = "SR_CMA_state",
      "Review and Audit" = "SR_RaAVV_state",
      "Activity Summary Report" = "SR_VVASRG_state"
    ),
    "Design Dev" = list(
      "Development Software Architecture" = "SD_SAD_state",
      "Development Software Design" = "SD_SDD_state",
      "Traceability Analysis" = "SD_TA_state",
      "Criticality Analysis" = "SD_CA_state",
      "Hazard Analysis" = "SD_HA_state",
      "Security Analysis" = "SD_SA_state",
      "Risk Analysis" = "SD_RA_state",
      "Software Component Test Plan" = "SD_SCTPG_state",
      "Software Integration Test Plan" = "SD_SITPG_state",
      "Software Component Test Design" = "SD_SCTDG_state",
      "Software Integration Test Design" = "SD_SITDG_state",
      "System Software Qualification" = "SD_SQTDG_state",
      "System Software Acceptance" = "SD_SATDG_state",
      "Configuration Management" = "SD_CM_state",
      "Review and Audit" = "SD_RaA_state"
    ),
    "Design V&V" = list(
      "Design Evaluation" = "SD_DE_state",
      "Interface Analysis" = "SD_IAVV_state",
      "Traceability Analysis" = "SD_TAVV_state",
      "Criticality Analysis" = "SD_CAVV_state",
      "Hazard Analysis" = "SD_HAVV_state",
      "Security Analysis" = "SD_SAVV_state",
      "Risk Analysis" = "SD_RAVV_state",
      "Software Component Test Plan" = "SD_VVSCTPG_state",
      "Software Integration Test Plan" = "SD_VVSITPG_state",
      "Software Component Test Design" = "SD_VVSCTDG_state",
      "Software Integration Test Design" = "SD_VVSITDG_state",
      "System Software Qualification" = "SD_VVSQTDG_state",
      "System Software Acceptance" = "SD_VVSATDG_state",
      "Configuration Management" = "SD_CMVV_state",
      "Review and Audit" = "SD_RaAVV_state",
      "Activity Summary Report" = "SD_VVASRG_state"
    ),
    "Implementation Dev" = list(
      "Source Code Document" = "IM_SCaSCDG_state",
      "Traceability Analysis" = "IM_TA_state",
      "Criticality Analysis" = "IM_CA_state",
      "Hazard Analysis" = "IM_HA_state",
      "Security Analysis" = "IM_SA_state",
      "Risk Analysis" = "IM_RA_state",
      "Software Component Test Case" = "IM_CTCG_state",
      "Software Integration Test Case" = "IM_SITCG_state",
      "Software Qualification Test Case" = "IM_SQTCG_state",
      "Software Acceptance Test Case" = "IM_SATCG_state",
      "Software Component Test Procedure" = "IM_SCTPG_state",
      "Software Integration Test Procedure" = "IM_SITPG_state",
      "System Software Qualification" = "IM_SQTPG_state",
      "System Software Component Test Execution" = "IM_SCTE_state",
      "Configuration Management" = "IM_CM_state",
      "Review and Audit" = "IM_RaA_state"
    ),
    "Implementation V&V" = list(
      "Source Code Document" = "IM_SCaSCDE_state",
      "Interface Analysis" = "IM_IAVV_state",
      "Traceability Analysis" = "IM_TAVV_state",
      "Criticality Analysis" = "IM_CAVV_state",
      "Hazard Analysis" = "IM_HAVV_state",
      "Security Analysis" = "IM_SAVV_state",
      "Risk Analysis" = "IM_RAVV_state",
      "Software Component Test Case" = "IM_VVSCTCG_state",
      "Software Integration Test Case" = "IM_VVSITCG_state",
      "Software Qualification Test Case" = "IM_VVSQTCG_state",
      "Software Acceptance Test Case" = "IM_VVSATCG_state",
      "Software Component Test Procedure" = "IM_VVSCTPG_state",
      "Software Integration Test Procedure" = "IM_VVSITPG_state",
      "System Software Qualification Test Procedure" = "IM_VVSQTPG_state",
      "System Software Component Test Execution" = "IM_VVSCTE_state",
      "Configuration Management" = "IM_CMVV_state",
      "Review and Audit" = "IM_RaAVV_state",
      "Activity Summary Report" = "IM_VVASRG_state"
    ),
    "Test Dev" = list(
      "Traceability Analysis" = "ST_TA_state",
      "Hazard Analysis" = "ST_HA_state",
      "Security Analysis" = "ST_SA_state",
      "Risk Analysis" = "ST_RA_state",
      "System Software Acceptance Test Execution" = "ST_SATE_state",
      "System Software Acceptance Procedure Generation" = "ST_SAPG_state",
      "System Software Integration Test Execution" = "ST_SITE_state",
      "System Software Qualification Test Execution" = "ST_SQTE_state",
      "Configuration Management" = "ST_CM_state",
      "Review and Audit" = "ST_RaA_state"
    ),
    "Test V&V" = list(
      "Traceability Analysis" = "ST_TAVV_state",
      "Hazard Analysis" = "ST_HAVV_state",
      "Security Analysis" = "ST_SAVV_state",
      "Risk Analysis" = "ST_RAVV_state",
      "System Software Acceptance Test Execution" = "ST_VVSATE_state",
      "System Software Acceptance Procedure Generation" = "ST_VVSAPG_state",
      "System Software Integration Test Execution" = "ST_VVSITE_state",
      "System Software Qualification Test Execution" = "ST_VVSQTE_state",
      "Configuration Management" = "ST_CMVV_state",
      "Review and Audit" = "ST_RaAVV_state",
      "Activity Summary Report" = "ST_VVASRG_state",
      "Acitivity Summary Report" = "ST_VVASRG_state"  # Support typo in desired JSON format
    ),
    "Installation and Checkout Dev" = list(
      "Installation Procedure Generation" = "IC_IPG_state",
      "Installation and Checkout" = "IC_IaC_state",
      "Hazard Analysis" = "IC_HA_state",
      "Security Analysis" = "IC_SA_state",
      "Risk Analysis" = "IC_RA_state"
    ),
    "Installation and Checkout V&V" = list(
      "Installation Procedure Generation" = "IC_ICAVV_state",
      "Installation and Checkout" = "IC_ICVV_state",
      "Hazard Analysis" = "IC_HAVV_state",
      "Security Analysis" = "IC_SAVV_state",
      "Risk Analysis" = "IC_RAVV_state",
      "Activity Summary Report" = "IC_VVASRG_state",
      "Final Report Generation" = "IC_VVFRG_state"
    )
  )
  
  # Function to get code key from label
  get_code_key <- function(tab_label, field_label) {
    tab_map <- label_to_code[[tab_label]]
    if (is.null(tab_map)) return(NULL)
    code <- tab_map[[field_label]]
    if (is.null(code)) return(NULL)
    return(code)
  }
  
  # Function to find tab label for a given field label (UI label)
  find_tab_for_label <- function(field_label) {
    for (tab_name in names(label_to_code)) {
      tab_map <- label_to_code[[tab_name]]
      if (field_label %in% names(tab_map)) {
        return(tab_name)
      }
    }
    return(NULL)
  }
  
  # Function to find tab label for a code key (e.g., "SR_SDP_state")
  # Lambda sends code keys directly, not UI labels
  find_tab_for_code_key <- function(code_key) {
    for (tab_name in names(label_to_code)) {
      tab_map <- label_to_code[[tab_name]]
      # Check if code_key is in the values of the map
      if (code_key %in% unlist(tab_map, use.names = FALSE)) {
        return(tab_name)
      }
    }
    return(NULL)
  }
  
  # Function to get code key from UI label (for reverse lookup)
  get_code_key_from_label <- function(tab_label, field_label) {
    tab_map <- label_to_code[[tab_label]]
    if (is.null(tab_map)) return(NULL)
    code <- tab_map[[field_label]]
    return(code)
  }
  
  # Build input structure from environment variables
  input_list <- list()
  
  # Get all environment variables (excluding system ones)
  all_env_vars <- Sys.getenv()
  system_vars <- c("JOB_ID", "JOBS_TABLE_NAME", "S3_BUCKET_NAME", "TEST_MODE", "PATH", "HOME", "USER", "LANG", "PWD", "SHLVL", "_")
  
  # Process FP Input
  # Lambda may send "FP Input" (UI label) or "FP_Input" (code key)
  fp_val <- Sys.getenv("FP Input", unset = "")
  if (fp_val == "") {
    fp_val <- Sys.getenv("FP_Input", unset = "")
  }
  if (fp_val != "") {
    if (is.null(input_list[["FP"]])) {
      input_list[["FP"]] <- list()
    }
    input_list[["FP"]][["FP_Input"]] <- fp_val
  }
  
  # Process settings
  settings_list <- list()
  settings_list[["nChains"]] <- as.character(nChains)
  settings_list[["nIter"]] <- as.character(nIter)
  settings_list[["nBurnin"]] <- as.character(nBurnin)
  settings_list[["nThin"]] <- as.character(nThin)
  settings_list[["computeDIC"]] <- as.character(computeDIC)
  working_dir <- Sys.getenv("workingDir", unset = "/app/results")
  if (working_dir != "") {
    settings_list[["workingDir"]] <- working_dir
  }
  settings_list[["includeTraceData"]] <- as.character(includeTraceData)
  input_list[["settings"]] <- settings_list
  
  # Process all other input fields
  print("--- Available environment variables (excluding system vars) ---")
  for (env_name in names(all_env_vars)) {
    if (!env_name %in% system_vars && env_name != "FP Input" && 
        !env_name %in% c("nChains", "nIter", "nBurnin", "nThin", "computeDIC", "workingDir", "includeTraceData")) {
      print(paste("  Found env var:", env_name, "=", Sys.getenv(env_name, unset = "")))
    }
  }
  
  for (env_name in names(all_env_vars)) {
    # Skip system variables and already processed ones
    if (env_name %in% system_vars || env_name == "FP Input" || 
        env_name %in% c("nChains", "nIter", "nBurnin", "nThin", "computeDIC", "workingDir", "includeTraceData")) {
      next
    }
    
    env_val <- Sys.getenv(env_name, unset = "")
    if (env_val == "") {
      next
    }
    
    # Lambda sends code keys directly (e.g., "SR_SDP_state"), not UI labels
    tab_label <- find_tab_for_code_key(env_name)
    code_key <- env_name
    
    # If not found by code key, try to find by UI label (for backward compatibility)
    if (is.null(tab_label)) {
      tab_label <- find_tab_for_label(env_name)
      if (!is.null(tab_label)) {
        code_key <- get_code_key(tab_label, env_name)
      }
    }
    
    # If still not found, check if it's FP_Input (special case)
    if (is.null(tab_label) && env_name == "FP_Input") {
      tab_label <- "FP"
      code_key <- "FP_Input"
    }
    
    if (is.null(tab_label)) {
      print(paste("  WARNING: No tab found for env var:", env_name))
      next
    }
    
    # Initialize tab if needed
    if (is.null(input_list[[tab_label]])) {
      input_list[[tab_label]] <- list()
    }
    
    # Special handling for "Test V&V" - "Acitivity Summary Report" typo
    if (tab_label == "Test V&V" && code_key == "ST_VVASRG_state") {
      code_key <- "Acitivity Summary Report"
    }
    
    # Store the value with code key
    input_list[[tab_label]][[code_key]] <- env_val
    print(paste("  Mapped:", env_name, "->", tab_label, "/", code_key, "=", env_val))
  }
  
  print(paste("--- Input structure built. Tabs found:", paste(names(input_list), collapse = ", "), "---"))
  
  # Reorder input_list to match desired JSON format order
  desired_tab_order <- c(
    "FP",
    "Requirement Dev",
    "Requirement V&V",
    "Design Dev",
    "Design V&V",
    "Implementation Dev",
    "Implementation V&V",
    "Test Dev",
    "Test V&V",
    "Installation and Checkout Dev",
    "Installation and Checkout V&V"
  )
  
  # Define field order for each tab (matching desired JSON format)
  tab_field_order <- list(
    "FP" = c("FP_Input"),
    "Requirement Dev" = c("SR_SDP_state", "SR_CD_state", "SR_SRS_state", "SR_TA_state", "SR_CA_state", "SR_HA_state", "SR_SA_state", "SR_RA_state", "SR_SQTPG_state", "SR_SATPG_state", "SR_CM_state", "SR_RaA_state"),
    "Requirement V&V" = c("SR_SVVP_state", "SR_CDE_state", "SR_HRAA_state", "SR_SRE_state", "SR_IAVV_state", "SR_TAVV_state", "SR_CAVV_state", "SR_HAVV_state", "SR_SAVV_state", "SR_RAVV_state", "SR_VVSQTPG_state", "SR_VVSATPG_state", "SR_CMA_state", "SR_RaAVV_state", "SR_VVASRG_state"),
    "Design Dev" = c("SD_SAD_state", "SD_SDD_state", "SD_TA_state", "SD_CA_state", "SD_HA_state", "SD_SA_state", "SD_RA_state", "SD_SCTPG_state", "SD_SITPG_state", "SD_SCTDG_state", "SD_SITDG_state", "SD_SQTDG_state", "SD_SATDG_state", "SD_CM_state", "SD_RaA_state"),
    "Design V&V" = c("SD_DE_state", "SD_IAVV_state", "SD_TAVV_state", "SD_CAVV_state", "SD_HAVV_state", "SD_SAVV_state", "SD_RAVV_state", "SD_VVSCTPG_state", "SD_VVSITPG_state", "SD_VVSCTDG_state", "SD_VVSITDG_state", "SD_VVSQTDG_state", "SD_VVSATDG_state", "SD_CMVV_state", "SD_RaAVV_state", "SD_VVASRG_state"),
    "Implementation Dev" = c("IM_SCaSCDG_state", "IM_TA_state", "IM_CA_state", "IM_HA_state", "IM_SA_state", "IM_RA_state", "IM_CTCG_state", "IM_SITCG_state", "IM_SATCG_state", "IM_SCTPG_state", "IM_SITPG_state", "IM_SQTPG_state", "IM_SCTE_state", "IM_CM_state", "IM_RaA_state"),
    "Implementation V&V" = c("IM_SCaSCDE_state", "IM_IAVV_state", "IM_TAVV_state", "IM_CAVV_state", "IM_HAVV_state", "IM_SAVV_state", "IM_RAVV_state", "IM_VVSCTCG_state", "IM_VVSITCG_state", "IM_VVSQTCG_state", "IM_VVSATCG_state", "IM_VVSCTPG_state", "IM_VVSITPG_state", "IM_VVSQTPG_state", "IM_VVSCTE_state", "IM_CMVV_state", "IM_RaAVV_state", "IM_VVASRG_state"),
    "Test Dev" = c("ST_TA_state", "ST_HA_state", "ST_SA_state", "ST_RA_state", "ST_SATE_state", "ST_SAPG_state", "ST_SITE_state", "ST_SQTE_state", "ST_CM_state", "ST_RaA_state"),
    "Test V&V" = c("ST_TAVV_state", "ST_HAVV_state", "ST_SAVV_state", "ST_RAVV_state", "ST_VVSATE_state", "ST_VVSAPG_state", "ST_VVSITE_state", "ST_VVSQTE_state", "ST_CMVV_state", "ST_RaAVV_state", "Acitivity Summary Report"),
    "Installation and Checkout Dev" = c("IC_IPG_state", "IC_IaC_state", "IC_HA_state", "IC_SA_state", "IC_RA_state"),
    "Installation and Checkout V&V" = c("IC_ICAVV_state", "IC_ICVV_state", "IC_HAVV_state", "IC_SAVV_state", "IC_RAVV_state", "IC_VVASRG_state", "IC_VVFRG_state")
  )
  
  # Function to reorder fields within a tab
  reorder_tab_fields <- function(tab_name, tab_data) {
    if (tab_name %in% names(tab_field_order)) {
      field_order <- tab_field_order[[tab_name]]
      ordered_tab <- list()
      for (field_name in field_order) {
        if (field_name %in% names(tab_data)) {
          ordered_tab[[field_name]] <- tab_data[[field_name]]
        }
      }
      for (field_name in names(tab_data)) {
        if (!field_name %in% names(ordered_tab)) {
          ordered_tab[[field_name]] <- tab_data[[field_name]]
        }
      }
      return(ordered_tab)
    } else {
      return(tab_data)
    }
  }
  
  ordered_input_list <- list()
  for (tab_name in desired_tab_order) {
    if (tab_name %in% names(input_list)) {
      ordered_input_list[[tab_name]] <- reorder_tab_fields(tab_name, input_list[[tab_name]])
    }
  }
  
  for (tab_name in names(input_list)) {
    if (!tab_name %in% names(ordered_input_list)) {
      ordered_input_list[[tab_name]] <- reorder_tab_fields(tab_name, input_list[[tab_name]])
    }
  }
  complete_json <- list(
    input = ordered_input_list,
    output = output_list
  )
  
  # Convert the complete structure to JSON
  json_output <- toJSON(complete_json, pretty = TRUE, auto_unbox = TRUE)
  
  # Define the JSON filename and write the file
  json_filename <- "results.json"
  write(json_output, file = json_filename)
  print(paste("--- Complete JSON (input + output) saved to", json_filename, "---"))
  
  # --- 6. Upload JSON Results to S3 ---
  s3_object_key <- paste0("results/results-", job_id, ".json")
  print(paste("--- Uploading results to s3://", s3_bucket_name, "/", s3_object_key, " ---", sep=""))
  
  if (test_mode != "true") {
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

    # --- Delete local JSON file after successful S3 upload ---
    if (file.exists(json_filename)) {
      try({ file.remove(json_filename) }, silent = TRUE)
    }
  } else {
    print("--- Skipping S3 upload and DynamoDB update in test mode ---")
    print("--- Key results saved locally ---")
    if ("PFD" %in% names(output_list)) {
      print(paste("PFD Mean:", output_list$PFD$mean))
      print(paste("PFD SD:", output_list$PFD$sd))
    }
  }
  
  # --- Cleanup JAGS objects to free memory ---
  if (exists("jags_model")) rm(jags_model)
  if (exists("jags_samples")) rm(jags_samples)
  invisible(gc())

  print("--- Script finished successfully. ---")
  
}, error = function(e) {
  
  # --- This block runs ONLY if an error occurred in the `tryCatch` block ---
  error_message <- paste("Error during simulation:", e$message)
  print(error_message)
  
  # Update job status to FAILED in DynamoDB (only if not in test mode)
  if (test_mode != "true") {
    dynamodb$update_item(
      TableName = table_name,
      Key = list(jobId = list(S = job_id)),
      UpdateExpression = "SET jobStatus = :s, errorMessage = :e",
      ExpressionAttributeValues = list(
        ":s" = list(S = "FAILED"),
        ":e" = list(S = error_message)
      )
    )
  } else {
    print("--- Skipping DynamoDB error update in test mode ---")
  }
  
  # Cause the script to exit with an error code
  quit(status = 1)
})