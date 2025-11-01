// =======================================================
// ================== API CONFIGURATION ==================
// =======================================================

// 환경 변수에서 API URL 로드 (Vite는 import.meta.env 사용)
// .env 파일에 다음 변수들을 설정하세요:
// VITE_API_BASE_URL=https://bm5kx387h8.execute-api.ap-northeast-2.amazonaws.com/prod
// VITE_API_BASE_URL_SST=https://a2gxqrwnzi.execute-api.ap-northeast-2.amazonaws.com
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://bm5kx387h8.execute-api.ap-northeast-2.amazonaws.com/prod';
const API_BASE_URL_SST = import.meta.env.VITE_API_BASE_URL_SST || 'https://a2gxqrwnzi.execute-api.ap-northeast-2.amazonaws.com';
// 개발 환경에서는 로컬 서버 사용 가능
// const API_BASE_URL_SST = import.meta.env.DEV ? 'http://localhost:8000' : import.meta.env.VITE_API_BASE_URL_SST;

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

// 입력 타입 (기존 유지)
export type SensitivityIn  = { pfd_goal: number; confidence_goal: number; trace_id?: string | null; test_mode?: boolean };
export type UpdatePfdIn    = { pfd_goal: number; demand: number; failures: number; trace_id?: string | null; test_mode?: boolean };
export type FullAnalysisIn = { pfd_goal: number; confidence_goal: number; failures: number; trace_id?: string | null; test_mode?: boolean };

// HybridTool 작업 요청 응답 (모든 trigger 함수 동일)
export type HybridToolJobResponse = {
  job_id: string;
  message: string;
  task_arn?: string;
};

// HybridTool 결과 조회 응답
export type HybridToolResultsResponse = {
  job_id: string;
  download_url?: string; // update-pfd, full-analysis에만 있음
  data?: SensitivityAnalysisResult; // sensitivity-analysis에만 있음 (Lambda 직접 반환)
  status: 'completed' | 'not_found' | 'failed';
  s3_location?: string;
  message?: string;
};

// S3에서 다운로드한 결과 파일 구조 (sensitivity-analysis)
export type SensitivityAnalysisResult = {
  message: string;
  data: {
    num_tests: number;
    prior_mean: number;
    prior_confidence: number;
  };
};

// 기존 동기 응답 타입 (호환성 유지 - 더 이상 사용 안 함)
export type SensitivityOut = { data: { num_tests: number }; trace_id?: string | null };
export type UpdatePfdOut   = { message?: string; trace_id?: string | null };
export type FullAnalysisOut= { download_url?: string; trace_id?: string | null };

/**
 * Performs sensitivity analysis to determine the number of required tests.
 * NOTE: trace_id는 전송되지만 HybridTool에서는 무시됨 (stateless 아키텍처)
 * @param payload - Input parameters for sensitivity analysis
 * @returns Job response with job_id for async processing
 */
export const sensitivityAnalysis = (payload: SensitivityIn) =>
  postJSON<HybridToolJobResponse>('/api/v1/sensitivity-analysis', payload);

/**
 * Updates the Probability of Failure on Demand (PFD) based on observed data.
 * NOTE: trace_id는 전송되지만 HybridTool에서는 무시됨 (stateless 아키텍처)
 * @param payload - Input parameters for PFD update
 * @returns Job response with job_id for async processing
 */
export const updatePfd = (payload: UpdatePfdIn) =>
  postJSON<HybridToolJobResponse>('/api/v1/update-pfd', payload);

/**
 * Runs a complete analysis including sensitivity analysis and PFD updates.
 * NOTE: trace_id는 전송되지만 HybridTool에서는 무시됨 (stateless 아키텍처)
 * @param payload - Input parameters for full analysis
 * @returns Job response with job_id for async processing
 */
export const fullAnalysis = (payload: FullAnalysisIn) =>
  postJSON<HybridToolJobResponse>('/api/v1/full-analysis', payload);

/**
 * Gets the job status from DynamoDB (BayesianPage와 동일한 방식)
 * @param jobId - The job ID returned from the trigger function
 * @returns Job status object with jobStatus field
 */
export const getHybridToolJobStatus = async (
  jobId: string
): Promise<{ jobId: string; jobStatus: string; jobType?: string; errorMessage?: string }> => {
  const response = await fetch(
    `${API_BASE_URL_SST}/api/v1/jobs/${jobId}`
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
 * @param type - The type of analysis (sensitivity-analysis, update-pfd, full-analysis)
 * @returns Results response with download URL or status
 */
export const getHybridToolResults = async (
  jobId: string,
  type: 'sensitivity-analysis' | 'update-pfd' | 'full-analysis'
): Promise<HybridToolResultsResponse> => {
  const response = await fetch(
    `${API_BASE_URL_SST}/api/v1/results/${jobId}?type=${type}`
  );

  // 404는 정상적인 응답 (파일이 아직 생성되지 않음) - 폴링 계속
  if (response.status === 404) {
    const data = await response.json().catch(() => ({}));
    return {
      job_id: jobId,
      status: 'not_found' as const,
      message: data.message || 'Results not found',
      ...data
    };
  }

  // 404가 아닌 다른 에러는 throw
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