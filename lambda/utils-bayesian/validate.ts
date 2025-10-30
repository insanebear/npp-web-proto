/**
 * Validation utility (repo-managed TS)
 * - Validates flattened form data against the validationSchema
 * - Settings fields are allowed/bypassed
 * - Last synced with live JS in lambda/aws-live/extracted.
 */

import { validationSchema } from './tabs';

interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export function validateFormData(formData: Record<string, any>): ValidationResult {
  console.log("Received request for validation.");
  const errors: string[] = [];

  const settingsFields = new Set<string>([
      "nChains", 
      "nIter", 
      "nBurnin", 
      "nThin",
      "autoCloseWinBugs",
      "computeDIC", 
      "workingDir",
      "includeTraceData"
  ]);

  if (typeof formData !== 'object' || formData === null) {
    return { isValid: false, errors: ["Request body must be a valid JSON object."] };
  }

  for (const fieldLabel in formData) {
    const submittedValue = formData[fieldLabel];

    if (settingsFields.has(fieldLabel)) {
      continue;
    }

    if (!validationSchema.has(fieldLabel)) {
      errors.push(`Field '${fieldLabel}' is not a valid field.`);
      continue;
    }

    const allowedValues = validationSchema.get(fieldLabel);

    if (fieldLabel === "FP Input") {
      if (typeof submittedValue !== 'string' || submittedValue.trim() === '') {
        errors.push("Field 'FP Input' must be a non-empty string.");
      }
      continue;
    }

    if (!allowedValues!.includes(submittedValue)) {
      errors.push(`Invalid value for '${fieldLabel}'. Received '${submittedValue}', but expected one of: ${allowedValues!.join(', ')}.`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors: errors,
  };
}
