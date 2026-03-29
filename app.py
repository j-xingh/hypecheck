import streamlit as st
import joblib

st.set_page_config(
    page_title="HypeCheck",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_model():
    return joblib.load("model/model.pkl")

model = load_model()

if "headline" not in st.session_state:
    st.session_state.headline = ""

def clear_input():
    st.session_state.headline = ""

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@300;400;500;600&family=Inter:wght@300;400;500;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background-color: #1a1c1e !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── HIDE SIDEBAR TOGGLE ───────────────────── */
[data-testid="collapsedControl"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden; }

/* ── CENTER EVERYTHING ─────────────────────── */
.block-container {
    max-width: 680px !important;
    margin: 0 auto !important;
    padding: 52px 24px 80px !important;
}

/* ── STATUS CHIP ───────────────────────────── */
.pg-chip-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 32px;
}
.pg-chip {
    display: inline-flex; align-items: center; gap: 8px;
    background: #1e2123; border: 1px solid #252830;
    border-radius: 999px; padding: 5px 16px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem; color: #00d4ff; letter-spacing: 1.5px;
}
.ch-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #00d4ff; box-shadow: 0 0 7px #00d4ffaa;
    animation: blink 2s ease infinite; flex-shrink: 0;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.15} }

/* ── HERO ──────────────────────────────────── */
.hero-wrap {
    display: flex; flex-direction: column;
    align-items: center; text-align: center;
    margin-bottom: 40px;
}
.hero-logo-row {
    display: flex; align-items: center;
    justify-content: center;
    gap: 16px; margin-bottom: 14px;
}
.hero-logo-box {
    width: 64px; height: 64px; border-radius: 16px;
    background: #1e2123; border: 1px solid #2a2d35;
    display: flex; align-items: center; justify-content: center;
    box-shadow: 0 0 28px #00d4ff0e; flex-shrink: 0;
}
.pg-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 3.6rem; font-weight: 800;
    letter-spacing: -2px; line-height: 1;
    color: #f0f2f5;
}
.pg-title span { color: #00d4ff; }
.pg-sub {
    font-size: 1rem; color: #8a9ab0;
    line-height: 1.7; max-width: 480px;
    text-align: center; margin: 0 auto;
}

/* ── DIVIDER ───────────────────────────────── */
.pg-divider {
    height: 1px; background: #252830;
    margin: 32px 0;
}

/* ── INPUT LABEL ───────────────────────────── */
.inp-lbl {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.56rem; color: #5a6272;
    letter-spacing: 3px; text-transform: uppercase;
    margin-bottom: 8px; text-align: left;
}

/* ── TEXTAREA ──────────────────────────────── */
div[data-testid="stTextArea"] textarea {
    background: #1e2123 !important;
    border: 1px solid #2a2d35 !important;
    border-radius: 13px !important;
    color: #c8d0dc !important;
    font-size: 0.97rem !important;
    padding: 16px 18px !important;
    line-height: 1.65 !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    resize: none !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: #00d4ff44 !important;
    box-shadow: 0 0 0 3px #00d4ff0e !important;
}
div[data-testid="stTextArea"] textarea::placeholder {
    color: #3a4050 !important;
}

/* ── BUTTONS ───────────────────────────────── */
div[data-testid="stButton"] button[kind="primary"] {
    background: #00d4ff !important;
    color: #0d0f12 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 11px 28px !important;
    font-family: 'JetBrains Mono', monospace !important;
    box-shadow: 0 0 20px #00d4ff2a !important;
    width: 100% !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background: #33ddff !important;
    box-shadow: 0 0 32px #00d4ff55 !important;
}
div[data-testid="stButton"] button[kind="secondary"] {
    background: #1e2123 !important;
    color: #8a9ab0 !important;
    border: 1px solid #2a2d35 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    width: 100% !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: #3a4050 !important;
    color: #c8d0dc !important;
}

/* ── RESULT CARDS ──────────────────────────── */
.card-bait {
    background: #1c1518;
    border: 1px solid #3d202a;
    border-radius: 16px; padding: 28px 30px;
    margin: 28px 0; animation: rise 0.3s ease;
    position: relative; overflow: hidden;
}
.card-bait::before {
    content:""; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, #ff3366, transparent);
}
.card-real {
    background: #131c20;
    border: 1px solid #1a3545;
    border-radius: 16px; padding: 28px 30px;
    margin: 28px 0; animation: rise 0.3s ease;
    position: relative; overflow: hidden;
}
.card-real::before {
    content:""; position:absolute; top:0; left:0; right:0; height:2px;
    background: linear-gradient(90deg, transparent, #00d4ff, transparent);
}
@keyframes rise {
    from { opacity:0; transform:translateY(8px); }
    to   { opacity:1; transform:translateY(0); }
}

.chip-bait {
    display: inline-flex; align-items: center; gap: 7px;
    background: #ff336618; color: #ff6688;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.58rem; font-weight: 600;
    letter-spacing: 2.5px; text-transform: uppercase;
    padding: 5px 13px; border-radius: 999px;
    border: 1px solid #ff336633; margin-bottom: 14px;
}
.chip-real {
    display: inline-flex; align-items: center; gap: 7px;
    background: #00d4ff14; color: #00d4ff;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.58rem; font-weight: 600;
    letter-spacing: 2.5px; text-transform: uppercase;
    padding: 5px 13px; border-radius: 999px;
    border: 1px solid #00d4ff2a; margin-bottom: 14px;
}
.r-dot {
    width: 6px; height: 6px; border-radius: 50%;
    flex-shrink: 0; animation: blink 1.2s ease infinite;
}
.r-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.3rem; font-weight: 700;
    color: #e8ecf2; margin-bottom: 7px; line-height: 1.3;
}
.r-desc {
    font-size: 0.86rem; color: #8a9ab0;
    line-height: 1.65; margin-bottom: 22px;
}
.prob-row {
    display: flex; justify-content: space-between;
    margin-bottom: 9px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem;
}
.bar-track {
    background: #252830; border-radius: 999px;
    height: 5px; overflow: hidden;
}
.bar-bait {
    height: 5px; border-radius: 999px;
    background: linear-gradient(90deg, #cc2244, #ff4466);
}
.bar-real {
    height: 5px; border-radius: 999px;
    background: linear-gradient(90deg, #0099cc, #00d4ff);
}

/* ── EXAMPLES ──────────────────────────────── */
.sec-hdr {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.54rem; color: #5a6272;
    letter-spacing: 3px; text-transform: uppercase;
    margin: 44px 0 14px;
    display: flex; align-items: center; gap: 10px;
}
.sec-hdr::after {
    content:""; flex:1; height:1px; background:#252830;
}
.ex-card {
    background: #1e2123; border: 1px solid #252830;
    border-radius: 11px; padding: 14px 15px; margin-bottom: 8px;
    transition: border-color 0.15s;
}
.ex-card:hover { border-color: #2a3040; }
.ex-tx { font-size: 0.83rem; color: #8a9ab0; line-height: 1.45; }

/* ── WARN + FOOTER ─────────────────────────── */
.warn-box {
    background: #1e1c18; border: 1px solid #2e2a1e;
    border-radius: 10px; padding: 13px 17px; margin: 14px 0;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem; color: #9a8a5a;
}
.pg-footer {
    margin-top: 64px; padding-top: 18px;
    border-top: 1px solid #252830;
    display: flex; justify-content: space-between;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.6rem; color: #454a55;
}
</style>
""", unsafe_allow_html=True)

# ── SPEEDO SVG ────────────────────────────────────────────────
SPEEDO = """<svg width="44" height="34" viewBox="0 0 52 40" fill="none">
  <defs>
    <linearGradient id="ag" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%"   stop-color="#00ffaa"/>
      <stop offset="38%"  stop-color="#00d4ff"/>
      <stop offset="72%"  stop-color="#ffcc00"/>
      <stop offset="100%" stop-color="#ff3366"/>
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="1.2" result="b"/>
      <feMerge><feMergeNode in="b"/>
      <feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <line x1="6"  y1="33" x2="9"  y2="28"
        stroke="#2a2d35" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="14" y1="15" x2="18" y2="19"
        stroke="#2a2d35" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="26" y1="9"  x2="26" y2="14"
        stroke="#2a2d35" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="38" y1="15" x2="34" y2="19"
        stroke="#2a2d35" stroke-width="1.5" stroke-linecap="round"/>
  <line x1="46" y1="33" x2="43" y2="28"
        stroke="#2a2d35" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M5 35 A21 21 0 0 1 47 35"
        stroke="#252830" stroke-width="5"
        stroke-linecap="round" fill="none"/>
  <path d="M5 35 A21 21 0 0 1 47 35"
        stroke="url(#ag)" stroke-width="3.5"
        stroke-linecap="round" fill="none" filter="url(#glow)"/>
  <line x1="26" y1="35" x2="39" y2="15"
        stroke="#e8ecf0" stroke-width="2" stroke-linecap="round"/>
  <circle cx="26" cy="35" r="4.2"
          fill="#1e2123" stroke="#00d4ff" stroke-width="1.5"/>
  <circle cx="26" cy="35" r="1.8" fill="#00d4ff"/>
</svg>"""

# ── MAIN ──────────────────────────────────────────────────────

# Status chip — centered
st.markdown("""
<div class="pg-chip-wrap">
    <div class="pg-chip">
        <div class="ch-dot"></div>
        MODEL ACTIVE &nbsp;·&nbsp; NAIVE BAYES &nbsp;·&nbsp; 95.6% ACC
    </div>
</div>""", unsafe_allow_html=True)

# Hero — centered
st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-logo-row">
        <div class="hero-logo-box">{SPEEDO}</div>
        <div class="pg-title">Hype<span>Check</span></div>
    </div>
    <p class="pg-sub">
        Paste any news headline below. Our machine learning model
        analyses it instantly and tells you whether it's engineered
        to manipulate, or genuine journalism.
    </p>
</div>
<div class="pg-divider"></div>
""", unsafe_allow_html=True)

# Input label
st.markdown('<div class="inp-lbl">Headline Input</div>',
            unsafe_allow_html=True)

# Text area
headline = st.text_area(
    label="",
    height=110,
    placeholder="Paste a news headline here...",
    label_visibility="collapsed",
    key="headline"
)

# Buttons
c1, c2 = st.columns([1, 1])
with c1:
    predict_btn = st.button("Analyse", type="primary",
                            use_container_width=True)
with c2:
    st.button("Clear", type="secondary",
              use_container_width=True,
              on_click=clear_input)

# ── RESULT ────────────────────────────────────────────────────
if predict_btn and st.session_state.headline.strip():
    pred   = model.predict([st.session_state.headline])[0]
    proba  = model.predict_proba([st.session_state.headline])[0]
    bait_p = round(proba[1] * 100, 1)
    real_p = round(proba[0] * 100, 1)

    if pred == 1:
        st.markdown(f"""
        <div class="card-bait">
            <div class="chip-bait">
                <div class="r-dot" style="background:#ff3366;"></div>
                Clickbait Detected
            </div>
            <div class="r-title">
                This headline is engineered to manipulate.
            </div>
            <div class="r-desc">
                Emotional triggers, vague language, or a deliberate
                curiosity gap — crafted to bait the click rather
                than inform the reader.
            </div>
            <div class="prob-row">
                <span style="color:#ff5577;">Clickbait probability</span>
                <span style="color:#e0e4ea;font-weight:600;">{bait_p}%</span>
            </div>
            <div class="bar-track">
                <div class="bar-bait" style="width:{bait_p}%"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card-real">
            <div class="chip-real">
                <div class="r-dot" style="background:#00d4ff;"></div>
                Signal Clear
            </div>
            <div class="r-title">
                This headline appears to be genuine news.
            </div>
            <div class="r-desc">
                Direct, factual language — no emotional manipulation,
                no curiosity baiting. Consistent with real journalism.
            </div>
            <div class="prob-row">
                <span style="color:#00d4ff;">Legitimate probability</span>
                <span style="color:#e0e4ea;font-weight:600;">{real_p}%</span>
            </div>
            <div class="bar-track">
                <div class="bar-real" style="width:{real_p}%"></div>
            </div>
        </div>""", unsafe_allow_html=True)

elif predict_btn:
    st.markdown("""
    <div class="warn-box">
        &gt; No input detected — please enter a headline first.
    </div>""", unsafe_allow_html=True)

# ── EXAMPLES ─────────────────────────────────────────────────
st.markdown('<div class="sec-hdr">Sample Headlines</div>',
            unsafe_allow_html=True)

examples = [
    ("You Won't Believe What This Celebrity Did Next", "bait"),
    ("RBI holds repo rate steady at 6.5%",             "real"),
    ("10 Shocking Things That Happen While You Sleep", "bait"),
    ("Supreme Court rules on landmark privacy case",   "real"),
    ("This One Weird Trick Will Change Your Life",     "bait"),
    ("India GDP growth rises to 7.2% in Q3 2025",     "real"),
    ("23 Things Only 90s Kids Will Remember",          "bait"),
    ("Scientists confirm water ice on Moon south pole","real"),
]

col_a, col_b = st.columns(2)
for i, (text, kind) in enumerate(examples):
    with (col_a if i % 2 == 0 else col_b):
        tag_color = "#ff556688" if kind == "bait" else "#00d4ff66"
        tag_text  = "// clickbait" if kind == "bait" else "// legitimate"
        st.markdown(f"""
        <div class="ex-card">
            <div style="font-family:'JetBrains Mono',monospace;
                        font-size:0.52rem;letter-spacing:2px;
                        text-transform:uppercase;color:{tag_color};
                        margin-bottom:5px;">{tag_text}</div>
            <div class="ex-tx">{text}</div>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("""
<div class="pg-footer">
    <span>HypeCheck - College ML Project · 2026</span>
    <span>Naive Bayes · TF-IDF · Scikit-learn · Streamlit</span>
</div>""", unsafe_allow_html=True)