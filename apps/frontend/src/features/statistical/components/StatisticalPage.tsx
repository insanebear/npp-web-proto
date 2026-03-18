/** @jsxImportSource @emotion/react */
import { useState, useEffect, useRef, useCallback, type FormEvent } from "react";
import { Global } from "@emotion/react";
import { cssObj } from "./style";
import * as api from "../../../shared/services/apiService";
import type { SensitivityAnalysisResult } from "../../../shared/services/apiService";
import { useAppSettings } from '../../../shared/hooks/useAppSettings';

// Polling configuration
const POLL_INTERVAL = 5000; // 5 seconds
const MAX_WAIT_TIME = 1200000; // 20 minutes (milliseconds)
const MAX_ATTEMPTS = 240; // Maximum 240 attempts (20 minutes / 5 seconds)

export default function StatisticalPage() {
  const settings = useAppSettings();
  const [pfdGoal, setPfdGoal] = useState("");
  const [confidenceGoal, setConfidenceGoal] = useState("");
  // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture, maintained for compatibility)
  const [traceId, _setTraceId] = useState<string | null>(null);
  const [tests, setTests] = useState<number | null>(null);
  const [failures, setFailures] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [downloadLink, setDownloadLink] = useState<string | null>(null);
  const [fullAnalysisResultData, setFullAnalysisResultData] = useState<any | null>(null);
  const [sensitivityJobId, setSensitivityJobId] = useState<string | null>(null);
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
  const [fullAnalysisCompletedTime, setFullAnalysisCompletedTime] = useState<number | null>(null);
  const elapsedTimerRef = useRef<NodeJS.Timeout | null>(null);
  const pollingRef = useRef<{ jobId: string; type: string; attempts: number; startTime: number } | null>(null);

  // Number of Tests lock/unlock state
  const [isNumOfTestsLocked, setIsNumOfTestsLocked] = useState<boolean>(true);
  const [sensitivityTests, setSensitivityTests] = useState<number | null>(null);


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
        // Check job status from DynamoDB (same approach as OpenBUGS_BBN)
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

  const handleViewFullAnalysisJson = () => {
    if (!fullAnalysisResultData) return;
    const jsonStr = JSON.stringify(fullAnalysisResultData, null, 2);
    const newWindow = window.open();
    if (newWindow) {
      newWindow.document.write(
        `<pre style="padding: 20px; font-family: monospace; white-space: pre-wrap; word-wrap: break-word;">${jsonStr}</pre>`
      );
      newWindow.document.title = 'Full Analysis 결과';
    }
  };

  const handleDownloadFullAnalysisJson = () => {
    if (!fullAnalysisResultData) return;
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

  // 1) Sensitivity Analysis
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
        settings: {
          draws: settings.nIter - settings.nBurnin,
          tune: settings.nBurnin,
          chains: settings.nChains,
          thin: settings.nThin,
        },
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
          const numTests = Number(resultData.data.num_tests);
          setTests(numTests);
          setSensitivityTests(numTests);
          setIsNumOfTestsLocked(true);
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


  // 3) Full Analysis
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

    // Sensitivity Analysis 실행 여부 확인
    if (tests === null || tests === 0) {
      setLoading(false);
      setErrorMsg("Full Analysis를 실행하기 전에 Sensitivity Analysis를 먼저 실행해주세요.");
      return;
    }

    // Failures 값 확인
    if (failures === null) {
      setLoading(false);
      setErrorMsg("Failures 값을 입력해주세요.");
      return;
    }

    try {
      // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
      // Test mode still makes actual API call but sends test_mode flag
      const jobResponse = await api.fullAnalysis({
        pfd_goal: p,
        confidence_goal: c,
        failures,
        demand_required: tests > 0 ? tests : undefined,
        trace_id: traceId ?? undefined,
        test_mode: testMode || undefined,
        ...buildBbnPayload(),
        settings: {
          draws: settings.nIter - settings.nBurnin,
          tune: settings.nBurnin,
          chains: settings.nChains,
          thin: settings.nThin,
        },
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

          {/* BBN JSON Result Selection */}
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

          {/* 3-column grid */}
          <div css={cssObj.settingsGrid}>

            {/* 1. Sensitivity Analysis */}
            <div css={cssObj.settingBox}>
              <form onSubmit={handleSensitivitySubmit} css={cssObj.formWrapper}>
                <h2>1. Sensitivity analysis</h2>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>PFD goal</label>
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
                  <label css={cssObj.inputLabel}>Confidence goal</label>
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
                    {isPolling && currentJobType === 'sensitivity-analysis' ? '계산 중...' : 'Calculate'}
                  </button>
                  {sensitivityCompletedTime !== null && (
                    <span style={{ color: '#666', fontSize: '13px' }}>
                      ({formatElapsedTime(sensitivityCompletedTime)} 소요)
                    </span>
                  )}
                </div>
                <div css={cssObj.outputBox}>
                  <span css={cssObj.outputLabel}>Required # of tests</span>
                  <span css={cssObj.outputValue}>
                    {tests !== null && tests > 0 ? tests : '—'}
                  </span>
                </div>
              </form>
            </div>

            {/* 2. Bayesian Update */}
            <div css={cssObj.settingBox}>
              <form onSubmit={(e) => { e.preventDefault(); handleFullAnalysisSubmit(); }} css={cssObj.formWrapper}>
                <h2>2. Bayesian update</h2>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>Number of tests</label>
                  <div css={cssObj.lockedInputRow}>
                    <div css={cssObj.lockedInputWrapper}>
                      <input
                        type="number"
                        value={tests ?? ''}
                        onChange={(e) => {
                          if (!isNumOfTestsLocked) {
                            const value = e.target.value;
                            setTests(value === '' ? null : Number(value));
                          }
                        }}
                        readOnly={isNumOfTestsLocked}
                        placeholder="정수 입력"
                        css={[cssObj.inputBox, isNumOfTestsLocked ? cssObj.lockedInputBox : null]}
                        min={1}
                      />
                      {isNumOfTestsLocked && (
                        <span css={cssObj.lockIcon}>🔒</span>
                      )}
                    </div>
                    {isNumOfTestsLocked ? (
                      <button
                        type="button"
                        css={cssObj.lockBtn}
                        onClick={() => setIsNumOfTestsLocked(false)}
                      >
                        직접 입력
                      </button>
                    ) : (
                      <button
                        type="button"
                        css={cssObj.restoreBtn}
                        onClick={() => {
                          setIsNumOfTestsLocked(true);
                          setTests(sensitivityTests);
                        }}
                      >
                        자동 입력 복원
                      </button>
                    )}
                  </div>
                  <span css={isNumOfTestsLocked ? cssObj.hintText : cssObj.warningHintText}>
                    {isNumOfTestsLocked
                      ? '1번 Sensitivity analysis 결과에서 자동 입력됩니다.'
                      : '1번 Sensitivity analysis 결과와 무관하게 입력된 값으로 실행됩니다'}
                  </span>
                </div>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>Number of failures</label>
                  <input
                    type="number"
                    value={failures ?? ''}
                    onChange={(e) => {
                      const value = e.target.value;
                      setFailures(value === '' ? null : Number(value));
                    }}
                    placeholder="정수 입력"
                    css={cssObj.inputBox}
                    min={0}
                    required
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <button
                    type="submit"
                    css={cssObj.saveButton}
                    disabled={loading || isPolling || (fullAnalysisJobId !== null && currentJobType === 'full-analysis')}
                  >
                    {isPolling && currentJobType === 'full-analysis' ? '분석 중...' : 'Run update'}
                  </button>
                  {fullAnalysisCompletedTime !== null && (
                    <span style={{ color: '#666', fontSize: '13px' }}>
                      ({formatElapsedTime(fullAnalysisCompletedTime!)} 소요)
                    </span>
                  )}
                </div>
                <p css={cssObj.sectionDescription}>
                  테스트 결과를 바탕으로 사전 PFD를 베이지안 방식으로 갱신하여 분석합니다.
                </p>
              </form>
            </div>

            {/* 3. Result Summary */}
            <div css={cssObj.settingBox}>
              <div css={cssObj.resultSummaryHeader}>
                <span>Result summary</span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <button
                    css={cssObj.jsonDownloadBtn}
                    onClick={handleViewFullAnalysisJson}
                    disabled={!fullAnalysisResultData}
                    title="새 탭에서 결과 보기"
                  >
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
                      <path d="M7 2.5C4.5 2.5 2.5 4.5 2.5 7C2.5 9.5 4.5 11.5 7 11.5C9.5 11.5 11.5 9.5 11.5 7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
                      <path d="M9 1.5H12.5V5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M12.5 1.5L7.5 6.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
                    </svg>
                  </button>
                  <button
                    css={cssObj.jsonDownloadBtn}
                    onClick={handleDownloadFullAnalysisJson}
                    disabled={!fullAnalysisResultData}
                    title="JSON 다운로드"
                  >
                    ↓ JSON
                  </button>
                </div>
              </div>
              <div css={cssObj.resultCardGrid}>
                <div css={[cssObj.resultCard, { gridColumn: '1 / -1' }]}>
                  <span css={cssObj.resultCardLabel}>Prior PFD</span>
                  <span css={cssObj.resultCardValue}>
                    {fullAnalysisResultData?.input?.parameter?.prior?.mean != null
                      ? fullAnalysisResultData.input.parameter.prior.mean.toExponential(4)
                      : '—'}
                  </span>
                </div>
                <div css={cssObj.resultCard}>
                  <span css={cssObj.resultCardLabel}>Updated PFD</span>
                  <span css={cssObj.resultCardValue}>
                    {fullAnalysisResultData?.output?.mean_posterior_pfd?.[0]?.[1] != null
                      ? fullAnalysisResultData.output.mean_posterior_pfd[0][1].toExponential(4)
                      : '—'}
                  </span>
                </div>
                <div css={cssObj.resultCard}>
                  <span css={cssObj.resultCardLabel}>Confidence</span>
                  <span css={cssObj.resultCardValue}>
                    {fullAnalysisResultData?.output?.confidence != null
                      ? (fullAnalysisResultData.output.confidence * 100).toFixed(1) + '%'
                      : '—'}
                  </span>
                </div>
              </div>
            </div>

          </div>

          {/* Footer note */}
          <div css={cssObj.footerNote}>
            각 섹션을 순서대로 실행하거나 독립적으로 사용할 수 있습니다.
          </div>

        </main>
      </div>
    </>
  );
}
