// =======================================================
// ================== API CONFIGURATION ==================
// =======================================================

// Load API URL from environment variables (Vite uses import.meta.env)
// ⚠️ Security: Environment variables are required. Please configure .env file.
// See .env.example for reference.
// Note: REST API Gateway URLs include stage path (/prod or /develop).
// Development mode (npm run dev) uses DEV variables, production build uses production variables.

function getRequiredEnvVar(name: string): string {
  const value = import.meta.env[name];
  if (!value) {
    throw new Error(
      `Missing required environment variable: ${name}\n` +
      `Please create a .env file with ${name} set to your API Gateway URL.\n` +
      `See .env.example for reference.`
    );
  }
  return value;
}

// Development vs Production environment selection
const isDevelopment = import.meta.env.MODE === 'development';

// Select API URLs based on environment
const API_BASE_URL = isDevelopment
  ? getRequiredEnvVar('VITE_API_DEV_BASE_URL')
  : getRequiredEnvVar('VITE_API_BASE_URL');

const API_BASE_URL_SST = isDevelopment
  ? getRequiredEnvVar('VITE_API_DEV_BASE_URL_SST')
  : getRequiredEnvVar('VITE_API_BASE_URL_SST');

// API Key: same key used for both development and production
const API_KEY = getRequiredEnvVar('VITE_API_KEY');

// Common headers for API requests
// Note: REST API is protected by Usage Plan + API Key
const getApiHeaders = () => ({
  'Content-Type': 'application/json',
  'x-api-key': API_KEY,
});

// =======================================================
// ================ BAYESIAN PAGE ENDPOINTS ==============
// =======================================================

/**
 * Starts a Bayesian simulation job with the provided form data.
 * @param formData - The form data containing simulation parameters
 * @returns The jobId for tracking the simulation progress
 */
export const startSimulation = async (formData: object): Promise<string> => {
  const requestBody = { data: JSON.stringify(formData) };

  const response = await fetch(`${API_BASE_URL}/simulations/bayesian`, {
    method: 'POST',
    headers: getApiHeaders(),
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.message || 'Failed to start the job.');
  }

  const result = await response.json();
  if (!result.jobId) {
    throw new Error('API response did not include a jobId.');
  }
  return result.jobId;
};

/**
 * Fetches the current status of a simulation job.
 * @param jobId - The unique identifier for the job
 * @returns The full status object from the backend
 */
export const getJobStatus = async (jobId: string) => {
  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`, {
    headers: getApiHeaders(),
  });
  if (!response.ok) throw new Error('Failed to fetch job status.');
  return response.json();
};

/**
 * Gets the final results for a completed BBN simulation job.
 * Fetches from hybrid-tool-results S3 bucket via getResults Lambda.
 * @param jobId - The unique identifier for the job
 * @returns The final JSON results: { input, output: { PFD: { mean, sd, median, q5, q95 } } }
 */
export const getResults = async (jobId: string) => {
  const response = await fetch(
    `${API_BASE_URL_SST}/api/v1/results/${jobId}?type=bbn-inference`,
    { headers: getApiHeaders() }
  );
  if (!response.ok) throw new Error('Could not get results.');

  const wrapper = await response.json();
  // wrapper = { job_id, status, data: { input, output }, s3_location }
  const data = wrapper?.data ?? wrapper;
  const rawText = JSON.stringify(data, null, 2);
  if (data && typeof data === 'object') {
    (data as any).__rawText = rawText;
  }
  return data;
};

// =======================================================
// ============== STATISTICAL PAGE ENDPOINTS =============
// =======================================================

type BbnInputOptions = {
  bbn_input_s3_bucket?: string;
  bbn_input_s3_key?: string;
  /** S3 key of a pre-computed prior trace (.nc file). Skips BBN model run when provided. */
  prior_trace_s3_key?: string;
};

type HybridToolSettings = {
  draws?: number;
  tune?: number;
  chains?: number;
  thin?: number;
};

export type SensitivityIn = {
  pfd_goal: number;
  confidence_goal: number;
  /** Test history: tests already performed (default 0 = plan from scratch) */
  demand?: number;
  /** Test history: failures observed so far (default 0) */
  failures?: number;
  trace_id?: string | null;
  test_mode?: boolean;
  settings?: HybridToolSettings;
} & BbnInputOptions;

export type PfdUpdateIn = {
  pfd_goal: number; 
  confidence_goal: number; 
  failures: number; 
  demand_required?: number;
  trace_id?: string | null; 
  test_mode?: boolean;
  settings?: HybridToolSettings;
} & BbnInputOptions;

// HybridTool job request response (same for all trigger functions)
export type HybridToolJobResponse = {
  job_id: string;
  message: string;
  task_arn?: string;
};

// HybridTool results response
export type HybridToolResultsResponse = {
  job_id: string;
  download_url?: string; // Only for pfd-update (full-analysis)
  data?: SensitivityAnalysisResult; // Only for sensitivity-analysis (returned directly from Lambda)
  status: 'completed' | 'not_found' | 'failed';
  s3_location?: string;
  message?: string;
};

// BBN result listing
export type BbnResultItem = {
  key: string;
  name: string;
  size?: number;
  last_modified?: string;
};

export type BbnResultListResponse = {
  bucket: string;
  prefix: string;
  count: number;
  items: BbnResultItem[];
};

export type BbnResultFileResponse = {
  bucket: string;
  key: string;
  size?: number;
  last_modified?: string;
  data: any;
};

// Result file structure from S3 (sensitivity-analysis)
export type SensitivityAnalysisResult = {
  message: string;
  data: {
    num_tests: number;
    /** Tests still to run = num_tests − tests_performed (absent in legacy results) */
    additional_tests?: number;
    tests_performed?: number;
    failures?: number;
    goal_already_achieved?: boolean;
    prior_mean: number;
    prior_confidence: number;
  };
};

/**
 * Performs sensitivity analysis to determine the number of required tests.
 * NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
 * @param payload - Input parameters for sensitivity analysis
 * @returns Job response with job_id for async processing
 */
export const sensitivityAnalysis = (payload: SensitivityIn) =>
  postJSON<HybridToolJobResponse>('/api/v1/sensitivity-analysis', payload);

/**
 * Runs PFD update (Bayesian update + full analysis).
 * NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
 * @param payload - Input parameters for PFD update
 * @returns Job response with job_id for async processing
 */
// TODO: Rename endpoint '/api/v1/full-analysis' to '/api/v1/pfd-update' once backend is updated.
//       Backend: Dockers/HybridTool/run_full_analysis.py (ECS Fargate task)
//       Runs composite job: sensitivity analysis → BBN inference → PFD update
//       S3 result key also uses 'full-analysis' prefix and must be updated together.
export const pfdUpdate = (payload: PfdUpdateIn) =>
  postJSON<HybridToolJobResponse>('/api/v1/full-analysis', payload);

/**
 * Gets the job status from DynamoDB (same approach as OpenBUGS_BBN)
 * @param jobId - The job ID returned from the trigger function
 * @returns Job status object with jobStatus field
 */
export const getHybridToolJobStatus = async (
  jobId: string
): Promise<{ jobId: string; jobStatus: string; jobType?: string; errorMessage?: string }> => {
  const response = await fetch(
    `${API_BASE_URL_SST}/api/v1/jobs/${jobId}`,
    { headers: getApiHeaders() }
  );

  if (!response.ok) {
    let message = '';
    try {
      const data = await response.json();
      message = data.message || `HTTP ${response.status}`;
    } catch {
      message = await response.text().catch(() => `HTTP ${response.status}`);
    }
    throw new Error(message);
  }

  return response.json();
};

/**
 * Gets the results for a hybrid tool job.
 * @param jobId - The job ID returned from the trigger function
 * @param type - The type of analysis (sensitivity-analysis, full-analysis)
 * @returns Results response with download URL or status
 */
export const getHybridToolResults = async (
  jobId: string,
  // TODO: Replace 'full-analysis' with 'pfd-update' once backend renames the task type string.
  type: 'sensitivity-analysis' | 'full-analysis'
): Promise<HybridToolResultsResponse> => {
  const response = await fetch(
    `${API_BASE_URL_SST}/api/v1/results/${jobId}?type=${type}`,
    { headers: getApiHeaders() }
  );

  // 404 is a normal response (file not yet created) - continue polling
  if (response.status === 404) {
    const data = await response.json().catch(() => ({}));
    return {
      job_id: jobId,
      status: 'not_found' as const,
      message: data.message || 'Results not found',
      ...data
    };
  }

  // Throw error for non-404 responses
  if (!response.ok) {
    let message = '';
    try {
      const data = await response.json();
      message = data.message || `HTTP ${response.status}`;
    } catch {
      message = await response.text().catch(() => `HTTP ${response.status}`);
    }
    throw new Error(message);
  }

  return response.json();
};

// =======================================================
// ============= BBN RESULT MANAGEMENT ENDPOINTS =========
// =======================================================

export const listBbnResultFiles = (limit?: number) => {
  const search = typeof limit === 'number' ? `?limit=${encodeURIComponent(limit)}` : '';
  return getJSON<BbnResultListResponse>(`/api/v1/results${search}`);
};

export const fetchBbnResultFile = (key: string) => {
  const params = new URLSearchParams({ key });
  return getJSON<BbnResultFileResponse>(`/api/v1/results?${params.toString()}`);
};

// =======================================================
// ================ PRESIGNED URL ENDPOINTS ==============
// =======================================================

export type UploadUrlResponse = {
  upload_url: string;
  s3_key: string;
  bucket: string;
};

export type DownloadUrlResponse = {
  download_url: string;
  key: string;
  bucket: string;
};

/**
 * Requests a presigned PUT URL for uploading a file to S3 (uploads/temp/ prefix).
 * The object is automatically deleted by S3 lifecycle policy after 24 hours.
 */
export const getUploadPresignedUrl = (filename: string, contentType: string) =>
  postJSON<UploadUrlResponse>('/api/v1/presigned-url', { filename, content_type: contentType });

/**
 * Requests a presigned GET URL for downloading a file from S3 by key.
 */
export const getDownloadPresignedUrl = (key: string) => {
  const params = new URLSearchParams({ key });
  return getJSON<DownloadUrlResponse>(`/api/v1/presigned-url?${params.toString()}`);
};

/**
 * Uploads a File to S3 using a presigned PUT URL.
 * Returns the S3 key of the uploaded file.
 */
export const uploadFileToS3 = async (file: File): Promise<{ s3_key: string; bucket: string }> => {
  const contentType = file.type || 'application/octet-stream';
  const { upload_url, s3_key, bucket } = await getUploadPresignedUrl(file.name, contentType);

  const res = await fetch(upload_url, {
    method: 'PUT',
    headers: { 'Content-Type': contentType },
    body: file,
  });

  if (!res.ok) {
    throw new Error(`Failed to upload file to S3: HTTP ${res.status}`);
  }

  return { s3_key, bucket };
};

// =======================================================
// ================== HELPER FUNCTIONS ===================
// =======================================================

/**
 * Joins a base URL with a path, handling trailing and leading slashes.
 * @param base - The base URL
 * @param path - The path to append
 * @returns The properly joined URL
 */
const join = (base: string, path: string) =>
  `${base.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;

/**
 * Makes a POST request to the SST API and returns parsed JSON response.
 * @param path - The API endpoint path
 * @param body - The request body data
 * @returns Parsed JSON response
 */
async function postJSON<T = any>(path: string, body: any): Promise<T> {
  const res = await fetch(join(API_BASE_URL_SST, path), {
    method: 'POST',
    headers: getApiHeaders(),
    body: JSON.stringify(body ?? {}),
  });

  if (!res.ok) {
    let message = '';
    try {
      const j = await res.json();
      message = j?.message || JSON.stringify(j);
    } catch {
      message = await res.text().catch(() => '');
    }
    throw new Error(`[${res.status}] ${message || 'Request failed'}`);
  }

  const text = await res.text();
  return text ? (JSON.parse(text) as T) : ({} as T);
}

/**
 * Makes a GET request to the SST API and returns parsed JSON response.
 * @param path - The API endpoint path
 * @returns Parsed JSON response
 */
export async function getJSON<T = any>(path: string): Promise<T> {
  const res = await fetch(join(API_BASE_URL_SST, path), {
    headers: getApiHeaders(),
  });
  if (!res.ok) {
    let message = await res.text().catch(() => '');
    try { message = (await res.json())?.message ?? message; } catch {}
    throw new Error(`[${res.status}] ${message || 'Request failed'}`);
  }
  return res.json() as Promise<T>;
}

// Log only in development environment
if (import.meta.env.DEV) {
  console.log('API Configuration loaded:', {
    mode: isDevelopment ? 'development' : 'production',
    API_BASE_URL: API_BASE_URL.substring(0, 50) + '...',
    API_BASE_URL_SST: API_BASE_URL_SST.substring(0, 50) + '...'
  });
}