/**
 * Parser utility (repo-managed TS)
 * - Parses API Gateway event body shaped like: { data: stringifiedJSON }
 * - Last synced with live JS in lambda/aws-live/extracted.
 */

import { APIGatewayProxyEvent } from 'aws-lambda';

interface ParseResult {
  success: boolean;
  data: any | null;
  error: string | null;
}

export function parseRequestBody(event: APIGatewayProxyEvent): ParseResult {
  try {
    if (!event.body) {
      return { success: false, data: null, error: "Request body is empty." };
    }

    // First parse: gets the outer object, e.g., { data: "..." }
    const outerObject = JSON.parse(event.body);

    if (typeof outerObject.data !== 'string') {
      return { success: false, data: null, error: "Request body must contain a 'data' key with a stringified JSON object." };
    }

    // Second parse: gets the actual form data from the inner string
    const innerData = JSON.parse(outerObject.data);
    
    return { success: true, data: innerData, error: null };

  } catch (error) {
    console.error("JSON Parsing Error:", error);
    return { success: false, data: null, error: "Invalid JSON format in request body." };
  }
}