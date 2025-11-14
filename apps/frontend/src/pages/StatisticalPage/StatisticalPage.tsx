/** @jsxImportSource @emotion/react */
import { useState, useEffect, useRef, useCallback, type FormEvent } from "react";
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
  const [fullAnalysisResultData, setFullAnalysisResultData] = useState<any | null>(null);
  const [sensitivityJobId, setSensitivityJobId] = useState<string | null>(null);
  const [updatePfdJobId, setUpdatePfdJobId] = useState<string | null>(null);
  const [fullAnalysisJobId, setFullAnalysisJobId] = useState<string | null>(null);
  const [usedBbnInput, setUsedBbnInput] = useState<{ source: string; bucket?: string; key?: string; description?: string; size?: number; path?: string } | null>(null);
  const [usedBbnInputJobType, setUsedBbnInputJobType] = useState<'sensitivity-analysis' | 'update-pfd' | 'full-analysis' | null>(null);

  const [bbnFiles, setBbnFiles] = useState<api.BbnResultItem[]>([]);
  const [bbnBucketInfo, setBbnBucketInfo] = useState<{ bucket: string; prefix: string } | null>(null);
  const [bbnFilesLoading, setBbnFilesLoading] = useState<boolean>(false);
  const [bbnFilesError, setBbnFilesError] = useState<string | null>(null);
  const [bbnLastRefreshed, setBbnLastRefreshed] = useState<Date | null>(null);
  const [selectedBbnKey, setSelectedBbnKey] = useState<string>("");
  const [selectedBbnData, setSelectedBbnData] = useState<any | null>(null);
  const [bbnFileLoading, setBbnFileLoading] = useState<boolean>(false);
  const [bbnFileMessage, setBbnFileMessage] = useState<string | null>(null);

  const [isPolling, setIsPolling] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0); // Elapsed time in seconds
  const [currentJobType, setCurrentJobType] = useState<'sensitivity-analysis' | 'update-pfd' | 'full-analysis' | null>(null);
  const isDevelopment = import.meta.env.DEV;
  const [testMode, setTestMode] = useState(isDevelopment); // Test mode (default true in development, only enabled in development)
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

  const refreshBbnFiles = useCallback(async () => {
    setBbnFilesLoading(true);
    setBbnFilesError(null);
    try {
      const response = await api.listBbnResultFiles(200);
      setBbnFiles(response.items ?? []);
      setBbnBucketInfo({ bucket: response.bucket, prefix: response.prefix });
      setBbnLastRefreshed(new Date());

      if (selectedBbnKey) {
        const exists = (response.items ?? []).some((item) => item.key === selectedBbnKey);
        if (!exists) {
          setSelectedBbnKey("");
          setSelectedBbnData(null);
          setBbnFileMessage(null);
        }
      }
    } catch (err: any) {
      console.error("Failed to load BBN result files:", err);
      setBbnFilesError(err?.message ?? String(err));
    } finally {
      setBbnFilesLoading(false);
    }
  }, [selectedBbnKey]);

  useEffect(() => {
    refreshBbnFiles();
  }, [refreshBbnFiles]);

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
              let resultData = response.data;
              if (type === 'full-analysis' && !downloadUrl && response.data) {
                // Create blob URL on frontend
                const jsonStr = JSON.stringify(response.data, null, 2);
                const blob = new Blob([jsonStr], { type: 'application/json' });
                downloadUrl = URL.createObjectURL(blob);
                resultData = response.data; // Store the data for viewing/downloading
              }
              onComplete(resultData, downloadUrl, completedElapsedTime);
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

  const formatBytes = (size?: number): string => {
    if (typeof size !== "number" || Number.isNaN(size) || size < 0) {
      return "-";
    }
    if (size < 1024) {
      return `${size} B`;
    }
    const units = ["KB", "MB", "GB", "TB"];
    let value = size / 1024;
    let unitIndex = 0;
    while (value >= 1024 && unitIndex < units.length - 1) {
      value /= 1024;
      unitIndex += 1;
    }
    return `${value.toFixed(1)} ${units[unitIndex]}`;
  };

  const formatTimestamp = (value?: string | Date | null): string => {
    if (!value) {
      return "-";
    }
    const date = value instanceof Date ? value : new Date(value);
    if (Number.isNaN(date.getTime())) {
      return typeof value === "string" ? value : "-";
    }
    return date.toLocaleString();
  };

  const formatFileLabel = (item: api.BbnResultItem): string => {
    const parts = [item.name];
    if (item.last_modified) {
      parts.push(formatTimestamp(item.last_modified));
    }
    if (typeof item.size === "number") {
      parts.push(formatBytes(item.size));
    }
    return parts.join(" • ");
  };

  const handleSelectBbnFile = async (key: string) => {
    setSelectedBbnKey(key);
    setSelectedBbnData(null);
    setBbnFileMessage(null);

    if (!key) {
      return;
    }

    setBbnFileLoading(true);
    try {
      const response = await api.fetchBbnResultFile(key);
      setSelectedBbnData(response.data);
    } catch (err: any) {
      console.error("Failed to load selected BBN file:", err);
      setBbnFileMessage(err?.message ?? String(err));
    } finally {
      setBbnFileLoading(false);
    }
  };

  const handleViewSelectedBbnData = () => {
    if (!selectedBbnData) return;
    const jsonStr = JSON.stringify(selectedBbnData, null, 2);
    const newWindow = window.open();
    if (newWindow) {
      newWindow.document.write(
        `<pre style="padding: 20px; font-family: monospace; white-space: pre-wrap; word-wrap: break-word;">${jsonStr}</pre>`
      );
      newWindow.document.title = "BBN 결과";
    }
  };

  const handleDownloadSelectedBbnData = () => {
    if (!selectedBbnData) return;
    const jsonStr = JSON.stringify(selectedBbnData, null, 2);
    const blob = new Blob([jsonStr], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const fileName = selectedBbnKey ? selectedBbnKey.split("/").pop() : `bbn-result-${Date.now()}.json`;
    link.href = url;
    link.download = fileName ?? `bbn-result-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const selectedBbnMeta = selectedBbnKey
    ? bbnFiles.find((item) => item.key === selectedBbnKey)
    : undefined;

  const buildBbnPayload = useCallback(() => {
    // 선택된 BBN 파일이 있으면 S3 경로 전달
    if (selectedBbnKey && selectedBbnKey.trim() && bbnBucketInfo?.bucket) {
      const payload = {
        bbn_input_s3_bucket: bbnBucketInfo.bucket,
        bbn_input_s3_key: selectedBbnKey,
      };
      console.log('[BBN Payload] S3 path will be sent:', payload);
      return payload;
    }
    console.log('[BBN Payload] No BBN file selected, using default');
    return {};
  }, [selectedBbnKey, bbnBucketInfo]);

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
        ...buildBbnPayload(),
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
          // Extract BBN input info from result
          if (resultData && (resultData as any).bbn_input) {
            setUsedBbnInput((resultData as any).bbn_input);
          } else {
            setUsedBbnInput({ source: 'default', description: 'NRC report data (default)' });
          }
          setUsedBbnInputJobType('sensitivity-analysis');
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
        ...buildBbnPayload(),
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
          // Extract BBN input info from result
          if (_data && _data.bbn_input) {
            setUsedBbnInput(_data.bbn_input);
          } else {
            setUsedBbnInput({ source: 'default', description: 'NRC report data (default)' });
          }
          setUsedBbnInputJobType('update-pfd');
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
    setFullAnalysisResultData(null);
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
        ...buildBbnPayload(),
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
        (resultData, downloadUrl, elapsedSeconds) => {
          if (resultData) {
            setFullAnalysisResultData(resultData);
            // Extract BBN input info from result
            if (resultData.input && resultData.input.bbn_input) {
              setUsedBbnInput(resultData.input.bbn_input);
            } else {
              setUsedBbnInput({ source: 'default', description: 'NRC report data (default)' });
            }
            setUsedBbnInputJobType('full-analysis');
          }
          if (downloadUrl) {
            setDownloadLink(downloadUrl);
          }
          setErrorMsg(null);
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

        <div css={cssObj.bbnSelectorBox}>
          <div css={cssObj.bbnSelectorHeader}>
            <div>
              <h2>BBN JSON Result Selection</h2>
              <p>
                {bbnBucketInfo
                  ? `${bbnBucketInfo.bucket}/${bbnBucketInfo.prefix ?? ""}`
                  : "버킷 정보를 불러오는 중입니다."}
                {bbnBucketInfo && (
                  <>
                    {bbnLastRefreshed && (
                      <span style={{ marginLeft: 8 }}>
                        · 갱신: {formatTimestamp(bbnLastRefreshed)}
                      </span>
                    )}
                    <span style={{ marginLeft: 8 }}>
                      · 총 {bbnFiles.length.toLocaleString()}건
                    </span>
                  </>
                )}
              </p>
            </div>
            <button
              type="button"
              css={cssObj.bbnRefreshButton}
              onClick={refreshBbnFiles}
              disabled={bbnFilesLoading}
            >
              {bbnFilesLoading ? "불러오는 중..." : "목록 새로고침"}
            </button>
          </div>

          <select
            css={cssObj.bbnSelect}
            value={selectedBbnKey}
            onChange={(e) => handleSelectBbnFile(e.target.value)}
            disabled={bbnFilesLoading || bbnFiles.length === 0}
          >
            <option value="">파일을 선택하세요</option>
            {bbnFiles.map((item) => (
              <option key={item.key} value={item.key}>
                {formatFileLabel(item)}
              </option>
            ))}
          </select>

          {bbnFilesError && (
            <span css={cssObj.bbnErrorText}>
              목록을 불러오는 데 실패했습니다: {bbnFilesError}
            </span>
          )}

          {!bbnFilesLoading && bbnFiles.length === 0 && !bbnFilesError && (
            <span css={cssObj.bbnMessage}>표시할 JSON 파일이 없습니다.</span>
          )}

          {selectedBbnMeta && (
            <div css={cssObj.bbnMetaInfo}>
              <span>파일명: {selectedBbnMeta.name}</span>
              {typeof selectedBbnMeta.size === "number" && (
                <span>크기: {formatBytes(selectedBbnMeta.size)}</span>
              )}
              {selectedBbnMeta.last_modified && (
                <span>수정: {formatTimestamp(selectedBbnMeta.last_modified)}</span>
              )}
            </div>
          )}

          {bbnFileLoading && (
            <span css={cssObj.bbnMessage}>선택한 파일을 불러오는 중입니다...</span>
          )}

          {bbnFileMessage && <span css={cssObj.bbnErrorText}>{bbnFileMessage}</span>}

          {selectedBbnData && !bbnFileLoading && (
            <div css={cssObj.bbnActionRow}>
              <button
                type="button"
                css={[cssObj.bbnButton, cssObj.bbnPrimaryButton]}
                onClick={handleViewSelectedBbnData}
              >
                결과보기
              </button>
              <button
                type="button"
                css={[cssObj.bbnButton, cssObj.bbnSecondaryButton]}
                onClick={handleDownloadSelectedBbnData}
              >
                다운로드
              </button>
            </div>
          )}
        </div>

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
                {/* 사용된 BBN 입력 정보 표시 */}
                {usedBbnInput && usedBbnInputJobType === 'sensitivity-analysis' && (
                  <div style={{ marginTop: 12, padding: '12px', backgroundColor: '#eff6ff', border: '1px solid #3b82f6', borderRadius: '6px', fontSize: '13px', color: '#1e40af' }}>
                    <div style={{ fontWeight: '600', marginBottom: '4px' }}>사용된 BBN 입력:</div>
                    <div style={{ color: '#374151' }}>
                      {usedBbnInput.source === 's3' 
                        ? `S3: ${usedBbnInput.bucket}/${usedBbnInput.key}`
                        : usedBbnInput.source === 'default'
                        ? usedBbnInput.description || '기본값 (NRC report data)'
                        : usedBbnInput.source === 'inline'
                        ? `인라인 JSON (${usedBbnInput.size} bytes)`
                        : `로컬 파일: ${usedBbnInput.path}`
                      }
                    </div>
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
                {/* 사용된 BBN 입력 정보 표시 */}
                {usedBbnInput && usedBbnInputJobType === 'update-pfd' && (
                  <div style={{ marginTop: 12, padding: '12px', backgroundColor: '#eff6ff', border: '1px solid #3b82f6', borderRadius: '6px', fontSize: '13px', color: '#1e40af' }}>
                    <div style={{ fontWeight: '600', marginBottom: '4px' }}>사용된 BBN 입력:</div>
                    <div style={{ color: '#374151' }}>
                      {usedBbnInput.source === 's3' 
                        ? `S3: ${usedBbnInput.bucket}/${usedBbnInput.key}`
                        : usedBbnInput.source === 'default'
                        ? usedBbnInput.description || '기본값 (NRC report data)'
                        : usedBbnInput.source === 'inline'
                        ? `인라인 JSON (${usedBbnInput.size} bytes)`
                        : `로컬 파일: ${usedBbnInput.path}`
                      }
                    </div>
                  </div>
                )}
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

              {(fullAnalysisResultData || downloadLink) && (
                <div css={cssObj.output} style={{ marginTop: 12, display: 'flex', gap: '12px', alignItems: 'center' }}>
                  <span style={{ color: '#666', fontSize: '14px' }}>결과:</span>
                  {fullAnalysisResultData && (
                    <>
                      <button
                        onClick={() => {
                          const jsonStr = JSON.stringify(fullAnalysisResultData, null, 2);
                          const newWindow = window.open();
                          if (newWindow) {
                            newWindow.document.write(`<pre style="padding: 20px; font-family: monospace; white-space: pre-wrap; word-wrap: break-word;">${jsonStr}</pre>`);
                            newWindow.document.title = 'Full Analysis 결과';
                          }
                        }}
                        style={{
                          padding: '6px 12px',
                          backgroundColor: '#2563EB',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '500'
                        }}
                      >
                        결과보기
                      </button>
                      <button
                        onClick={() => {
                          const jsonStr = JSON.stringify(fullAnalysisResultData, null, 2);
                          const blob = new Blob([jsonStr], { type: 'application/json' });
                          const url = URL.createObjectURL(blob);
                          const link = document.createElement('a');
                          link.href = url;
                          link.download = `full-analysis-result-${Date.now()}.json`;
                          document.body.appendChild(link);
                          link.click();
                          document.body.removeChild(link);
                          URL.revokeObjectURL(url);
                        }}
                        style={{
                          padding: '6px 12px',
                          backgroundColor: '#10B981',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontSize: '14px',
                          fontWeight: '500'
                        }}
                      >
                        다운로드
                      </button>
                    </>
                  )}
                  {downloadLink && !fullAnalysisResultData && (
                    <a 
                      href={downloadLink} 
                      target="_blank" 
                      rel="noreferrer"
                      style={{
                        padding: '6px 12px',
                        backgroundColor: '#2563EB',
                        color: '#FFFFFF',
                        textDecoration: 'none',
                        borderRadius: '6px',
                        fontSize: '14px',
                        fontWeight: '500',
                        display: 'inline-block'
                      }}
                    >
                      결과보기
                    </a>
                  )}
                </div>
              )}
              {/* 사용된 BBN 입력 정보 표시 */}
              {usedBbnInput && usedBbnInputJobType === 'full-analysis' && (
                <div style={{ marginTop: 12, padding: '12px', backgroundColor: '#eff6ff', border: '1px solid #3b82f6', borderRadius: '6px', fontSize: '13px', color: '#1e40af' }}>
                  <div style={{ fontWeight: '600', marginBottom: '4px' }}>사용된 BBN 입력:</div>
                  <div style={{ color: '#374151' }}>
                    {usedBbnInput.source === 's3' 
                      ? `S3: ${usedBbnInput.bucket}/${usedBbnInput.key}`
                      : usedBbnInput.source === 'default'
                      ? usedBbnInput.description || '기본값 (NRC report data)'
                      : usedBbnInput.source === 'inline'
                      ? `인라인 JSON (${usedBbnInput.size} bytes)`
                      : `로컬 파일: ${usedBbnInput.path}`
                    }
                  </div>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </>
  );
}
