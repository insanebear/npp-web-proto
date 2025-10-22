# ===================================================================
# Simple Test Script for run_simulation.R Changes
# ===================================================================
# This script tests specific parts of your changes without running the full simulation
# ===================================================================

print("--- Testing run_simulation.R Changes ---")

# Test 1: Check if required libraries can be loaded
print("--- Test 1: Library Loading ---")
tryCatch({
  library("rjags")
  library("jsonlite")
  print("✓ All required libraries loaded successfully")
}, error = function(e) {
  print(paste("✗ Library loading failed:", e$message))
})

# Test 2: Check if data.R can be sourced
print("--- Test 2: Data Loading ---")
tryCatch({
  source("plumber/data.R")
  print("✓ Data loaded successfully")
  print(paste("  - Number of data elements:", length(data)))
}, error = function(e) {
  print(paste("✗ Data loading failed:", e$message))
})

# Test 3: Test environment variable parsing functions
print("--- Test 3: Environment Variable Parsing ---")
getenv_numeric <- function(var_name, default_val = 2) {
  val <- Sys.getenv(var_name, unset = "")
  if (val == "High") val <- "1"
  if (val == "Medium") val <- "2"
  if (val == "Low") val <- "3"
  if (is.null(val) || val == "") return(default_val)
  return(as.numeric(val))
}

getenv_logical <- function(var_name, default_val = TRUE) {
  val <- tolower(Sys.getenv(var_name, unset = ""))
  if (val == "") return(default_val)
  return(val == "true")
}

# Test the functions
test_fp <- getenv_numeric("FP Input", 50)
test_sdp <- getenv_numeric("Software Development Planning", 2)
test_logical <- getenv_logical("computeDIC", TRUE)

print(paste("✓ FP Input:", test_fp))
print(paste("✓ Software Development Planning:", test_sdp))
print(paste("✓ computeDIC:", test_logical))

# Test 4: Check if model file exists
print("--- Test 4: Model File Check ---")
model_file <- "plumber/R2WinBUGS_Combined_Model.txt"
if (file.exists(model_file)) {
  print(paste("✓ Model file exists:", model_file))
  file_info <- file.info(model_file)
  print(paste("  - File size:", file_info$size, "bytes"))
} else {
  print(paste("✗ Model file not found:", model_file))
}

# Test 5: Test JSON creation
print("--- Test 5: JSON Creation ---")
tryCatch({
  test_data <- list(
    test_param = list(
      mean = 0.5,
      sd = 0.1,
      median = 0.5,
      q2_5 = 0.3,
      q97_5 = 0.7
    )
  )
  json_output <- toJSON(test_data, pretty = TRUE, auto_unbox = TRUE)
  write(json_output, file = "test_output.json")
  print("✓ JSON creation and writing successful")
  print("  - Test file created: test_output.json")
}, error = function(e) {
  print(paste("✗ JSON creation failed:", e$message))
})

print("--- All tests completed ---")
