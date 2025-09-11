const API_BASE_URL = 'https://bm5kx387h8.execute-api.ap-northeast-2.amazonaws.com/prod';


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