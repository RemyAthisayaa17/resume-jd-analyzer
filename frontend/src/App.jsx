import { useState, useEffect } from "react";

const palette = {
  bg: "#1F0822",
  surface: "#2E1B3B",
  plum: "#814881",
  mauve: "#D180C8",
  terra: "#E77665",
  topaz: "#F9CE75",
  muted: "#AA78B4"
};

export default function App() {
  const [resume, setResume] = useState(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!resume || !jd) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("jd", jd);

    const res = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });

    setResult(await res.json());
    setLoading(false);
  };

  return (
    <div style={pageStyle}>
      {/* HERO */}
      <section style={sectionStyle}>
        <h1 style={heroTitle}>
          Candidate & Position Alignment
        </h1>
        <p style={heroSubtitle}>
          Upload profile and define requirements for strategic analysis.
        </p>

        <div style={inputGrid}>
          <div style={uploadBox}>
            {resume ? (
              <>
                <div style={pdfIconPremium}>PDF</div>
                <div style={{ color: palette.topaz, fontWeight: 600 }}>
                  {resume.name}
                </div>
              </>
            ) : (
              <input
                type="file"
                onChange={e => setResume(e.target.files[0])}
                style={fileInput}
              />
            )}
          </div>

          <textarea
            rows={4}
            value={jd}
            onChange={e => setJd(e.target.value)}
            placeholder="Enter position requirements…"
            style={textArea}
          />
        </div>

        <button onClick={analyze} disabled={loading} style={cta}>
          {loading ? "Analyzing…" : "Generate Strategic Insights"}
        </button>
      </section>

      {result && (
        <>
          {/* SCORE */}
          <section style={{ marginTop: 80, textAlign: "center" }}>
            <ScoreRing value={result.match_score} />
            <p style={scoreLabel}>Alignment Score</p>
            <p style={scoreMessage}>{result.score_message}</p>
          </section>

          {/* COMPETENCY */}
          <section style={{ ...sectionStyle, marginTop: 72 }}>
            <h3 style={sectionTitle}>Competency Breakdown</h3>

            <SkillBlock
              title="Matched Competencies"
              items={result.matched_skills}
              color={palette.mauve}
            />

            <SkillBlock
              title="Critical Gaps"
              items={result.missing_skills}
              color={palette.terra}
            />
          </section>

          {/* STRATEGY */}
          <section style={{ ...sectionStyle, marginTop: 72 }}>
            <h3 style={sectionTitle}>Strategic Recommendations</h3>
            {result.suggestions.map((s, i) => (
              <div key={i} style={strategyItem}>{s}</div>
            ))}
          </section>
        </>
      )}
    </div>
  );
}

/* ---------- COMPONENTS ---------- */

function ScoreRing({ value }) {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = value;
    const duration = 1200;
    const stepTime = 15;
    const increment = (end / duration) * stepTime;

    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        start = end;
        clearInterval(timer);
      }
      setProgress(parseFloat(start.toFixed(1)));
    }, stepTime);

    return () => clearInterval(timer);
  }, [value]);

  const radius = 100;
  const stroke = 10;
  const normalizedRadius = radius - stroke / 2;
  const circumference = normalizedRadius * 2 * Math.PI;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  return (
    <div style={{ position: "relative", width: radius * 2, height: radius * 2, margin: "0 auto" }}>
      <svg height={radius * 2} width={radius * 2} style={{ transform: "rotate(-90deg)" }}>
        <circle
          stroke="#3B224A"
          fill="transparent"
          strokeWidth={stroke}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
        <circle
          stroke={palette.topaz}
          fill="transparent"
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${circumference} ${circumference}`}
          strokeDashoffset={strokeDashoffset}
          r={normalizedRadius}
          cx={radius}
          cy={radius}
        />
      </svg>
      <span style={{
        position: "absolute",
        top: "50%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        fontSize: 56,
        fontWeight: 800,
        color: palette.topaz,
        animation: "pulse 1.2s ease-out"
      }}>
        {progress}%
      </span>

      {/* Pulse keyframes */}
      <style>{`
        @keyframes pulse {
          0% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.7; }
          50% { transform: translate(-50%, -50%) scale(1.05); opacity: 1; }
          100% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
        }
      `}</style>
    </div>
  );
}

function SkillBlock({ title, items, color }) {
  return (
    <div style={{ marginBottom: 28 }}>
      <h4 style={{ color, marginBottom: 10 }}>{title}</h4>
      <div style={pillWrap}>
        {items.length === 0
          ? <span style={{ opacity: 0.5 }}>None identified</span>
          : items.map((i, idx) => <span key={idx} style={pill}>{i}</span>)}
      </div>
    </div>
  );
}

/* ---------- STYLES ---------- */

const pageStyle = {
  minHeight: "100vh",
  background: palette.bg,
  color: palette.topaz,
  padding: 48,
  fontFamily: "Georgia, Inter, system-ui"
};

const sectionStyle = {
  background: palette.surface,
  borderRadius: 28,
  padding: 36,
  maxWidth: 1100,
  margin: "0 auto"
};

const heroTitle = {
  textAlign: "center",
  fontSize: 34,
  fontWeight: 700
};

const heroSubtitle = {
  textAlign: "center",
  color: palette.muted,
  marginTop: 6
};

const inputGrid = {
  display: "grid",
  gridTemplateColumns: "1fr 1.4fr",
  gap: 28,
  marginTop: 28
};

const uploadBox = {
  background: "#3B224A",
  borderRadius: 16,
  padding: 20,
  textAlign: "center",
  border: `1px solid ${palette.plum}`
};

const pdfIconPremium = {
  width: 50,
  height: 50,
  borderRadius: 12,
  background: `linear-gradient(145deg, #FFD966, #F9CE75)`,
  color: palette.bg,
  fontWeight: 800,
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  margin: "0 auto 10px",
  boxShadow: "0 4px 15px rgba(255, 206, 117, 0.4)"
};

const fileInput = { width: "100%", color: palette.topaz };

const textArea = {
  padding: 14,
  borderRadius: 16,
  background: "#3B224A",
  border: `1px solid ${palette.plum}`,
  color: palette.topaz,
  resize: "none"
};

const cta = {
  marginTop: 28,
  width: "100%",
  padding: 16,
  borderRadius: 18,
  background: palette.topaz,
  color: palette.bg,
  border: "none",
  fontWeight: 700,
  cursor: "pointer",
  boxShadow: "0 0 0px transparent",
  transition: "all 0.2s ease"
};

const scoreLabel = { marginTop: 14, color: palette.muted };
const scoreMessage = { marginTop: 6, fontSize: 15, opacity: 0.85 };
const sectionTitle = { marginBottom: 18 };
const pillWrap = { display: "flex", flexWrap: "wrap", gap: 10 };
const pill = { padding: "8px 14px", borderRadius: 999, background: "#3B224A", fontSize: 14 };
const strategyItem = { padding: "14px 0", borderBottom: `1px solid ${palette.plum}`, color: palette.muted };
