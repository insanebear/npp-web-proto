/** @jsxImportSource @emotion/react */
import { useState, useEffect, useRef, useCallback, type FormEvent } from "react";
import { Global } from "@emotion/react";
import { cssObj } from "./style";
import * as api from "../../../shared/services/apiService";
import type { SensitivityAnalysisResult } from "../../../shared/services/apiService";
import { useAppSettings } from '../../../shared/hooks/useAppSettings';

type BbnTab = 'select' | 'upload';

// Polling configuration
const POLL_INTERVAL = 5000; // 5 seconds
const MAX_WAIT_TIME = 7_200_000; // 120 minutes (milliseconds)
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
  const [pfdUpdateResultData, setPfdUpdateResultData] = useState<any | null>(null);
  const [sensitivityJobId, setSensitivityJobId] = useState<string | null>(null);
  const [pfdUpdateJobId, setPfdUpdateJobId] = useState<string | null>(null);

  // BBN selector tab
  const [bbnTab, setBbnTab] = useState<BbnTab>('select');

  // Upload tab state
  const [uploadedJsonKey, setUploadedJsonKey] = useState<string | null>(null);
  const [uploadedNcKey, setUploadedNcKey] = useState<string | null>(null);
  const [uploadedBucket, setUploadedBucket] = useState<string | null>(null);
  const [jsonUploading, setJsonUploading] = useState(false);
  const [ncUploading, setNcUploading] = useState(false);
  const [jsonUploadError, setJsonUploadError] = useState<string | null>(null);
  const [ncUploadError, setNcUploadError] = useState<string | null>(null);
  const [uploadedJsonName, setUploadedJsonName] = useState<string | null>(null);
  const [uploadedNcName, setUploadedNcName] = useState<string | null>(null);
  const [uploadedJsonSettings, setUploadedJsonSettings] = useState<{ nChains: string; nIter: string; nBurnin: string; nThin: string } | null>(null);
  const [editedUploadSettings, setEditedUploadSettings] = useState<{ nChains: string; nIter: string; nBurnin: string; nThin: string } | null>(null);
  const [editedSelectSettings, setEditedSelectSettings] = useState<{ nChains: string; nIter: string; nBurnin: string; nThin: string } | null>(null);
  const [isHyperparamModalOpen, setIsHyperparamModalOpen] = useState(false);
  const [hyperparamModalTarget, setHyperparamModalTarget] = useState<'upload' | 'select'>('upload');
  const [modalDraft, setModalDraft] = useState<{ nChains: string; nIter: string; nBurnin: string; nThin: string }>({ nChains: '', nIter: '', nBurnin: '', nThin: '' });

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
  // TODO: Replace 'full-analysis' with 'pfd-update' once backend renames the task type string.
  const [currentJobType, setCurrentJobType] = useState<'sensitivity-analysis' | 'full-analysis' | null>(null);
  const isDevelopment = import.meta.env.DEV;
  const [testMode, setTestMode] = useState(isDevelopment); // Test mode (default true in development, only enabled in development)
  const [sensitivityCompletedTime, setSensitivityCompletedTime] = useState<number | null>(null);
  const [pfdUpdateCompletedTime, setPfdUpdateCompletedTime] = useState<number | null>(null);
  const [pfdUpdateUsedDefaultBbn, setPfdUpdateUsedDefaultBbn] = useState<boolean>(false);
  const elapsedTimerRef = useRef<NodeJS.Timeout | null>(null);
  const pollingRef = useRef<{ jobId: string; type: string; attempts: number; startTime: number } | null>(null);
  const jsonFileInputRef = useRef<HTMLInputElement>(null);
  const ncFileInputRef = useRef<HTMLInputElement>(null);

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
      const items = response.items ?? [];
      
      // 최신 생성된 파일이 먼저 오도록 정렬 (last_modified 기준 내림차순)
      const sortedItems = [...items].sort((a, b) => {
        // last_modified가 없는 항목은 뒤로
        if (!a.last_modified && !b.last_modified) return 0;
        if (!a.last_modified) return 1;
        if (!b.last_modified) return -1;
        
        // 최신 파일이 먼저 오도록 내림차순 정렬
        const dateA = new Date(a.last_modified).getTime();
        const dateB = new Date(b.last_modified).getTime();
        return dateB - dateA;
      });
      
      setBbnFiles(sortedItems);
      setBbnBucketInfo({ bucket: response.bucket, prefix: response.prefix });
      setBbnLastRefreshed(new Date());

      if (selectedBbnKey) {
        const exists = sortedItems.some((item) => item.key === selectedBbnKey);
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
    type: 'sensitivity-analysis' | 'full-analysis',
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
        onError('Result retrieval timed out. Please try again later.');
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
              onError('Job completed but no results were found.');
            }
          } else {
            // Failed to fetch results
            setIsPolling(false);
            setCurrentJobType(null);
            onError(response.message || 'Failed to retrieve results');
          }
          return;
        } else if (statusData.jobStatus === 'FAILED') {
          // Job failed → immediate error handling
          setIsPolling(false);
          setCurrentJobType(null);
          onError(statusData.errorMessage || 'Job failed.');
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
          onError(`Server error: ${errorMessage}. Result retrieval stopped.`);
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
          onError('Result retrieval timed out. Please try again later.');
        }
      }
    };

    poll();
  };

  // Format elapsed time (seconds → "mm:ss" or "X minutes Y seconds")
  const formatElapsedTime = (seconds: number): string => {
    if (seconds < 60) {
      return `${seconds}s`;
    }
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
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
      setEditedSelectSettings(null);
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
      newWindow.document.title = "BBN Result";
    }
  };

  const handleDownloadSelectedBbnData = async () => {
    if (!selectedBbnData) return;

    // Download JSON
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

    // Download matching NC trace file
    // JSON key pattern: results/bbn/results-{jobId}.json → NC key: results/bbn/prior-trace-{jobId}.nc
    if (selectedBbnKey) {
      const match = selectedBbnKey.match(/results-([^/]+)\.json$/);
      if (match) {
        const jobId = match[1];
        const ncKey = `results/bbn/prior-trace-${jobId}.nc`;
        try {
          const { download_url } = await api.getDownloadPresignedUrl(ncKey);
          const ncLink = document.createElement("a");
          ncLink.href = download_url;
          ncLink.download = `prior-trace-${jobId}.nc`;
          document.body.appendChild(ncLink);
          ncLink.click();
          document.body.removeChild(ncLink);
        } catch (err) {
          console.warn("NC trace file not available:", err);
        }
      }
    }
  };

  const handleViewPfdUpdateJson = () => {
    if (!pfdUpdateResultData) return;
    const jsonStr = JSON.stringify(pfdUpdateResultData, null, 2);
    const newWindow = window.open();
    if (newWindow) {
      newWindow.document.write(
        `<pre style="padding: 20px; font-family: monospace; white-space: pre-wrap; word-wrap: break-word;">${jsonStr}</pre>`
      );
      newWindow.document.title = 'PFD Update Result';
    }
  };

  const handleDownloadPfdUpdateJson = () => {
    if (!pfdUpdateResultData) return;
    const jsonStr = JSON.stringify(pfdUpdateResultData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `pfd-update-result-${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };


  const selectedBbnMeta = selectedBbnKey
    ? bbnFiles.find((item) => item.key === selectedBbnKey)
    : undefined;

  const renderHyperparamInfo = (s: { nChains: string; nIter: string; nBurnin: string; nThin: string }) => (
    <div style={{ marginTop: '8px' }}>
      <div style={{ fontSize: '13px', color: '#374151', display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
        <span>Chains: <strong>{s.nChains}</strong></span>
        <span>Iterations: <strong>{s.nIter}</strong></span>
        <span>Burn-in: <strong>{s.nBurnin}</strong></span>
        <span>Thin: <strong>{s.nThin}</strong></span>
      </div>
      <p style={{ margin: '4px 0 0', fontSize: '12px', color: '#6B7280' }}>
        These hyperparameters from the BBN analysis will be applied through to the final target reliability assessment.
      </p>
    </div>
  );

  const buildBbnPayload = useCallback(() => {
    if (bbnTab === 'upload') {
      // Upload tab: use uploaded file S3 keys
      if (uploadedJsonKey && uploadedNcKey && uploadedBucket) {
        const payload = {
          bbn_input_s3_bucket: uploadedBucket,
          bbn_input_s3_key: uploadedJsonKey,
          prior_trace_s3_key: uploadedNcKey,
        };
        console.log('[BBN Payload] Uploaded files will be used:', payload);
        return payload;
      }
      return {};
    }
    // Select tab: use S3 list selection
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
  }, [bbnTab, selectedBbnKey, bbnBucketInfo, uploadedJsonKey, uploadedNcKey, uploadedBucket]);

  const getBbnSettings = useCallback(() => {
    let s: { nChains: string; nIter: string; nBurnin: string; nThin: string } | null = null;
    if (bbnTab === 'select') {
      s = editedSelectSettings ?? selectedBbnData?.input?.settings ?? null;
    } else if (bbnTab === 'upload') {
      s = editedUploadSettings ?? uploadedJsonSettings;
    }
    if (s) {
      const nIter = parseInt(s.nIter);
      const nBurnin = parseInt(s.nBurnin);
      return {
        draws: nIter - nBurnin,
        tune: nBurnin,
        chains: parseInt(s.nChains),
        thin: parseInt(s.nThin),
      };
    }
    // Fallback to app settings
    return {
      draws: settings.nIter - settings.nBurnin,
      tune: settings.nBurnin,
      chains: settings.nChains,
      thin: settings.nThin,
    };
  }, [bbnTab, selectedBbnData, editedSelectSettings, uploadedJsonSettings, editedUploadSettings, settings]);

  // Upload tab: handle file selection and upload to S3
  const handleUploadFile = async (
    file: File,
    fileType: 'json' | 'nc'
  ) => {
    if (fileType === 'json') {
      setJsonUploading(true);
      setJsonUploadError(null);
      setUploadedJsonKey(null);
      setUploadedJsonName(null);
      setUploadedJsonSettings(null);
      setEditedUploadSettings(null);
    } else {
      setNcUploading(true);
      setNcUploadError(null);
      setUploadedNcKey(null);
      setUploadedNcName(null);
    }
    try {
      const { s3_key, bucket } = await api.uploadFileToS3(file);
      if (fileType === 'json') {
        setUploadedJsonKey(s3_key);
        setUploadedJsonName(file.name);
        setUploadedBucket(bucket);

        // Parse JSON locally to extract hyperparameter settings
        try {
          const text = await file.text();
          const parsed = JSON.parse(text);
          const s = parsed?.input?.settings;
          if (s && s.nChains !== undefined && s.nIter !== undefined && s.nBurnin !== undefined && s.nThin !== undefined) {
            setUploadedJsonSettings({ nChains: String(s.nChains), nIter: String(s.nIter), nBurnin: String(s.nBurnin), nThin: String(s.nThin) });
          }
        } catch {
          // settings not available — silently ignore
        }
      } else {
        setUploadedNcKey(s3_key);
        setUploadedNcName(file.name);
        setUploadedBucket(bucket);
      }
    } catch (err: any) {
      const msg = err?.message ?? String(err);
      if (fileType === 'json') {
        setJsonUploadError(msg);
      } else {
        setNcUploadError(msg);
      }
    } finally {
      if (fileType === 'json') {
        setJsonUploading(false);
      } else {
        setNcUploading(false);
      }
    }
  };

  // 1) Sensitivity Analysis
  const handleSensitivitySubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);
    setSensitivityJobId(null);
    setSensitivityCompletedTime(null);

    // Quick validation
    const p = parseFloat(pfdGoal);
    const c = parseFloat(confidenceGoal);
    if (!Number.isFinite(p) || !Number.isFinite(c)) {
      setLoading(false);
      setErrorMsg("Please enter valid numbers.");
      return;
    }

    // Upload tab: both files required
    if (bbnTab === 'upload' && (!uploadedJsonKey || !uploadedNcKey)) {
      setLoading(false);
      setErrorMsg("Upload tab is selected but both JSON and NC files are required. Please upload both files before calculating.");
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
          ...getBbnSettings(),
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
        },
        (error) => {
          setErrorMsg(`Sensitivity Analysis error: ${error}`);
        }
      );
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Sensitivity Analysis error: ${err?.message ?? String(err)}`);
      setLoading(false);
    }
  };


  // 2) PFD Update
  const handlePfdUpdateSubmit = async () => {
    setErrorMsg(null);
    setLoading(true);
    setPfdUpdateResultData(null);
    setPfdUpdateJobId(null);
    setPfdUpdateCompletedTime(null);
    setPfdUpdateUsedDefaultBbn(bbnTab === 'select' ? !selectedBbnKey : false);

    const p = parseFloat(pfdGoal);
    const c = parseFloat(confidenceGoal);
    if (!Number.isFinite(p) || !Number.isFinite(c)) {
      setLoading(false);
      setErrorMsg("Please enter valid numbers.");
      return;
    }

    // Upload tab: both files required
    if (bbnTab === 'upload' && (!uploadedJsonKey || !uploadedNcKey)) {
      setLoading(false);
      setErrorMsg("Upload tab is selected but both JSON and NC files are required. Please upload both files before calculating.");
      return;
    }

    // Check if Sensitivity Analysis has been run
    if (tests === null || tests === 0) {
      setLoading(false);
      setErrorMsg("Please run Sensitivity Analysis first, or enter the number of tests manually.");
      return;
    }

    // Check Failures value
    if (failures === null) {
      setLoading(false);
      setErrorMsg("Please enter a Failures value.");
      return;
    }

    try {
      // NOTE: trace_id is sent but ignored by HybridTool (stateless architecture)
      // Test mode still makes actual API call but sends test_mode flag
      const jobResponse = await api.pfdUpdate({
        pfd_goal: p,
        confidence_goal: c,
        failures,
        demand_required: tests > 0 ? tests : undefined,
        trace_id: traceId ?? undefined,
        test_mode: testMode || undefined,
        ...buildBbnPayload(),
        settings: {
          ...getBbnSettings(),
        },
      });

      const jobId = jobResponse.job_id;
      setPfdUpdateJobId(jobId);
      setLoading(false);
      const jobStartTime = Date.now(); // Record job start time
      setIsPolling(true);
      setCurrentJobType('full-analysis');

      pollResults(
        jobId,
        'full-analysis',
        jobStartTime,
        (resultData, _, elapsedSeconds) => {
          if (resultData) {
            setPfdUpdateResultData(resultData);
          }
          setErrorMsg(null);
          if (elapsedSeconds !== undefined) {
            setPfdUpdateCompletedTime(elapsedSeconds);
          }
        },
        (error) => {
          setErrorMsg(`PFD Update error: ${error}`);
        }
      );
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`PFD Update error: ${err?.message ?? String(err)}`);
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
                  {loading ? 'Requesting...' : 'Calculating...'}
                </p>
                {!loading && isPolling && (
                  <div style={{ fontSize: '14px', color: '#1F2937' }}>
                    Elapsed time: {formatElapsedTime(elapsedTime)}
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
                <h2>Initial Reliability Assessment Result based on Bayesian Methods</h2>
                {bbnTab === 'select' && (
                  <p>
                    {bbnBucketInfo
                      ? `${bbnBucketInfo.bucket}/${bbnBucketInfo.prefix ?? ""}`
                      : "Loading bucket information..."}
                    {bbnBucketInfo && (
                      <>
                        {bbnLastRefreshed && (
                          <span style={{ marginLeft: 8 }}>
                            · Updated: {formatTimestamp(bbnLastRefreshed)}
                          </span>
                        )}
                        <span style={{ marginLeft: 8 }}>
                          · Total {bbnFiles.length.toLocaleString()} files
                        </span>
                      </>
                    )}
                  </p>
                )}
                {bbnTab === 'upload' && (
                  <p>Upload JSON and NC files downloaded from the BBN analysis result.</p>
                )}
              </div>
              {bbnTab === 'select' && (
                <button
                  type="button"
                  css={cssObj.bbnRefreshButton}
                  onClick={refreshBbnFiles}
                  disabled={bbnFilesLoading}
                >
                  {bbnFilesLoading ? "Loading..." : "Refresh List"}
                </button>
              )}
            </div>

            {/* Tab bar */}
            <div css={cssObj.bbnTabBar}>
              <button
                type="button"
                css={[cssObj.bbnTab, bbnTab === 'select' && cssObj.bbnTabActive]}
                onClick={() => setBbnTab('select')}
              >
                Select from list
              </button>
              <button
                type="button"
                css={[cssObj.bbnTab, bbnTab === 'upload' && cssObj.bbnTabActive]}
                onClick={() => setBbnTab('upload')}
              >
                Upload files
              </button>
            </div>

            {/* Tab: Select from list */}
            {bbnTab === 'select' && (
              <>
                <select
                  css={cssObj.bbnSelect}
                  value={selectedBbnKey}
                  onChange={(e) => handleSelectBbnFile(e.target.value)}
                  disabled={bbnFilesLoading || bbnFiles.length === 0}
                >
                  <option value="">Select a file</option>
                  {bbnFiles.map((item) => (
                    <option key={item.key} value={item.key}>
                      {formatFileLabel(item)}
                    </option>
                  ))}
                </select>

                {bbnFilesError && (
                  <span css={cssObj.bbnErrorText}>
                    Failed to load list: {bbnFilesError}
                  </span>
                )}

                {!bbnFilesLoading && bbnFiles.length === 0 && !bbnFilesError && (
                  <span css={cssObj.bbnMessage}>No JSON files available.</span>
                )}

                {bbnFileLoading && (
                  <span css={cssObj.bbnMessage}>Loading selected file...</span>
                )}

                {bbnFileMessage && <span css={cssObj.bbnErrorText}>{bbnFileMessage}</span>}

                {selectedBbnData && !bbnFileLoading && (
                  <>
                    {selectedBbnData.input?.settings
                      ? (
                        <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginTop: '8px' }}>
                          <div style={{ flex: 1 }}>
                            {renderHyperparamInfo(editedSelectSettings ?? {
                              nChains: String(selectedBbnData.input.settings.nChains),
                              nIter: String(selectedBbnData.input.settings.nIter),
                              nBurnin: String(selectedBbnData.input.settings.nBurnin),
                              nThin: String(selectedBbnData.input.settings.nThin),
                            })}
                          </div>
                          <button
                            type="button"
                            css={cssObj.bbnUploadButton}
                            style={{ marginTop: '0', whiteSpace: 'nowrap', flexShrink: 0 }}
                            onClick={() => {
                              const base = editedSelectSettings ?? {
                                nChains: String(selectedBbnData.input.settings.nChains),
                                nIter: String(selectedBbnData.input.settings.nIter),
                                nBurnin: String(selectedBbnData.input.settings.nBurnin),
                                nThin: String(selectedBbnData.input.settings.nThin),
                              };
                              setModalDraft({ ...base });
                              setHyperparamModalTarget('select');
                              setIsHyperparamModalOpen(true);
                            }}
                          >
                            Edit settings
                          </button>
                        </div>
                        )
                      : selectedBbnMeta && (
                          <div css={cssObj.bbnMetaInfo}>
                            <span>File: {selectedBbnMeta.name}</span>
                            {typeof selectedBbnMeta.size === "number" && (
                              <span>Size: {formatBytes(selectedBbnMeta.size)}</span>
                            )}
                            {selectedBbnMeta.last_modified && (
                              <span>Modified: {formatTimestamp(selectedBbnMeta.last_modified)}</span>
                            )}
                          </div>
                        )
                    }
                    <div css={cssObj.bbnActionRow}>
                      <button
                        type="button"
                        css={[cssObj.bbnButton, cssObj.bbnPrimaryButton]}
                        onClick={handleViewSelectedBbnData}
                      >
                        View
                      </button>
                      <button
                        type="button"
                        css={[cssObj.bbnButton, cssObj.bbnSecondaryButton]}
                        onClick={handleDownloadSelectedBbnData}
                      >
                        Download
                      </button>
                    </div>
                  </>
                )}
              </>
            )}

            {/* Tab: Upload files */}
            {bbnTab === 'upload' && (
              <div css={cssObj.bbnUploadArea}>
                {/* JSON file */}
                <div css={cssObj.bbnUploadRow}>
                  <span css={cssObj.bbnUploadLabel}>JSON file</span>
                  <input
                    ref={jsonFileInputRef}
                    type="file"
                    accept=".json,application/json"
                    css={cssObj.bbnUploadInput}
                    disabled={jsonUploading}
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleUploadFile(file, 'json');
                    }}
                  />
                  <button
                    type="button"
                    css={cssObj.bbnUploadButton}
                    disabled={jsonUploading}
                    onClick={() => jsonFileInputRef.current?.click()}
                  >
                    {jsonUploading ? 'Uploading...' : 'Choose file'}
                  </button>
                  <span css={cssObj.bbnUploadFileName}>
                    {jsonUploadError
                      ? <span css={cssObj.bbnErrorText}>Error: {jsonUploadError}</span>
                      : uploadedJsonName
                        ? <span css={cssObj.bbnUploadStatusOk}>✓ {uploadedJsonName}</span>
                        : 'No file chosen'}
                  </span>
                </div>

                {/* NC file */}
                <div css={cssObj.bbnUploadRow}>
                  <span css={cssObj.bbnUploadLabel}>NC file</span>
                  <input
                    ref={ncFileInputRef}
                    type="file"
                    accept=".nc,application/x-netcdf,application/octet-stream"
                    css={cssObj.bbnUploadInput}
                    disabled={ncUploading}
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleUploadFile(file, 'nc');
                    }}
                  />
                  <button
                    type="button"
                    css={cssObj.bbnUploadButton}
                    disabled={ncUploading}
                    onClick={() => ncFileInputRef.current?.click()}
                  >
                    {ncUploading ? 'Uploading...' : 'Choose file'}
                  </button>
                  <span css={cssObj.bbnUploadFileName}>
                    {ncUploadError
                      ? <span css={cssObj.bbnErrorText}>Error: {ncUploadError}</span>
                      : uploadedNcName
                        ? <span css={cssObj.bbnUploadStatusOk}>✓ {uploadedNcName}</span>
                        : 'No file chosen'}
                  </span>
                </div>

                {uploadedJsonSettings && (
                  <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginTop: '8px' }}>
                    <div style={{ flex: 1 }}>
                      {renderHyperparamInfo(editedUploadSettings ?? uploadedJsonSettings)}
                    </div>
                    <button
                      type="button"
                      css={cssObj.bbnUploadButton}
                      style={{ marginTop: '0', whiteSpace: 'nowrap', flexShrink: 0 }}
                      onClick={() => {
                        const current = editedUploadSettings ?? uploadedJsonSettings;
                        setModalDraft({ ...current });
                        setHyperparamModalTarget('upload');
                        setIsHyperparamModalOpen(true);
                      }}
                    >
                      Edit settings
                    </button>
                  </div>
                )}

                {(!uploadedJsonKey || !uploadedNcKey) && (uploadedJsonKey || uploadedNcKey) && (
                  <span css={cssObj.bbnErrorText}>
                    Both JSON and NC files must be uploaded before calculating.
                  </span>
                )}
                {uploadedJsonKey && uploadedNcKey && (
                  <span css={cssObj.bbnUploadStatusOk}>
                    Both files uploaded. Ready to calculate.
                  </span>
                )}
              </div>
            )}
          </div>

          {/* 3-column grid */}
          <div css={cssObj.settingsGrid}>

            {/* 1. Sensitivity Analysis */}
            <div css={cssObj.settingBox}>
              <form onSubmit={handleSensitivitySubmit} css={cssObj.formWrapper}>
                <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  1. Required number of tests
                  <span style={{ position: 'relative', display: 'inline-flex', alignItems: 'center' }}>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '16px',
                        height: '16px',
                        borderRadius: '50%',
                        border: '1.5px solid #6B7280',
                        color: '#6B7280',
                        fontSize: '11px',
                        fontWeight: 'bold',
                        cursor: 'default',
                        userSelect: 'none',
                      }}
                      className="info-icon-trigger"
                    >
                      i
                    </span>
                    <span
                      className="info-tooltip"
                      style={{
                        position: 'absolute',
                        left: '50%',
                        bottom: 'calc(100% + 6px)',
                        transform: 'translateX(-50%)',
                        backgroundColor: '#1F2937',
                        color: '#F9FAFB',
                        fontSize: '12px',
                        fontWeight: 'normal',
                        lineHeight: '1.5',
                        padding: '8px 10px',
                        borderRadius: '6px',
                        whiteSpace: 'nowrap',
                        pointerEvents: 'none',
                        opacity: 0,
                        transition: 'opacity 0.15s',
                        zIndex: 10,
                      }}
                    >
                      Calculates the required number of tests 
                      <br />to achieve the input PFD and confidence goal,
                      <br />assuming no failures occur.
                    </span>
                  </span>
                </h2>
                <div css={cssObj.inputGroup}>
                  <label css={cssObj.inputLabel}>PFD goal</label>
                  <input
                    type="number"
                    step="any"
                    value={pfdGoal}
                    onChange={(e) => setPfdGoal(e.target.value)}
                    placeholder="e.g. 0.0001"
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
                    placeholder="e.g. 0.95"
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
                    {isPolling && currentJobType === 'sensitivity-analysis' ? 'Calculating...' : 'Calculate'}
                  </button>
                  {sensitivityCompletedTime !== null && (
                    <span style={{ color: '#666', fontSize: '13px' }}>
                      ({formatElapsedTime(sensitivityCompletedTime)} elapsed)
                    </span>
                  )}
                </div>
                <div css={cssObj.outputBox}>
                  <span css={cssObj.outputLabel}>Required number of tests</span>
                  <span css={cssObj.outputValue}>
                    {tests !== null && tests > 0 ? tests : '—'}
                  </span>
                </div>
              </form>
            </div>

            {/* 2. PFD Update */}
            <div css={cssObj.settingBox}>
              <form onSubmit={(e) => { e.preventDefault(); handlePfdUpdateSubmit(); }} css={cssObj.formWrapper}>
                <h2 style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  2. PFD update
                  <span style={{ position: 'relative', display: 'inline-flex', alignItems: 'center' }}>
                    <span
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '16px',
                        height: '16px',
                        borderRadius: '50%',
                        border: '1.5px solid #6B7280',
                        color: '#6B7280',
                        fontSize: '11px',
                        fontWeight: 'bold',
                        cursor: 'default',
                        userSelect: 'none',
                      }}
                      className="info-icon-trigger"
                    >
                      i
                    </span>
                    <span
                      className="info-tooltip"
                      style={{
                        position: 'absolute',
                        left: '50%',
                        bottom: 'calc(100% + 6px)',
                        transform: 'translateX(-50%)',
                        backgroundColor: '#1F2937',
                        color: '#F9FAFB',
                        fontSize: '12px',
                        fontWeight: 'normal',
                        lineHeight: '1.5',
                        padding: '8px 10px',
                        borderRadius: '6px',
                        whiteSpace: 'nowrap',
                        pointerEvents: 'none',
                        opacity: 0,
                        transition: 'opacity 0.15s',
                        zIndex: 10,
                      }}
                    >
                      Updates the BBN-derived prior PFD with observed test results
                      <br/> to reflect the current system reliability.
                    </span>
                  </span>
                </h2>
                <div css={cssObj.hintText} style={{ display: 'flex', gap: '12px', fontSize: '13px' }}>
                  <span>PFD goal: <strong>{pfdGoal !== '' ? pfdGoal : '—'}</strong></span>
                  <span>Confidence goal: <strong>{confidenceGoal !== '' ? confidenceGoal : '—'}</strong></span>
                </div>
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
                        placeholder="e.g. 10"
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
                        Edit
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
                        Restore auto-fill
                      </button>
                    )}
                  </div>
                  <span css={isNumOfTestsLocked ? cssObj.hintText : cssObj.warningHintText}>
                    {isNumOfTestsLocked
                      ? 'Auto-filled from Sensitivity analysis result.'
                      : 'Will run with the entered value, independent of Sensitivity analysis result.'}
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
                    placeholder="e.g. 1"
                    css={cssObj.inputBox}
                    min={0}
                    required
                  />
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <button
                    type="submit"
                    css={cssObj.saveButton}
                    disabled={loading || isPolling || (pfdUpdateJobId !== null && currentJobType === 'full-analysis')}
                  >
                    {isPolling && currentJobType === 'full-analysis' ? 'Analyzing...' : 'Run update'}
                  </button>
                  {pfdUpdateCompletedTime !== null && (
                    <span style={{ color: '#666', fontSize: '13px' }}>
                      ({formatElapsedTime(pfdUpdateCompletedTime!)} elapsed)
                    </span>
                  )}
                </div>
              </form>
            </div>

            {/* 3. Result Summary */}
            <div css={cssObj.settingBox}>
              <div css={cssObj.resultSummaryHeader}>
                <span>Result summary</span>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <button
                    css={cssObj.jsonDownloadBtn}
                    onClick={handleViewPfdUpdateJson}
                    disabled={!pfdUpdateResultData}
                    title="View result in new tab"
                  >
                    <svg width="14" height="14" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg" style={{ display: 'block' }}>
                      <path d="M7 2.5C4.5 2.5 2.5 4.5 2.5 7C2.5 9.5 4.5 11.5 7 11.5C9.5 11.5 11.5 9.5 11.5 7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
                      <path d="M9 1.5H12.5V5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
                      <path d="M12.5 1.5L7.5 6.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
                    </svg>
                  </button>
                  <button
                    css={cssObj.jsonDownloadBtn}
                    onClick={handleDownloadPfdUpdateJson}
                    disabled={!pfdUpdateResultData}
                    title="JSON 다운로드"
                  >
                    ↓ JSON
                  </button>
                </div>
              </div>
              <div css={cssObj.resultCardPriorRow}>
                <span>Prior PFD:</span>
                <span style={{ fontWeight: 600, color: '#374151' }}>
                  {pfdUpdateResultData?.input?.parameter?.prior?.mean != null
                    ? pfdUpdateResultData.input.parameter.prior.mean.toExponential(4)
                    : '—'}
                </span>
              </div>
              <div css={cssObj.resultCardGrid}>
                <div css={cssObj.resultCardPrimary}>
                  <span css={cssObj.resultCardLabelPrimary}>Updated PFD</span>
                  <span css={cssObj.resultCardValuePrimary}>
                    {pfdUpdateResultData?.output?.mean_posterior_pfd?.[0]?.[1] != null
                      ? pfdUpdateResultData.output.mean_posterior_pfd[0][1].toExponential(4)
                      : '—'}
                  </span>
                </div>
                <div css={cssObj.resultCardPrimary}>
                  <span css={cssObj.resultCardLabelPrimary}>Confidence</span>
                  <span css={cssObj.resultCardValuePrimary}>
                    {pfdUpdateResultData?.output?.confidence != null
                      ? (pfdUpdateResultData.output.confidence * 100).toFixed(1) + '%'
                      : '—'}
                  </span>
                </div>
              </div>
              {pfdUpdateUsedDefaultBbn && (
                <div css={cssObj.hintText} style={{ marginTop: 8 }}>
                  BBN input: NRC report data (default)
                </div>
              )}
            </div>

          </div>

          {/* Footer note */}
          <div css={cssObj.footerNote}>
            Each section can be run in order or used independently.
          </div>

        </main>
      </div>

      {/* Hyperparameter edit modal */}
      {isHyperparamModalOpen && (
        <div
          style={{
            position: 'fixed', inset: 0, zIndex: 1000,
            backgroundColor: 'rgba(0,0,0,0.4)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
          onClick={() => setIsHyperparamModalOpen(false)}
        >
          <div
            style={{
              background: '#fff', borderRadius: '10px', padding: '28px 32px',
              width: '340px', boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
              display: 'flex', flexDirection: 'column', gap: '16px',
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 700, color: '#111827' }}>
              Edit Bayesian Settings
            </h3>

            {(['nChains', 'nIter', 'nBurnin', 'nThin'] as const).map((key) => {
              const labels: Record<string, string> = { nChains: 'Chains', nIter: 'Iterations', nBurnin: 'Burn-in', nThin: 'Thin' };
              return (
                <div key={key} style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <label style={{ fontSize: '13px', color: '#374151', fontWeight: 500 }}>{labels[key]}</label>
                  <input
                    type="number"
                    min={1}
                    value={modalDraft[key]}
                    onChange={(e) => setModalDraft((prev) => ({ ...prev, [key]: e.target.value }))}
                    css={cssObj.inputBox}
                  />
                </div>
              );
            })}

            <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end', marginTop: '4px' }}>
              <button
                type="button"
                css={[cssObj.bbnButton, cssObj.bbnSecondaryButton]}
                onClick={() => {
                  if (hyperparamModalTarget === 'select') setEditedSelectSettings(null);
                  else setEditedUploadSettings(null);
                  setIsHyperparamModalOpen(false);
                }}
              >
                Reset to original
              </button>
              <button
                type="button"
                css={[cssObj.bbnButton]}
                style={{ background: '#E5E7EB', color: '#374151' }}
                onClick={() => setIsHyperparamModalOpen(false)}
              >
                Cancel
              </button>
              <button
                type="button"
                css={[cssObj.bbnButton, cssObj.bbnPrimaryButton]}
                onClick={() => {
                  if (hyperparamModalTarget === 'select') setEditedSelectSettings({ ...modalDraft });
                  else setEditedUploadSettings({ ...modalDraft });
                  setIsHyperparamModalOpen(false);
                }}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
