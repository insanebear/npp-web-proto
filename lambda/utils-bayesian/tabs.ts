/**
 * Validation schema (repo-managed TS)
 * - Single source of truth for allowed field values per tab
 * - Directly synced from live JS in lambda/aws-live/extracted
 * - Used by validate.ts for form data validation
 */

// This block contains two files that you would package together in a .zip file for deployment.

// --- /validation/schema.js ---
// This file acts as the single source of truth for our validation rules.
// It's directly derived from your TABS.ts constant.

const TABS = [
  {
    label: "FP",
    children: [{ label: "FP Input", values: [""] }],
  },
  {
    label: "Requirement Dev",
    children: [
      {
        label: "Software Development Planning",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Development of Concept",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Development of SRS",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Criticality Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Quanlification",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Acceptance",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Requirement V&V",
    children: [
      {
        label: "Software Planning",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Concpet Documentation Evaluation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware User Requirement Allocation Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware Requirement Evaluation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Interface Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Criticality Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Quanlification",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Acceptance",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Acitivity Summary Report",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Design Dev",
    children: [
      {
        label: "Development Sofware Architecture",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Development Sofware Design",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Criticality Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware Component Test Plan",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Plan",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Component Test Design",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Design",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Quanlification",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Acceptance",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Design V&V",
    children: [
      {
        label: "Design Evaluation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Interface Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Criticality Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Component Test Plan",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Plan",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Component Test Design",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Design",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Quanlification",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Acceptance",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Acitivity Summary Report",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Implementation Dev",
    children: [
      {
        label: "Source Code Document",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Criticality Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware Component Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware Acceptance Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Component Test Procedure",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Procedure",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Quanlification",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Component Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Implementation V&V",
    children: [
      {
        label: "Source Code Document",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Interface Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Criticality Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware Component Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Qualification Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Sofware Acceptance Test Case",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Component Test Procedure",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Software Integration Test Procedure",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Quanlification Test Procedure",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Component Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Acitivity Summary Report",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Test Dev",
    children: [
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Acceptance Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Acceptance Procedure Generation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Integration Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Quanlification Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Test V&V",
    children: [
      {
        label: "Traceability Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Software Acceptance Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Acceptance Procedure Generation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Integration Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "System Sofware Quanlification Test Execution",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Configuration Management",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Review and Audit",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Acitivity Summary Report",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Installlation and Checkout Dev",
    children: [
      {
        label: "Installation Procedure Generation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Installation and Checkout",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
  {
    label: "Installlation and Checkout V&V",
    children: [
      {
        label: "Installation Procedure Generation",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Installation and Checkout",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Hazard Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Security Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Risk Analysis",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Acitivity Summary Report",
        values: ["Low", "Medium", "High"],
      },
      {
        label: "Final Report Generation",
        values: ["Low", "Medium", "High"],
      },
    ],
  },
] as const;


// To make lookups faster, we transform the array into a Map object.
// The key will be the field label (e.g., "Software Development Planning")
// and the value will be the array of its allowed values (e.g., ["Low", "Medium", "High"]).
const validationSchema = new Map();

TABS.forEach(tab => {
  tab.children.forEach(child => {
    validationSchema.set(child.label, child.values);
  });
});

// We export the schema so our handler can use it.
export { validationSchema };