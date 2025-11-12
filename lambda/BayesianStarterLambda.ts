/**
 * AWS Lambda Function: BayesianStarterLambda
 *
 * Source of truth: This TypeScript file is the repo-managed Lambda source.
 * Build with tsc (see scripts/deploy-lambda.sh). The deployed handler
 * remains "lambda/BayesianStarterLambda.handler" via preserved output paths.
 * Last synced with live JS in lambda/aws-live/extracted.
 *
 * Workflow:
 * 1) Receive request via API Gateway
 * 2) Parse and validate form data
 * 3) Write job item to DynamoDB (PENDING)
 * 4) Start ECS Fargate task with env vars
 * 5) Return 202 with jobId
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
  if (!TABLE_NAME || !CLUSTER_NAME || !TASK_DEFINITION || !SUBNET_ID || !CONTAINER_NAME) {
    console.error("Missing required environment variables.");
    return {
      statusCode: 500,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Internal server error: Service is not configured correctly." }),
    };
  }

  // 2. Request data parsing
  const { success, data: nestedData, error: parsingError } = parseRequestBody(event);

  if (!success || !nestedData) {
    return {
      statusCode: 400,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: parsingError }),
    };
  }

  // 3. Data structure flattening
  const { settings, ...tabData } = nestedData;
  const flatFormData: Record<string, any> = { ...settings };

  for (const key in tabData) {
      Object.assign(flatFormData, tabData[key]);
  }

  // 4. Form data validation
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

    const dbItem = {
      jobId,
      jobType: "bayesian-simulation",
      jobStatus: "PENDING",
      formData: flatFormData,
      createdAt: new Date().toISOString(),
    };
    await docClient.send(new PutCommand({ TableName: TABLE_NAME, Item: dbItem }));

    // 6. Prepare env vars for Fargate container
    const formDataEnvironmentVariables = Object.entries(flatFormData).map(([key, value]) => ({
      name: key,
      value: String(value),
    }));

    // 7. Configure Fargate task execution command
    const command = new RunTaskCommand({
      cluster: CLUSTER_NAME,
      taskDefinition: TASK_DEFINITION,
      launchType: "FARGATE",
      networkConfiguration: {
        awsvpcConfiguration: {
          subnets: [SUBNET_ID],
          assignPublicIp: "ENABLED"
        },
      },
      overrides: {
        containerOverrides: [{
          name: CONTAINER_NAME,
          environment: [
            { name: "JOB_ID", value: jobId },
            ...formDataEnvironmentVariables
          ],
        }],
      },
    });

    // 8. Execute Fargate task
    await ecsClient.send(command);
    console.log(`Fargate task started successfully for job ${jobId}.`);

    // 9. Return success response
    return {
      statusCode: 202,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Job accepted for processing.", jobId }),
    };
  } catch (error) {
    console.error("Error activating Fargate task:", error);
    return {
      statusCode: 500,
      headers: { "Access-Control-Allow-Origin": "*" },
      body: JSON.stringify({ message: "Internal server error: Could not start the simulation job." }),
    };
  }
};