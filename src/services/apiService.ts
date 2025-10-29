// =======================================================
// ================== API CONFIGURATION ==================
// =======================================================

const API_BASE_URL = 'https://bm5kx387h8.execute-api.ap-northeast-2.amazonaws.com/prod';
// const API_BASE_URL_SST = 'https://a2gxqrwnzi.execute-api.ap-northeast-2.amazonaws.com';
const API_BASE_URL_SST = 'http://localhost:8000';

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
    headers: { 'Content-Type': 'application/json' },
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
  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
  if (!response.ok) throw new Error('Failed to fetch job status.');
  return response.json();
};

/**
 * Gets the final results for a completed simulation job.
 * @param jobId - The unique identifier for the job
 * @returns The final JSON results from the S3 file
 */
export const getResults = async (jobId: string) => {
  const urlResponse = await fetch(`${API_BASE_URL}/jobs/${jobId}/results-url`, { method: 'POST' });
  if (!urlResponse.ok) throw new Error('Could not get results URL.');
  
  const { downloadUrl } = await urlResponse.json();
  
  const resultsResponse = await fetch(downloadUrl);
  if (!resultsResponse.ok) throw new Error('Could not download results file from S3.');
  // Preserve the original JSON text as-is
  const rawText = await resultsResponse.text();
  try {
    const parsed = rawText ? JSON.parse(rawText) : {};
    // Attach the original raw text so the UI can display it unchanged
    if (parsed && typeof parsed === 'object') {
      (parsed as any).__rawText = rawText;
    }
    return parsed;
  } catch {
    // If parsing fails, return an object containing only the raw text
    return { __rawText: rawText } as any;
  }
};

// =======================================================
// ============== STATISTICAL PAGE ENDPOINTS =============
// =======================================================

export type SensitivityIn  = { pfd_goal: number; confidence_goal: number; trace_id?: string | null };
export type SensitivityOut = { data: { num_tests: number }; trace_id?: string | null };

export type UpdatePfdIn    = { pfd_goal: number; demand: number; failures: number; trace_id?: string | null };
export type UpdatePfdOut   = { message?: string; trace_id?: string | null };

export type FullAnalysisIn = { pfd_goal: number; confidence_goal: number; failures: number; trace_id?: string | null };
export type FullAnalysisOut= { download_url?: string; trace_id?: string | null };

/**
 * Performs sensitivity analysis to determine the number of required tests.
 * @param payload - Input parameters for sensitivity analysis
 * @returns Analysis results including number of tests required
 */
export const sensitivityAnalysis = (payload: SensitivityIn) =>
  postJSON<SensitivityOut>('/sensitivity-analysis', payload);

/**
 * Updates the Probability of Failure on Demand (PFD) based on observed data.
 * @param payload - Input parameters for PFD update
 * @returns Update confirmation message
 */
export const updatePfd = (payload: UpdatePfdIn) =>
  postJSON<UpdatePfdOut>('/update-pfd', payload);

/**
 * Runs a complete analysis including sensitivity analysis and PFD updates.
 * @param payload - Input parameters for full analysis
 * @returns Download URL for the analysis results
 */
export const fullAnalysis = (payload: FullAnalysisIn) =>
  postJSON<FullAnalysisOut>('/full-analysis', payload);

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
    headers: { 'Content-Type': 'application/json' },
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
  const res = await fetch(join(API_BASE_URL_SST, path));
  if (!res.ok) {
    let message = await res.text().catch(() => '');
    try { message = (await res.json())?.message ?? message; } catch {}
    throw new Error(`[${res.status}] ${message || 'Request failed'}`);
  }
  return res.json() as Promise<T>;
}

// Debug logging for development
console.log('API_BASE_URL_SST =', API_BASE_URL_SST);