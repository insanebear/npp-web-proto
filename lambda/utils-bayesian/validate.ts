/**
 * Validation utility (repo-managed TS)
 * - Validates flattened form data against the validationSchema
 * - Settings fields are allowed/bypassed
 * - Last synced with live JS in lambda/aws-live/extracted.
 */

import { validationSchema } from './tabs';
import { labelToCode } from './labelToCode';

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

  for (const fieldKey in formData) {
    const submittedValue = formData[fieldKey];

    if (settingsFields.has(fieldKey)) {
      continue;
    }

    // Accept either label keys or python-code keys
    let effectiveLabel: string | null = null;
    if (validationSchema.has(fieldKey)) {
      effectiveLabel = fieldKey;
    } else {
      // try map code->label by scanning sections
      for (const section of Object.keys(labelToCode)) {
        const entries = (labelToCode as any)[section] as Record<string, string>;
        for (const [label, code] of Object.entries(entries)) {
          if (code === fieldKey) {
            effectiveLabel = label;
            break;
          }
        }
        if (effectiveLabel) break;
      }
    }

    if (!effectiveLabel || !validationSchema.has(effectiveLabel)) {
      errors.push(`Field '${fieldKey}' is not a valid field.`);
      continue;
    }

    const allowedValues = validationSchema.get(effectiveLabel);

    if (effectiveLabel === "FP Input") {
      if (typeof submittedValue !== 'string' || submittedValue.trim() === '') {
        errors.push("Field 'FP Input' must be a non-empty string.");
      }
      continue;
    }

    if (!allowedValues!.includes(submittedValue)) {
      errors.push(`Invalid value for '${effectiveLabel}'. Received '${submittedValue}', but expected one of: ${allowedValues!.join(', ')}.`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors: errors,
  };
}
