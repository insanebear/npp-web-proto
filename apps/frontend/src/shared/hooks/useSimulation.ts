import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAppState } from '../contexts/AppStateContext';
import * as apiService from '../services/apiService';
import type { SimulationInput } from '../types';

export const useSimulation = () => {
  const location = useLocation();

  const {
    jobId,
    setJobId,
    jobStatus,
    setJobStatus,
    setResults,
    setError,
    setSimulationInput,
    setPendingFile,
    setInputValues,
    initializeInputState,
  } = useAppState();

  /**
   * Start a new simulation with the provided form data
   * @param formData - The form data containing simulation parameters
   */
  const handleStartSimulation = async (formData: SimulationInput) => {
    setError(null);
    setResults(null);
    setJobStatus('Submitting...');
    setSimulationInput(formData);
    try {
      const newJobId = await apiService.startSimulation(formData);
      setJobId(newJobId);
    } catch (err: any) {
      setError(err.message);
      setJobStatus(null);
    }
  };

  /**
   * Reset all application state to initial values
   */
  const handleReset = () => {
    setJobId(null);
    setJobStatus(null);
    setResults(null);
    setError(null);
    setSimulationInput(null);
    setPendingFile(null);
    setInputValues(initializeInputState());
  };

  // Job status polling effect
  useEffect(() => {
    if (!jobId || jobStatus === 'COMPLETED' || jobStatus === 'FAILED' || jobId === 'local') {
      return;
    }
    const intervalId = setInterval(async () => {
      try {
        const statusData = await apiService.getJobStatus(jobId);
        setJobStatus(statusData.jobStatus);
        if (statusData.jobStatus === 'FAILED') {
          setError('The simulation job failed.');
        }
      } catch (err) {
        setError('Failed to get job status.');
        setJobId(null);
      }
    }, 5000);
    return () => clearInterval(intervalId);
  }, [jobId, jobStatus, setJobId, setJobStatus, setError]);

  // Results download effect
  useEffect(() => {
    if (jobStatus === 'COMPLETED' && jobId && jobId !== 'local') {
      apiService.getResults(jobId)
        .then(setResults)
        .catch((err: any) => setError(`Failed to fetch final results: ${err?.message ?? err}`));
    }
  }, [jobStatus, jobId, setResults, setError]);

  // URL job ID extraction effect
  useEffect(() => {
    const pathParts = location.pathname.split('/');
    const urlJobId = pathParts[2];
    if (pathParts[1] === 'reliability-views' && urlJobId && urlJobId !== 'local' && !jobId) {
      setJobId(urlJobId);
    }
  }, [location.pathname, jobId, setJobId]);

  return {
    handleStartSimulation,
    handleReset,
  };
};