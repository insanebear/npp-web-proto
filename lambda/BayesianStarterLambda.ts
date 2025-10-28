/**
 * AWS Lambda Function: BayesianStarterLambda
 * 
 * This Lambda function serves as the entry point for starting Bayesian simulation jobs.
 * It receives form data from the web application and initiates a container task on AWS Fargate
 * that runs R-based JAGS Bayesian simulations.
 * 
 * Workflow:
 * 1. Receive form data through API Gateway
 * 2. Parse and validate request data
 * 3. Store job status in DynamoDB (PENDING)
 * 4. Start simulation by passing data as environment variables to Fargate container
 * 5. Return job ID (client can use this to query job status)
 */

import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { parseRequestBody } from './utils-bayesian/parser';
import { validateFormData } from './utils-bayesian/validate';
import { ECSClient, RunTaskCommand } from "@aws-sdk/client-ecs";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, PutCommand } from "@aws-sdk/lib-dynamodb";
import { randomUUID } from "crypto";

// Initialize AWS service clients
const ecsClient = new ECSClient({});
const docClient = DynamoDBDocumentClient.from(new DynamoDBClient({}));

// Get AWS resource information from environment variables
const TABLE_NAME = process.env.JOBS_TABLE_NAME;        // DynamoDB table name (for storing job status)
const CLUSTER_NAME = process.env.CLUSTER_NAME;         // ECS cluster name
const TASK_DEFINITION = process.env.TASK_DEFINITION;   // Fargate task definition name
const SUBNET_ID = process.env.SUBNET_ID;               // VPC subnet ID
const CONTAINER_NAME = process.env.CONTAINER_NAME;     // Container name

export const handler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  console.log("Received request to start simulation job.");

  // 1. Environment variable validation
  // Check if Lambda function is properly configured
  if (!TABLE_NAME || !CLUSTER_NAME || !TASK_DEFINITION || !SUBNET_ID || !CONTAINER_NAME) {
    console.error("Missing required environment variables.");
    return {
      statusCode: 500,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Internal server error: Service is not configured correctly." }),
    };
  }

  // 2. Request data parsing
  // Parse JSON data received from API Gateway
  // Data structure from web app: { data: "JSON.stringify(formData)" }
  const { success, data: nestedData, error: parsingError } = parseRequestBody(event);

  if (!success || !nestedData) {
    return {
      statusCode: 400,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: parsingError }),
    };
  }

  // 3. Data structure flattening
  // Web app sends nested data: { settings: {...}, tab1: {...}, tab2: {...} }
  // Need to flatten for Fargate container environment variables
  const { settings, ...tabData } = nestedData;
  const flatFormData: Record<string, any> = { ...settings };

  // Merge each tab's data into flat structure
  for (const key in tabData) {
      Object.assign(flatFormData, tabData[key]);
  }

  // 4. Form data validation
  // Verify that submitted data is valid (required fields, allowed values, etc.)
  const { isValid, errors } = validateFormData(flatFormData);

  if (!isValid) {
    console.error("Validation failed:", errors);
    return {
      statusCode: 400,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Invalid form data submitted.", errors }),
    };
  }

  console.log("Validation successful. Proceeding to start Fargate task...");

  try {
    // 5. Generate job ID and store job status in DynamoDB
    const jobId = randomUUID();
    console.log(`Starting job with ID: ${jobId}`);

    // Store job information in DynamoDB (status: PENDING)
    // Client can query job status using this jobId
    const dbItem = {
      jobId,
      jobStatus: "PENDING",  // PENDING -> RUNNING -> COMPLETED/FAILED
      formData: flatFormData, // All form data needed for simulation
      createdAt: new Date().toISOString(),
    };
    await docClient.send(new PutCommand({ TableName: TABLE_NAME, Item: dbItem }));

    // 6. Prepare environment variables for Fargate container
    // Pass data as environment variables accessible via Sys.getenv() in R script
    const formDataEnvironmentVariables = Object.entries(flatFormData).map(([key, value]) => ({
      name: key,
      value: String(value), // Convert all values to strings (environment variables only support strings)
    }));

    // 7. Configure Fargate task execution command
    const command = new RunTaskCommand({
      cluster: CLUSTER_NAME,                    // ECS cluster
      taskDefinition: TASK_DEFINITION,          // Task definition (R container image)
      launchType: "FARGATE",                    // Serverless container execution
      networkConfiguration: {
        awsvpcConfiguration: { 
          subnets: [SUBNET_ID],                 // VPC subnet
          assignPublicIp: "ENABLED"             // Public IP for internet access
        },
      },
      overrides: {
        containerOverrides: [{
          name: CONTAINER_NAME,
          // Pass JOB_ID and all form data as environment variables
          environment: [
            { name: "JOB_ID", value: jobId },    // For R script to identify job ID
            ...formDataEnvironmentVariables      // All form data (FP Input, various settings, etc.)
          ],
        }],
      },
    });

    // 8. Execute Fargate task
    // R container starts and runs JAGS Bayesian simulation
    await ecsClient.send(command);
    console.log(`Fargate task started successfully for job ${jobId}.`);

    // 9. Return success response
    // Client can use jobId to poll job status
    return {
      statusCode: 202, // Accepted - indicates asynchronous job has started
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Job accepted for processing.", jobId }),
    };
  } catch (error) {
    // 10. Error handling
    console.error("Error activating Fargate task:", error);
    return {
      statusCode: 500,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Internal server error: Could not start the simulation job." }),
    };
  }
};

/**
 * Complete System Workflow:
 * 
 * 1. Web Application (React)
 *    - User fills out Bayesian simulation form
 *    - Input FP Input, various settings (nChains, nIter, etc.), tab-specific data
 *    - Calls this Lambda function when Submit button is clicked
 * 
 * 2. This Lambda Function (BayesianStarterLambda)
 *    - Parse and validate form data
 *    - Store job status in DynamoDB (PENDING)
 *    - Start R simulation by executing Fargate container
 *    - Return jobId
 * 
 * 3. Fargate Container (R + JAGS)
 *    - Run JAGS Bayesian simulation with data passed as environment variables
 *    - Update status in DynamoDB (RUNNING -> COMPLETED/FAILED)
 *    - Save simulation results as JSON to S3
 * 
 * 4. Web Application
 *    - Poll job status using jobId
 *    - Download results from S3 and display on screen when completed
 * 
 * Key Data Flow:
 * - Form data: Web App -> Lambda -> Fargate (environment variables)
 * - Job status: Lambda -> DynamoDB <- Fargate
 * - Simulation results: Fargate -> S3 -> Web App
 */