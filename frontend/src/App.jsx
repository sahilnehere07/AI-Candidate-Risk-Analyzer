import { useEffect, useState } from "react";
import "./App.css";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [page, setPage] = useState("landing");

  const [candidateName, setCandidateName] = useState("");
  const [candidateEmail, setCandidateEmail] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [documentName, setDocumentName] = useState("");

  const [applicationStartTime, setApplicationStartTime] = useState(null);

  const [result, setResult] = useState(null);
  const [botResult, setBotResult] = useState(null);
  const [candidateRisk, setCandidateRisk] = useState(null);

  const [loading, setLoading] = useState(false);
  const [loadingCandidate, setLoadingCandidate] = useState(false);
  const [error, setError] = useState("");

  const [candidates, setCandidates] = useState([]);
  const [loadingCandidates, setLoadingCandidates] = useState(false);


  async function loadCandidates() {
    setLoadingCandidates(true);

    try {
      const response = await fetch(`${API_BASE}/candidates`);

      if (!response.ok) {
        throw new Error("Failed to load candidate history.");
      }

      const data = await response.json();
      setCandidates(data);
    } catch (error) {
      console.error("Candidate history error:", error);
    } finally {
      setLoadingCandidates(false);
    }
  }

  useEffect(() => {
    loadCandidates();
  }, []);

  useEffect(() => {
    if (page === "candidate-analysis") {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: "auto",
      });
    }
  }, [page]);

  function startApplication() {
    setCandidateName("");
    setCandidateEmail("");
    setSelectedFile(null);
    setDocumentName("");
    setResult(null);
    setBotResult(null);
    setCandidateRisk(null);
    setError("");

    setApplicationStartTime(Date.now());
    setPage("application");

    window.scrollTo({
      top: 0,
      behavior: "auto",
    });
  }

  function handleFileChange(event) {
    const file = event.target.files[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setDocumentName(file.name);
    setError("");
  }

  async function handleSubmitApplication(event) {
    event.preventDefault();

    if (!candidateName.trim()) {
      setError("Please enter your full name.");
      return;
    }

    if (!candidateEmail.trim()) {
      setError("Please enter your email address.");
      return;
    }

    if (!selectedFile) {
      setError("Please upload your resume.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const timeTakenSeconds = applicationStartTime
        ? (Date.now() - applicationStartTime) / 1000
        : 10;

      // =========================================================
      // ENGINE 1: RESUME ANALYSIS
      // =========================================================

      const formData = new FormData();
      formData.append("file", selectedFile);

      const uploadResponse = await fetch(`${API_BASE}/upload`, {
        method: "POST",
        body: formData,
      });

      const uploadData = await uploadResponse.json();

      if (!uploadResponse.ok) {
        throw new Error(
          uploadData.detail ||
            "Unable to analyze the resume."
        );
      }

      // =========================================================
      // ENGINE 2: BOT DETECTION
      // =========================================================

      const botResponse = await fetch(
        `${API_BASE}/submit-application`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            honeypot_value: "",
            time_taken_seconds: timeTakenSeconds,
            user_agent: navigator.userAgent,
          }),
        }
      );

      const botData = await botResponse.json();

      if (!botResponse.ok) {
        throw new Error(
          botData.detail ||
            "Unable to analyze application behavior."
        );
      }

      // =========================================================
      // SAVE FINAL CANDIDATE RISK
      // =========================================================

      const riskResponse = await fetch(
        `${API_BASE}/candidate-risk`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: candidateName,
            email: candidateEmail,
            resume_filename: selectedFile.name,
            analysis: uploadData.analysis,
            ai_risk: uploadData.risk,
            bot_detection: botData.bot_detection,
            rate_limit: botData.rate_limit,
          }),
        }
      );

      const riskData = await riskResponse.json();

      if (!riskResponse.ok) {
        throw new Error(
          riskData.detail ||
            "Unable to calculate candidate risk."
        );
      }

      setResult(uploadData);
      setBotResult(botData);
      setCandidateRisk(riskData);
      setDocumentName(selectedFile.name);

      await loadCandidates();

      setPage("dashboard");
    } catch (error) {
      console.error(
        "Application submission error:",
        error
      );

      setError(
        error.message ||
          "Unable to connect to the backend."
      );
    } finally {
      setLoading(false);
    }
  }

  // =========================================================
  // OPEN SAVED CANDIDATE
  // =========================================================

  async function openCandidate(candidateId) {
    if (!candidateId) {
      setError("Invalid candidate ID.");
      return;
    }

    setLoadingCandidate(true);
    setError("");

    try {
      console.log(
        "Opening saved candidate:",
        candidateId
      );

      const response = await fetch(
        `${API_BASE}/candidates/${candidateId}`
      );

      const data = await response.json();

      console.log(
        "Saved candidate response:",
        data
      );

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Unable to load saved candidate."
        );
      }

      // =========================================================
      // CANDIDATE INFORMATION
      // =========================================================

      setCandidateName(data.name || "");
      setCandidateEmail(data.email || "");
      setDocumentName(data.resume_filename || "");
      setSelectedFile(null);

      // =========================================================
      // NLP ANALYSIS
      // =========================================================

      setResult({
        filename: data.resume_filename,

        analysis: {
          sentence_count:
            data.sentence_count || 0,

          sentence_lengths: [],

          average_sentence_length:
            data.average_sentence_length || 0,

          burstiness:
            data.burstiness || 0,

          buzzword_count: 0,

          flagged_phrases: [],

          ai_style_pattern_count: 0,

          ai_style_patterns: [],

          bigram_density:
            data.bigram_density || 0,

          trigram_density:
            data.trigram_density || 0,

          vocabulary_diversity:
            data.vocabulary_diversity || 0,
        },

        metadata: {
          author: null,
          creator: null,
          producer: null,
          creation_date: null,
          modification_date: null,
        },

        metadata_analysis: {
          suspicious_count: 0,
          suspicious_fields: [],
        },

        risk: {
          ai_risk_score:
            data.ai_risk_score || 0,

          classification:
            data.ai_classification ||
            "Unknown",

          signals:
            data.ai_signals || [],

          contributions:
            data.ai_contributions || [],
        },
      });

      // =========================================================
      // BOT INFORMATION
      // =========================================================

      setBotResult({
        bot_detection: {
          is_bot:
            Boolean(data.bot_detected),

          reason_count:
            data.bot_reason_count || 0,

          reasons:
            data.bot_reasons || [],
        },

        rate_limit: {
          is_rate_limited:
            Boolean(data.rate_limited),
        },
      });

      // =========================================================
      // FINAL RISK INFORMATION
      // =========================================================

      setCandidateRisk({
        candidate_id: data.id,

        overall_status:
          data.overall_status ||
          "Unknown",

        ai_content: {
          score:
            data.ai_risk_score || 0,

          classification:
            data.ai_classification ||
            "Unknown",

          signals:
            data.ai_signals || [],
        },

        bot_behavior: {
          is_bot:
            Boolean(data.bot_detected),

          reason_count:
            data.bot_reason_count || 0,

          reasons:
            data.bot_reasons || [],

          rate_limited:
            Boolean(data.rate_limited),
        },
      });

      // Open the dedicated saved-candidate analysis view.
      setPage("candidate-analysis");

      console.log(
        "Saved candidate opened successfully."
      );
    } catch (error) {
      console.error(
        "Saved candidate error:",
        error
      );

      setError(
        error.message ||
          "Unable to load saved candidate."
      );
    } finally {
      setLoadingCandidate(false);
    }
  }

  function startAnotherApplication() {
    setPage("landing");

    setResult(null);
    setBotResult(null);
    setCandidateRisk(null);

    setSelectedFile(null);
    setDocumentName("");

    setCandidateName("");
    setCandidateEmail("");

    setError("");

    window.scrollTo({
      top: 0,
      behavior: "auto",
    });
  }

  // =========================================================
  // LANDING PAGE
  // =========================================================

  if (page === "landing") {
    return (
      <div className="app">

        <header className="topbar">
          <div className="brand">

            <div className="brand-icon">
              V
            </div>

            <div>
              <h1>
                Candidate Risk Analyzer
              </h1>

              <p>
                AI-powered application screening
              </p>
            </div>

          </div>

          <div className="status">
            <span className="status-dot"></span>
            System Online
          </div>
        </header>

        <main className="landing-page">

          <section className="hero">

            <div className="hero-badge">
              AI + BEHAVIORAL SECURITY
            </div>

            <h2>
              Smarter candidate
              <br />
              <span>screening.</span>
            </h2>

            <p>
              Analyze resume content, document signals,
              and application behavior to help recruiters
              identify candidates that deserve closer review.
            </p>

            <button
              className="primary-button"
              onClick={startApplication}
            >
              Start Application
              <span>→</span>
            </button>

            <div className="hero-note">
              Secure analysis · PDF & DOCX · Recruiter review
            </div>

          </section>

          <section className="engine-grid">

            <div className="engine-card">

              <div className="engine-number">
                01
              </div>

              <h3>
                NLP Analysis
              </h3>

              <p>
                Examines sentence patterns, repeated
                n-grams, vocabulary diversity, and
                other text signals.
              </p>

            </div>

            <div className="engine-card">

              <div className="engine-number">
                02
              </div>

              <h3>
                Behavioral Security
              </h3>

              <p>
                Checks submission speed, suspicious
                user agents, honeypots, and rate limits.
              </p>

            </div>

            <div className="engine-card">

              <div className="engine-number">
                03
              </div>

              <h3>
                Risk Triage
              </h3>

              <p>
                Combines the signals into a recruiter-
                friendly candidate risk assessment.
              </p>

            </div>

          </section>

        </main>

      </div>
    );
  }

  // =========================================================
  // APPLICATION PAGE
  // =========================================================

  if (page === "application") {
    return (
      <div className="app">

        <header className="topbar">

          <div className="brand">

            <div className="brand-icon">
              V
            </div>

            <div>
              <h1>
                Candidate Application
              </h1>

              <p>
                Secure application screening
              </p>
            </div>

          </div>

          <div className="status">
            <span className="status-dot"></span>
            Application Active
          </div>

        </header>

        <main className="application-page">

          <div className="application-header">

            <p className="eyebrow">
              JOB APPLICATION
            </p>

            <h2>
              Submit your application
            </h2>

            <p>
              Complete the form and upload your resume.
              Your application will be analyzed automatically.
            </p>

          </div>

          <form
            className="application-card"
            onSubmit={handleSubmitApplication}
          >

            <div className="form-section">

              <div className="section-title">
                Candidate information
              </div>

              <label>
                Full name

                <input
                  type="text"
                  placeholder="Enter your full name"
                  value={candidateName}
                  onChange={(event) =>
                    setCandidateName(
                      event.target.value
                    )
                  }
                />
              </label>

              <label>
                Email address

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={candidateEmail}
                  onChange={(event) =>
                    setCandidateEmail(
                      event.target.value
                    )
                  }
                />
              </label>

            </div>

            <div className="form-section">

              <div className="section-title">
                Resume
              </div>

              <label className="resume-dropzone">

                <div className="resume-icon">
                  ↑
                </div>

                <strong>
                  {selectedFile
                    ? selectedFile.name
                    : "Upload your resume"}
                </strong>

                <span>
                  PDF or DOCX · Maximum 5 MB
                </span>

                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={handleFileChange}
                  hidden
                />

              </label>

            </div>

            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

            <div className="form-footer">

              <button
                type="button"
                className="secondary-button"
                onClick={() =>
                  setPage("landing")
                }
              >
                Back
              </button>

              <button
                type="submit"
                className="primary-button"
                disabled={loading}
              >
                {loading
                  ? "Analyzing Application..."
                  : "Submit Application →"}
              </button>

            </div>

          </form>

          <div className="privacy-note">
            Your application is analyzed using automated
            risk signals. Results are intended to support
            recruiter review, not automatically reject candidates.
          </div>

        </main>

      </div>
    );
  }

  // =========================================================
  // DASHBOARD
  // =========================================================

  return (
    <div className="app">

      <header className="topbar">

        <div className="brand">

          <div className="brand-icon">
            V
          </div>

          <div>
            <h1>
              Candidate Risk Analyzer
            </h1>

            <p>
              Recruiter dashboard
            </p>
          </div>

        </div>

        <div className="status">
          <span className="status-dot"></span>
          Analysis Complete
        </div>

      </header>

      <main className="dashboard">

        <section className="welcome">

          <p className="eyebrow">
            RECRUITER DASHBOARD
          </p>

          <h2>
            Candidate analysis
          </h2>

          <p className="description">
            Review automated signals for the submitted candidate.
          </p>

          {page === "candidate-analysis" && (
            <button
              type="button"
              className="secondary-button dashboard-button"
              onClick={() => {
                setPage("dashboard");
                window.scrollTo({
                  top: 0,
                  left: 0,
                  behavior: "auto",
                });
              }}
            >
              ← Back to Candidate History
            </button>
          )}

        </section>

        {loadingCandidate && (
          <div className="result-item">
            Loading saved candidate analysis...
          </div>
        )}

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {candidateRisk && result && botResult && (
          <>

            {/* CANDIDATE */}

            <section className="candidate-banner">

              <div>
                <span>
                  CANDIDATE
                </span>

                <strong>
                  {candidateName}
                </strong>
              </div>

              <div>
                <span>
                  EMAIL
                </span>

                <strong>
                  {candidateEmail}
                </strong>
              </div>

              <div>
                <span>
                  DOCUMENT
                </span>

                <strong>
                  {documentName}
                </strong>
              </div>

            </section>

            {/* METRICS */}

            <section className="metrics">

              <div className="metric-card">

                <span className="metric-label">
                  AI CONTENT RISK
                </span>

                <strong>
                  {candidateRisk.ai_content.score}/100
                </strong>

                <p>
                  {candidateRisk.ai_content.classification}
                </p>

              </div>

              <div className="metric-card">

                <span className="metric-label">
                  BOT BEHAVIOR
                </span>

                <strong>
                  {candidateRisk.bot_behavior.is_bot
                    ? "FLAGGED"
                    : "LOW"}
                </strong>

                <p>
                  {candidateRisk.bot_behavior.is_bot
                    ? "Suspicious behavior detected"
                    : "No suspicious behavior"}
                </p>

              </div>

              <div className="metric-card">

                <span className="metric-label">
                  OVERALL STATUS
                </span>

                <strong>
                  {candidateRisk.overall_status}
                </strong>

                <p>
                  Recruiter triage result
                </p>

              </div>

            </section>

            {/* RISK SIGNALS */}

            <section className="signals-card">

              <div className="section-heading">

                <div>

                  <p className="eyebrow">
                    ANALYSIS
                  </p>

                  <h3>
                    Risk signals
                  </h3>

                </div>

                <span className="empty-badge">
                  {candidateRisk.ai_content.signals.length +
                    candidateRisk.bot_behavior.reasons.length}{" "}
                  signals
                </span>

              </div>

              <div className="results">

                {candidateRisk.ai_content.signals.map(
                  (signal, index) => (
                    <div
                      className="result-item"
                      key={`ai-${index}`}
                    >
                      <span className="signal-dot"></span>
                      {signal}
                    </div>
                  )
                )}

                {candidateRisk.bot_behavior.reasons.map(
                  (reason, index) => (
                    <div
                      className="result-item"
                      key={`bot-${index}`}
                    >
                      <span className="signal-dot"></span>
                      {reason}
                    </div>
                  )
                )}

                {candidateRisk.ai_content.signals.length === 0 &&
                  candidateRisk.bot_behavior.reasons.length === 0 && (
                    <div className="result-item">
                      No suspicious signals detected.
                    </div>
                  )}

              </div>

            </section>

            {/* NLP FEATURES */}

            <section className="signals-card">

              <div className="section-heading">

                <div>

                  <p className="eyebrow">
                    NLP FEATURES
                  </p>

                  <h3>
                    Text analysis
                  </h3>

                </div>

              </div>

              <div className="feature-grid">

                <div className="feature">

                  <span>
                    Sentence count
                  </span>

                  <strong>
                    {result.analysis.sentence_count}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Average sentence length
                  </span>

                  <strong>
                    {result.analysis.average_sentence_length}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Burstiness
                  </span>

                  <strong>
                    {result.analysis.burstiness}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Bigram density
                  </span>

                  <strong>
                    {result.analysis.bigram_density}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Trigram density
                  </span>

                  <strong>
                    {result.analysis.trigram_density}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Vocabulary diversity
                  </span>

                  <strong>
                    {result.analysis.vocabulary_diversity}
                  </strong>

                </div>

              </div>

            </section>

            {/* BOT DETECTION */}

            <section className="signals-card">

              <div className="section-heading">

                <div>

                  <p className="eyebrow">
                    BEHAVIORAL SECURITY
                  </p>

                  <h3>
                    Bot detection
                  </h3>

                </div>

              </div>

              <div className="feature-grid">

                <div className="feature">

                  <span>
                    Bot detected
                  </span>

                  <strong>
                    {botResult.bot_detection.is_bot
                      ? "Yes"
                      : "No"}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Detection reasons
                  </span>

                  <strong>
                    {botResult.bot_detection.reason_count}
                  </strong>

                </div>

                <div className="feature">

                  <span>
                    Rate limit
                  </span>

                  <strong>
                    {botResult.rate_limit.is_rate_limited
                      ? "Blocked"
                      : "Allowed"}
                  </strong>

                </div>

              </div>

            </section>

            {page === "dashboard" && (
              <>
                {/* CANDIDATE HISTORY */}

                <section className="signals-card">

              <div className="section-heading">

                <div>

                  <p className="eyebrow">
                    DATABASE
                  </p>

                  <h3>
                    Candidate history
                  </h3>

                </div>

                <span className="empty-badge">
                  {candidates.length}{" "}
                  {candidates.length === 1
                    ? "candidate"
                    : "candidates"}
                </span>

              </div>

              {loadingCandidates ? (
                <div className="result-item">
                  Loading candidate history...
                </div>
              ) : candidates.length === 0 ? (
                <div className="result-item">
                  No saved candidates yet.
                </div>
              ) : (

                <div
                  style={{
                    overflowX: "auto",
                    width: "100%",
                  }}
                >

                  <table
                    style={{
                      width: "100%",
                      borderCollapse: "collapse",
                      minWidth: "950px",
                    }}
                  >

                    <thead>

                      <tr>

                        <th style={tableHeaderStyle}>
                          Candidate
                        </th>

                        <th style={tableHeaderStyle}>
                          Resume
                        </th>

                        <th style={tableHeaderStyle}>
                          AI Risk
                        </th>

                        <th style={tableHeaderStyle}>
                          Bot
                        </th>

                        <th style={tableHeaderStyle}>
                          Status
                        </th>

                        <th style={tableHeaderStyle}>
                          Action
                        </th>

                      </tr>

                    </thead>

                    <tbody>

                      {candidates.map(
                        (candidate) => (

                          <tr
                            key={candidate.id}
                          >

                            <td style={tableCellStyle}>

                              <strong>
                                {candidate.name}
                              </strong>

                              <div
                                style={{
                                  fontSize: "13px",
                                  marginTop: "4px",
                                  opacity: 0.65,
                                }}
                              >
                                {candidate.email}
                              </div>

                            </td>

                            <td style={tableCellStyle}>
                              {candidate.resume_filename}
                            </td>

                            <td style={tableCellStyle}>

                              <strong>
                                {candidate.ai_risk_score}/100
                              </strong>

                              <div
                                style={{
                                  fontSize: "13px",
                                  marginTop: "4px",
                                  opacity: 0.65,
                                }}
                              >
                                {candidate.ai_classification}
                              </div>

                            </td>

                            <td style={tableCellStyle}>

                              <strong>
                                {candidate.bot_detected
                                  ? "Yes"
                                  : "No"}
                              </strong>

                            </td>

                            <td style={tableCellStyle}>

                              <strong>
                                {candidate.overall_status}
                              </strong>

                            </td>

                            <td style={tableCellStyle}>

                              <button
                                type="button"
                                className="primary-button"
                                disabled={loadingCandidate}
                                onClick={() =>
                                  openCandidate(
                                    candidate.id
                                  )
                                }
                              >
                                {loadingCandidate
                                  ? "Loading..."
                                  : "View Analysis →"}
                              </button>

                            </td>

                          </tr>

                        )
                      )}

                    </tbody>

                  </table>

                </div>

              )}

                </section>
              </>
            )}

            <button
              className="secondary-button dashboard-button"
              onClick={startAnotherApplication}
            >
              ← Analyze Another Candidate
            </button>

          </>
        )}

      </main>

    </div>
  );
}

const tableHeaderStyle = {
  textAlign: "left",
  padding: "14px 12px",
  borderBottom: "1px solid #e5e7eb",
  fontSize: "12px",
  textTransform: "uppercase",
  letterSpacing: "0.08em",
};

const tableCellStyle = {
  padding: "16px 12px",
  borderBottom: "1px solid #f0f0f0",
};

export default App;