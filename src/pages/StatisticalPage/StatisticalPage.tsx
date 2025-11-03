/** @jsxImportSource @emotion/react */
import { useState, useEffect, useRef, type FormEvent } from "react";
import { Global } from "@emotion/react";
import { cssObj } from "./style";
import * as api from "../../services/apiService";
import type { SensitivityAnalysisResult } from "../../services/apiService";

// Polling configuration
const POLL_INTERVAL = 5000; // 5 seconds
const MAX_WAIT_TIME = 1200000; // 20 minutes (milliseconds)
const MAX_ATTEMPTS = 240; // Maximum 240 attempts (20 minutes / 5 seconds)

export default function StatisticalPage() {
  const [pfdGoal, setPfdGoal] = useState("");
  const [confidenceGoal, setConfidenceGoal] = useState("");
  // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture, maintained for compatibility)
  const [traceId, _setTraceId] = useState<string | null>(null);
  const [tests, setTests] = useState<number>(0);
  const [failures, setFailures] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [downloadLink, setDownloadLink] = useState<string | null>(null);
  const [sensitivityJobId, setSensitivityJobId] = useState<string | null>(null);
  const [updatePfdJobId, setUpdatePfdJobId] = useState<string | null>(null);
  const [fullAnalysisJobId, setFullAnalysisJobId] = useState<string | null>(null);

  const [isPolling, setIsPolling] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0); // Elapsed time in seconds
  const [currentJobType, setCurrentJobType] = useState<'sensitivity-analysis' | 'update-pfd' | 'full-analysis' | null>(null);
  const isDevelopment = import.meta.env.DEV;
  const [testMode, setTestMode] = useState(false); // Test mode (only enabled in development)
  const [sensitivityCompletedTime, setSensitivityCompletedTime] = useState<number | null>(null);
  const [updatePfdCompletedTime, setUpdatePfdCompletedTime] = useState<number | null>(null);
  const [fullAnalysisCompletedTime, setFullAnalysisCompletedTime] = useState<number | null>(null);
  const elapsedTimerRef = useRef<NodeJS.Timeout | null>(null);
  const pollingRef = useRef<{ jobId: string; type: string; attempts: number; startTime: number } | null>(null);

  useEffect(() => {
    if (isPolling) {
      elapsedTimerRef.current = setInterval(() => {
        setElapsedTime((prev) => prev + 1);
      }, 1000);
    } else {
      if (elapsedTimerRef.current) {
        clearInterval(elapsedTimerRef.current);
        elapsedTimerRef.current = null;
      }
      setElapsedTime(0);
    }
    return () => {
      if (elapsedTimerRef.current) {
        clearInterval(elapsedTimerRef.current);
      }
    };
  }, [isPolling]);

  const pollResults = async (
    jobId: string,
    type: 'sensitivity-analysis' | 'update-pfd' | 'full-analysis',
    jobStartTime: number, // Job start time passed from handler
    onComplete: (data: any, downloadUrl?: string, elapsedSeconds?: number) => void,
    onError: (error: string) => void
  ) => {
    let attempts = 0;
    const startTime = Date.now();
    pollingRef.current = { jobId, type, attempts: 0, startTime };

    const poll = async () => {
      // Timeout check
      if (attempts >= MAX_ATTEMPTS || Date.now() - startTime > MAX_WAIT_TIME) {
        setIsPolling(false);
        setCurrentJobType(null);
        onError('결과 조회 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.');
        return;
      }

      try {
        // Check job status from DynamoDB (same approach as BayesianPage)
        const statusData = await api.getHybridToolJobStatus(jobId);
        
        if (statusData.jobStatus === 'COMPLETED') {
          // Job completed → fetch results
          const response = await api.getHybridToolResults(jobId, type);
          
          if (response.status === 'completed') {
            // Calculate elapsed time from job start
            const completedElapsedTime = Math.floor((Date.now() - jobStartTime) / 1000);
            // All types return data directly from Lambda (solves presigned URL issues)
            if (response.data) {
              setIsPolling(false);
              setCurrentJobType(null);
              // For full-analysis, create download_url from data if needed
              let downloadUrl = response.download_url;
              if (type === 'full-analysis' && !downloadUrl && response.data) {
                // Create blob URL on frontend
                const jsonStr = JSON.stringify(response.data, null, 2);
                const blob = new Blob([jsonStr], { type: 'application/json' });
                downloadUrl = URL.createObjectURL(blob);
              }
              onComplete(response.data, downloadUrl, completedElapsedTime);
            } else if (response.download_url) {
              // Maintain compatibility with legacy approach
              setIsPolling(false);
              setCurrentJobType(null);
              onComplete(null, response.download_url, completedElapsedTime);
            } else {
              // Status is COMPLETED but no results found - error handling
              setIsPolling(false);
              setCurrentJobType(null);
              onError('작업이 완료되었지만 결과를 찾을 수 없습니다.');
            }
          } else {
            // Failed to fetch results
            setIsPolling(false);
            setCurrentJobType(null);
            onError(response.message || '결과 조회 실패');
          }
          return;
        } else if (statusData.jobStatus === 'FAILED') {
          // Job failed → immediate error handling
          setIsPolling(false);
          setCurrentJobType(null);
          onError(statusData.errorMessage || '작업이 실패했습니다.');
          return;
        } else {
          // PENDING, RUNNING status → continue polling
          attempts++;
          pollingRef.current = { jobId, type, attempts, startTime };
          setTimeout(poll, POLL_INTERVAL);
        }
      } catch (err: any) {
        console.error('Polling error:', err);
        
        // Server errors (403, 500) → stop immediately (retry won't help)
        const errorMessage = err?.message || String(err);
        if (errorMessage.includes('403') || errorMessage.includes('500') || 
            errorMessage.includes('Forbidden') || errorMessage.includes('Internal Server Error')) {
          setIsPolling(false);
          setCurrentJobType(null);
          onError(`서버 오류: ${errorMessage}. 결과 조회를 중단했습니다.`);
          return;
        }
        
        // 404 (no results) → continue polling, network errors → retry
        attempts++;
        if (attempts < MAX_ATTEMPTS) {
          pollingRef.current = { jobId, type, attempts, startTime };
          setTimeout(poll, POLL_INTERVAL);
        } else {
          setIsPolling(false);
          setCurrentJobType(null);
          onError('결과 조회 시간이 초과되었습니다. 잠시 후 다시 시도해주세요.');
        }
      }
    };

    poll();
  };

  // Format elapsed time (seconds → "mm:ss" or "X minutes Y seconds")
  const formatElapsedTime = (seconds: number): string => {
    if (seconds < 60) {
      return `${seconds}초`;
    }
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}분 ${secs}초`;
  };

  const handleSensitivitySubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);
    setSensitivityJobId(null);
    setSensitivityCompletedTime(null);

    // Quick validation
    const p = parseFloat(pfdGoal);
    const c = parseFloat(confidenceGoal);
    if (!Number.isFinite(p) || !Number.isFinite(c)) {
      setLoading(false);
      setErrorMsg("숫자를 정확히 입력하세요.");
      return;
    }

    try {
      // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
      // Test mode still makes actual API call but sends test_mode flag
      const jobResponse = await api.sensitivityAnalysis({
        pfd_goal: p,
        confidence_goal: c,
        trace_id: traceId ?? undefined,
        test_mode: testMode || undefined,
      });
      
      const jobId = jobResponse.job_id;
      setSensitivityJobId(jobId);
      setLoading(false);
      const jobStartTime = Date.now(); // Record job start time
      setIsPolling(true);
      setCurrentJobType('sensitivity-analysis');

      pollResults(
        jobId,
        'sensitivity-analysis',
        jobStartTime,
        (resultData: SensitivityAnalysisResult, _downloadUrl, elapsedSeconds) => {
          setTests(Number(resultData.data.num_tests));
          setErrorMsg(null);
          if (elapsedSeconds !== undefined) {
            setSensitivityCompletedTime(elapsedSeconds);
          }
        },
        (error) => {
          setErrorMsg(`Sensitivity Analysis 오류: ${error}`);
        }
      );
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Sensitivity Analysis 오류: ${err?.message ?? String(err)}`);
      setLoading(false);
    }
  };

  // 2) Update PFD
  const handlePfdUpdateSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);
    setUpdatePfdJobId(null);
    setUpdatePfdCompletedTime(null);

    const p = parseFloat(pfdGoal);
    if (!Number.isFinite(p)) {
      setLoading(false);
      setErrorMsg("PFD Goal을 숫자로 입력하세요.");
      return;
    }

    try {
      // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
      // Test mode still makes actual API call but sends test_mode flag
      const jobResponse = await api.updatePfd({
        pfd_goal: p,
        demand: tests,
        failures,
        trace_id: traceId ?? undefined,
        test_mode: testMode || undefined,
      });
      
      const jobId = jobResponse.job_id;
      setUpdatePfdJobId(jobId);
      setLoading(false);
      const jobStartTime = Date.now(); // Record job start time
      setIsPolling(true);
      setCurrentJobType('update-pfd');

      pollResults(
        jobId,
        'update-pfd',
        jobStartTime,
        (_data, _downloadUrl, elapsedSeconds) => {
          setErrorMsg(null);
          // Update PFD only needs success confirmation
          if (elapsedSeconds !== undefined) {
            setUpdatePfdCompletedTime(elapsedSeconds);
          }
        },
        (error) => {
          setErrorMsg(`Update PFD 오류: ${error}`);
        }
      );
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Update PFD 오류: ${err?.message ?? String(err)}`);
      setLoading(false);
    }
  };

  const handleFullAnalysisSubmit = async () => {
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);
    setFullAnalysisJobId(null);
    setFullAnalysisCompletedTime(null);

    const p = parseFloat(pfdGoal);
    const c = parseFloat(confidenceGoal);
    if (!Number.isFinite(p) || !Number.isFinite(c)) {
      setLoading(false);
      setErrorMsg("숫자를 정확히 입력하세요.");
      return;
    }

    try {
      // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
      // Test mode still makes actual API call but sends test_mode flag
      const jobResponse = await api.fullAnalysis({
        pfd_goal: p,
        confidence_goal: c,
        failures,
        trace_id: traceId ?? undefined,
        test_mode: testMode || undefined,
      });
      
      const jobId = jobResponse.job_id;
      setFullAnalysisJobId(jobId);
      setLoading(false);
      const jobStartTime = Date.now(); // Record job start time
      setIsPolling(true);
      setCurrentJobType('full-analysis');

      pollResults(
        jobId,
        'full-analysis',
        jobStartTime,
        (_, downloadUrl, elapsedSeconds) => {
          if (downloadUrl) {
            setDownloadLink(downloadUrl);
            setErrorMsg(null);
          }
          if (elapsedSeconds !== undefined) {
            setFullAnalysisCompletedTime(elapsedSeconds);
          }
        },
        (error) => {
          setErrorMsg(`Full Analysis 오류: ${error}`);
        }
      );
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Full Analysis 오류: ${err?.message ?? String(err)}`);
      setLoading(false);
    }
  };

  return (
    <>
      <Global styles={cssObj.globalStyles} />
      <div css={cssObj.pageWrapper}>
        <main css={cssObj.mainContent}>
          <section
            id="settings-title-section"
            css={[cssObj.container, cssObj.settingsTitleSection]}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h1 css={cssObj.title}>Statistical Methods</h1>
              {isDevelopment && (
                <div style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '12px' 
                }}>
                  <label style={{ 
                    color: '#000000', 
                    fontSize: '14px', 
                    fontWeight: '500', 
                    whiteSpace: 'nowrap',
                    cursor: 'pointer'
                  }}>
                    Test Mode (Use dummy data)
                  </label>
                  <input
                    type="checkbox"
                    checked={testMode}
                    onChange={(e) => setTestMode(e.target.checked)}
                    style={{
                      width: '16px',
                      height: '16px',
                      color: '#2563eb',
                      backgroundColor: '#f3f4f6',
                      borderColor: '#d1d5db',
                      borderRadius: '4px',
                      outline: 'none',
                      cursor: 'pointer'
                    }}
                  />
                </div>
              )}
            </div>
          </section>

          {(loading || isPolling) && (
            <div css={cssObj.container} style={{ marginTop: 8, marginBottom: 8 }}>
              <div style={{
                border: '1px solid #2563EB',
                borderRadius: '8px',
                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                padding: '16px',
                display: 'flex',
                flexDirection: 'column',
                gap: '8px'
              }}>
                <p style={{ margin: 0, fontSize: '14px', color: '#1F2937', fontWeight: loading ? 500 : 700 }}>
                  {loading ? '요청 중입니다...' : '계산 중입니다...'}
                </p>
                {!loading && isPolling && (
                  <div style={{ fontSize: '14px', color: '#1F2937' }}>
                    경과 시간: {formatElapsedTime(elapsedTime)}
                  </div>
                )}
              </div>
            </div>
          )}
          {errorMsg && (
            <div
              css={cssObj.container}
              style={{ marginTop: 8, color: "#d33" }}
            >
              <p>{errorMsg}</p>
            </div>
          )}

          <div css={cssObj.settingsGrid}>
            {/* 1. Sensitivity Analysis */}
            <div css={cssObj.settingBox}>
              <form onSubmit={handleSensitivitySubmit} css={cssObj.formWrapper}>
                <h2>1. Sensitivity Analysis</h2>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>PFD Goal</label>
                  <input
                    type="number"
                    step="any"
                    value={pfdGoal}
                    onChange={(e) => setPfdGoal(e.target.value)}
                    placeholder="예: 0.0001"
                    css={cssObj.inputBox}
                    required
                  />
                </div>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>Confidence Goal</label>
                  <input
                    type="number"
                    step="any"
                    value={confidenceGoal}
                    onChange={(e) => setConfidenceGoal(e.target.value)}
                    placeholder="예: 0.95"
                    css={cssObj.inputBox}
                    required
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <button 
                    type="submit" 
                    css={cssObj.saveButton} 
                    disabled={loading || isPolling || (sensitivityJobId !== null && currentJobType === 'sensitivity-analysis')}
                  >
                    {isPolling && currentJobType === 'sensitivity-analysis' ? '계산 중...' : 'Calculate Number of Tests'}
                  </button>
                  {sensitivityCompletedTime !== null && (
                    <span style={{ color: '#666', fontSize: '14px' }}>
                      ({formatElapsedTime(sensitivityCompletedTime)} 소요)
                    </span>
                  )}
                </div>

                {/* 결과 미니 표시 */}
                {tests > 0 && (
                  <div css={cssObj.output} style={{ marginTop: 12 }}>
                    계산된 <b>Number of Tests</b>: {tests}
                  </div>
                )}
              </form>
            </div>

            {/* 2. Update PFD */}
            <div css={cssObj.settingBox}>
              <form onSubmit={handlePfdUpdateSubmit} css={cssObj.formWrapper}>
                <h2>2. Update PFD</h2>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>Number of Tests</label>
                  <input
                    type="number"
                    value={tests}
                    onChange={(e) => setTests(Number(e.target.value))}
                    css={cssObj.inputBox}
                    min={1}
                    required
                  />
                </div>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>Number of Failures</label>
                  <input
                    type="number"
                    value={failures}
                    onChange={(e) => setFailures(Number(e.target.value))}
                    css={cssObj.inputBox}
                    min={0}
                    required
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <button 
                    type="submit" 
                    css={cssObj.saveButton} 
                    disabled={loading || isPolling || (updatePfdJobId !== null && currentJobType === 'update-pfd')}
                  >
                    {isPolling && currentJobType === 'update-pfd' ? '처리 중...' : 'Update'}
                  </button>
                  {updatePfdCompletedTime !== null && (
                    <span style={{ color: '#666', fontSize: '14px' }}>
                      ({formatElapsedTime(updatePfdCompletedTime)} 소요)
                    </span>
                  )}
                </div>
              </form>
            </div>

            {/* 3. Full Analysis */}
            <div css={[cssObj.settingBox, cssObj.longSettingBox]}>
              <h2>3. Full Analysis (Save JSON)</h2>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <button
                  css={cssObj.saveButton}
                  onClick={handleFullAnalysisSubmit}
                  disabled={loading || isPolling || (fullAnalysisJobId !== null && currentJobType === 'full-analysis')}
                >
                  {isPolling && currentJobType === 'full-analysis' ? '분석 중...' : 'Run Full Analysis and Save'}
                </button>
                {fullAnalysisCompletedTime !== null && (
                  <span style={{ color: '#666', fontSize: '14px' }}>
                    ({formatElapsedTime(fullAnalysisCompletedTime)} 소요)
                  </span>
                )}
              </div>

              {downloadLink && (
                <p css={cssObj.output} style={{ marginTop: 12 }}>
                  저장됨:&nbsp;
                  <a href={downloadLink} target="_blank" rel="noreferrer">
                    결과 JSON 다운로드
                  </a>
                </p>
              )}
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
