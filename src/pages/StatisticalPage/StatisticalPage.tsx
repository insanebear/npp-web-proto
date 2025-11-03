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
    onComplete: (data: any, downloadUrl?: string) => void,
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
              onComplete(response.data, downloadUrl);
            } else if (response.download_url) {
              // Maintain compatibility with legacy approach
              setIsPolling(false);
              setCurrentJobType(null);
              onComplete(null, response.download_url);
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

  // Estimate remaining time (simple linear estimation)
  const estimateRemainingTime = (): string | null => {
    if (!isPolling || elapsedTime < 10) return null; // Start estimation after minimum 10 seconds
    // sensitivity-analysis usually takes 1-2 minutes, full-analysis takes 5-10 minutes
    // Assume average 3 minutes (could be improved with history-based estimation)
    const avgTime = currentJobType === 'full-analysis' ? 300 : 120; // full: 5 min, others: 2 min
    const remaining = Math.max(0, avgTime - elapsedTime);
    if (remaining < 30) return null; // Don't display if less than 30 seconds remaining
    return formatElapsedTime(remaining);
  };

  const handleSensitivitySubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);
    setSensitivityJobId(null);

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
      setIsPolling(true);
      setCurrentJobType('sensitivity-analysis');

      pollResults(
        jobId,
        'sensitivity-analysis',
        (resultData: SensitivityAnalysisResult) => {
          setTests(Number(resultData.data.num_tests));
          setErrorMsg(null);
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
      setIsPolling(true);
      setCurrentJobType('update-pfd');

      pollResults(
        jobId,
        'update-pfd',
        () => {
          setErrorMsg(null);
          // Update PFD only needs success confirmation
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
      setIsPolling(true);
      setCurrentJobType('full-analysis');

      pollResults(
        jobId,
        'full-analysis',
        (_, downloadUrl) => {
          if (downloadUrl) {
            setDownloadLink(downloadUrl);
            setErrorMsg(null);
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
            <div css={cssObj.container} style={{ marginTop: 8 }}>
              <p>
                {loading ? '요청 중입니다...' : '계산 중입니다...'}
              </p>
              {isPolling && (
                <div style={{ marginTop: 8, fontSize: '14px', color: '#666' }}>
                  <div>경과 시간: {formatElapsedTime(elapsedTime)}</div>
                  {estimateRemainingTime() && (
                    <div style={{ marginTop: 4 }}>
                      예상 남은 시간: 약 {estimateRemainingTime()}
                    </div>
                  )}
                </div>
              )}
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
                <button 
                  type="submit" 
                  css={cssObj.saveButton} 
                  disabled={loading || isPolling || (sensitivityJobId !== null && currentJobType === 'sensitivity-analysis')}
                >
                  {isPolling && currentJobType === 'sensitivity-analysis' ? '계산 중...' : 'Calculate Number of Tests'}
                </button>

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
                <button 
                  type="submit" 
                  css={cssObj.saveButton} 
                  disabled={loading || isPolling || (updatePfdJobId !== null && currentJobType === 'update-pfd')}
                >
                  {isPolling && currentJobType === 'update-pfd' ? '처리 중...' : 'Update'}
                </button>
              </form>
            </div>

            {/* 3. Full Analysis */}
            <div css={[cssObj.settingBox, cssObj.longSettingBox]}>
              <h2>3. Full Analysis (Save JSON)</h2>
              <button
                css={cssObj.saveButton}
                onClick={handleFullAnalysisSubmit}
                disabled={loading || isPolling || (fullAnalysisJobId !== null && currentJobType === 'full-analysis')}
              >
                {isPolling && currentJobType === 'full-analysis' ? '분석 중...' : 'Run Full Analysis and Save'}
              </button>

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
