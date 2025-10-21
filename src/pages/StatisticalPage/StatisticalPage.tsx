/** @jsxImportSource @emotion/react */
import { useState, type FormEvent } from "react";
import { Global } from "@emotion/react";
import { cssObj } from "./style";
import * as api from "../../services/apiService"; // <-- calls AWS endpoints you wired

export default function StatisticalPage() {
  // 입력값
  const [pfdGoal, setPfdGoal] = useState("");
  const [confidenceGoal, setConfidenceGoal] = useState("");

  // trace 재사용용
  const [traceId, setTraceId] = useState<string | null>(null);

  // 2단계 입력
  const [tests, setTests] = useState<number>(0);
  const [failures, setFailures] = useState<number>(0);

  // 상태/링크
  const [loading, setLoading] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [downloadLink, setDownloadLink] = useState<string | null>(null);

  // 1) Number of Tests 계산
  const handleSensitivitySubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);

    // quick guard
    const p = parseFloat(pfdGoal);
    const c = parseFloat(confidenceGoal);
    if (!Number.isFinite(p) || !Number.isFinite(c)) {
      setLoading(false);
      setErrorMsg("숫자를 정확히 입력하세요.");
      return;
    }

    try {
      const out = await api.sensitivityAnalysis({
        pfd_goal: p,
        confidence_goal: c,
        trace_id: traceId ?? undefined,
      });
      if (out.trace_id) setTraceId(out.trace_id);
      setTests(Number(out.data.num_tests));
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Sensitivity Analysis 오류: ${err?.message ?? String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  // 2) Update PFD
  const handlePfdUpdateSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);

    const p = parseFloat(pfdGoal);
    if (!Number.isFinite(p)) {
      setLoading(false);
      setErrorMsg("PFD Goal을 숫자로 입력하세요.");
      return;
    }

    try {
      const out = await api.updatePfd({
        pfd_goal: p,
        demand: tests,
        failures,
        trace_id: traceId ?? undefined,
      });
      if (out.trace_id) setTraceId(out.trace_id);
      // 성공 메시지를 별도로 노출하고 싶으면 여기서 setErrorMsg(null) 유지
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Update PFD 오류: ${err?.message ?? String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  // 3) Full Analysis (저장 & 다운로드 링크 노출)
  const handleFullAnalysisSubmit = async () => {
    setErrorMsg(null);
    setLoading(true);
    setDownloadLink(null);

    const p = parseFloat(pfdGoal);
    const c = parseFloat(confidenceGoal);
    if (!Number.isFinite(p) || !Number.isFinite(c)) {
      setLoading(false);
      setErrorMsg("숫자를 정확히 입력하세요.");
      return;
    }

    try {
      const out = await api.fullAnalysis({
        pfd_goal: p,
        confidence_goal: c,
        failures,
        trace_id: traceId ?? undefined,
      });
      if (out.trace_id) setTraceId(out.trace_id);
      if (out.download_url) setDownloadLink(out.download_url);
      else setErrorMsg("download_url 이 응답에 없습니다.");
    } catch (err: any) {
      console.error(err);
      setErrorMsg(`Full Analysis 오류: ${err?.message ?? String(err)}`);
    } finally {
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
            <h1 css={cssObj.title}>Statistical Methods</h1>
          </section>

          {loading && (
            <div css={cssObj.container} style={{ marginTop: 8 }}>
              <p>처리 중입니다...</p>
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
                <button type="submit" css={cssObj.saveButton} disabled={loading}>
                  Calculate Number of Tests
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
                <button type="submit" css={cssObj.saveButton} disabled={loading}>
                  Update
                </button>
              </form>
            </div>

            {/* 3. Full Analysis */}
            <div css={[cssObj.settingBox, cssObj.longSettingBox]}>
              <h2>3. Full Analysis (Save JSON)</h2>
              <button
                css={cssObj.saveButton}
                onClick={handleFullAnalysisSubmit}
                disabled={loading}
              >
                Run Full Analysis and Save
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
