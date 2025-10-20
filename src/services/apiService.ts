const API_BASE_URL = 'https://bm5kx387h8.execute-api.ap-northeast-2.amazonaws.com/prod';
const API_BASE_URL_SST = 'https://a2gxqrwnzi.execute-api.ap-northeast-2.amazonaws.com';

/**
 * Takes the form data, wraps it, and starts the simulation.
 * @returns The jobId for the new simulation.
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
 * Fetches the current status of a given job.
 * @returns The full status object from the backend.
 */
export const getJobStatus = async (jobId: string) => {
  const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
  if (!response.ok) throw new Error('Failed to fetch job status.');
  return response.json();
};

/**
 * Gets the final results for a completed job.
 * @returns The final JSON results from the S3 file.
 */
export const getResults = async (jobId: string) => {
  const urlResponse = await fetch(`${API_BASE_URL}/jobs/${jobId}/results-url`, { method: 'POST' });
  if (!urlResponse.ok) throw new Error('Could not get results URL.');
  
  const { downloadUrl } = await urlResponse.json();
  
  const resultsResponse = await fetch(downloadUrl);
  if (!resultsResponse.ok) throw new Error('Could not download results file from S3.');
  
  return resultsResponse.json();
};




//SST Page API Services
const join = (base: string, path: string) =>
  `${base.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;

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

export async function getJSON<T = any>(path: string): Promise<T> {
  const res = await fetch(join(API_BASE_URL_SST, path));
  if (!res.ok) {
    let message = await res.text().catch(() => '');
    try { message = (await res.json())?.message ?? message; } catch {}
    throw new Error(`[${res.status}] ${message || 'Request failed'}`);
  }
  return res.json() as Promise<T>;
}




// =======================================================
// ============== STATISTICAL PAGE ENDPOINTS =============
// =======================================================
//   POST /sensitivity-analysis
//   POST /update-pfd
//   POST /full-analysis

export type SensitivityIn  = { pfd_goal: number; confidence_goal: number; trace_id?: string | null };
export type SensitivityOut = { data: { num_tests: number }; trace_id?: string | null };

export type UpdatePfdIn    = { pfd_goal: number; demand: number; failures: number; trace_id?: string | null };
export type UpdatePfdOut   = { message?: string; trace_id?: string | null };

export type FullAnalysisIn = { pfd_goal: number; confidence_goal: number; failures: number; trace_id?: string | null };
export type FullAnalysisOut= { download_url?: string; trace_id?: string | null };

export const sensitivityAnalysis = (payload: SensitivityIn) =>
  postJSON<SensitivityOut>('/sensitivity-analysis', payload);

export const updatePfd = (payload: UpdatePfdIn) =>
  postJSON<UpdatePfdOut>('/update-pfd', payload);

export const fullAnalysis = (payload: FullAnalysisIn) =>
  postJSON<FullAnalysisOut>('/full-analysis', payload);

// Helpful while debugging:
console.log('API_BASE_URL_SST =', API_BASE_URL_SST);