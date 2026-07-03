import streamlit as st
import pandas as pd
import plotly.express as px
import asyncio
import tempfile
import os
import base64

st.set_page_config(
    page_title="Haiti Minimum Wage History | GlobalInternet.py",
    layout="wide",
    page_icon="🇭🇹"
)

# ---------- Custom Styling ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(145deg, #f5f0eb 0%, #e8e0d8 100%);
        color: #1a1a1a;
    }
    .main-title {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #003366, #1a5276);
        border-radius: 20px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-title h1 { margin: 0; font-size: 2.5rem; }
    .main-title p { margin: 0.5rem 0 0; font-size: 1.2rem; opacity: 0.9; }
    .stat-box {
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(5px);
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid #ccc;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }
    .stat-box .label { font-size: 0.9rem; color: #555; }
    .stat-box .value { font-size: 2rem; font-weight: 700; color: #003366; }
    .highlight-red { color: #cc0000; font-weight: 700; }
    .highlight-green { color: #006600; font-weight: 700; }
    .footer {
        margin-top: 3rem;
        text-align: center;
        font-size: 0.9rem;
        color: #666;
        border-top: 1px solid #ccc;
        padding-top: 1.5rem;
    }
    .stButton>button {
        background: #003366 !important;
        color: white !important;
        border-radius: 30px !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
    }
    .stButton>button:hover {
        background: #1a5276 !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
data = {
    "Year": ["1970s", "1980s", "1990s", "2000s", "2026"],
    "Nominal Wage (HTG/day)": [15, 15, 30, 70, 1000],
    "Real Value (relative to 1980)": [1.5, 1.0, 0.35, 0.18, 0.12],
    "Approx. USD/day": [3.00, 2.50, 1.80, 2.02, 7.70],
    "Purchasing Power (index)": [100, 60, 30, 18, 10],
}
df = pd.DataFrame(data)
df["Real Wage (1981 gourdes)"] = [15*1.5, 15*1.0, 30*0.35, 70*0.18, 1000*0.12]

# ---------- Title ----------
st.markdown("""
<div class="main-title">
    <h1>🇭🇹 Haiti Factory Workers' Minimum Wage</h1>
    <p>A Half‑Century of Broken Promises — From 15 Gourdes to 1,000 Gourdes, but Purchasing Power Collapsed</p>
</div>
""", unsafe_allow_html=True)

# ---------- Key Metrics ----------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="label">1970s Wage</div>
        <div class="value">15 HTG/day</div>
        <div style="font-size:0.9rem; color:#666;">~ $3.00 USD</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="label">2026 Wage</div>
        <div class="value">1,000 HTG/day</div>
        <div style="font-size:0.9rem; color:#666;">~ $7.70 USD</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="label">Real Wage Loss (vs 1980)</div>
        <div class="value" style="color:#cc0000;">-88%</div>
        <div style="font-size:0.9rem; color:#666;">Purchasing power collapsed</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- Data Table ----------
st.subheader("📊 Historical Wage Data")
st.dataframe(df.style.format({
    "Nominal Wage (HTG/day)": "{:,.0f}",
    "Real Wage (1981 gourdes)": "{:.2f}",
    "Purchasing Power (index)": "{:.0f}"
}), use_container_width=True)

# ---------- Chart ----------
st.subheader("📈 Nominal vs. Real Wage (Purchasing Power)")
fig = px.line(
    df,
    x="Year",
    y=["Nominal Wage (HTG/day)", "Purchasing Power (index)"],
    title="Nominal wage skyrockets, but purchasing power plummets",
    labels={"value": "Value", "variable": "Metric"},
    markers=True,
    color_discrete_map={
        "Nominal Wage (HTG/day)": "#003366",
        "Purchasing Power (index)": "#cc0000"
    }
)
fig.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_title="",
    yaxis_title="HTG / Index",
    template="plotly_white",
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Cost of Living Comparison ----------
st.markdown("---")
st.subheader("💰 The Cost of Living Reality")
st.markdown("""
In **Port-au-Prince**, the estimated monthly cost for a single person is **125,086 HTG**.
A factory worker earning 1,000 HTG/day for 26 days earns **26,000 HTG/month**.
That is only **~21%** of what it costs to live.
""")

col1, col2 = st.columns(2)
with col1:
    st.metric("Monthly Cost of Living", "125,086 HTG", delta=None)
with col2:
    st.metric("Monthly Factory Wage", "26,000 HTG", delta="-99,086 HTG", delta_color="inverse")

# ---------- Audio Narration (FULL SCRIPT) ----------
st.markdown("---")
st.subheader("🎧 Listen to the Full Story")

# Complete narration script covering title, history, data, cost of living, and call to action.
FULL_NARRATION = """
🇭🇹 Haiti Factory Workers' Minimum Wage.
A half-century of broken promises. From 15 gourdes to 1,000 gourdes, but purchasing power collapsed.

In the 1970s, a Haitian factory worker earned 15 gourdes per day, about three US dollars.
In the 1980s, the wage stayed at 15 gourdes, but inflation ate away its value. Purchasing power dropped by nearly half.
In the 1990s, the wage was doubled to 30 gourdes, but the gourde collapsed. By 1999, the real wage was worth 65 percent less than in 1980.
In the 2000s, the wage rose to 70 gourdes, but that was only worth about two US dollars.
Today, in 2026, the minimum wage for factory workers is 1,000 gourdes per day, about seven dollars and seventy cents US.

That sounds like progress, but the cost of living has skyrocketed. A single person needs one hundred and twenty-five thousand gourdes per month just to get by in Port-au-Prince. A factory worker earns only twenty-six thousand gourdes per month. That is barely one-fifth of what they need.

Fifty years of wage increases, but the worker's buying power has been destroyed. The promise of a living wage remains unfulfilled.

✊ Join the Movement for a Living Wage.
The workers who make the clothes we wear, who assemble the electronics we use, who fuel Haiti's industrial future — they deserve more than crumbs. They deserve a wage that reflects their humanity.

The time for change is now.

Built by Gesner Deslandes, Engineer-in-Chief at GlobalInternet.py.
Data sourced from historical records and official Haitian government announcements.
"""

async def generate_audio(text):
    try:
        import edge_tts
        voice = "en-US-GuyNeural"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            output_path = tmp.name
        comm = edge_tts.Communicate(text, voice)
        await comm.save(output_path)
        return output_path
    except Exception as e:
        st.error(f"Audio generation failed: {e}")
        return None

def play_audio(audio_path):
    if audio_path and os.path.exists(audio_path):
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width:100%;"></audio>', unsafe_allow_html=True)
        os.unlink(audio_path)

if st.button("🔊 Play Full Narration"):
    with st.spinner("Generating audio..."):
        audio_file = asyncio.run(generate_audio(FULL_NARRATION))
        if audio_file:
            play_audio(audio_file)
        else:
            st.error("Could not generate audio.")

st.caption("AI voice narrates the entire story – from the 1970s to the call for change.")

# ---------- Call to Action ----------
st.markdown("---")
st.markdown("""
### ✊ Join the Movement for a Living Wage

The workers who make the clothes we wear, who assemble the electronics we use, who fuel Haiti's industrial future — they deserve more than crumbs. They deserve a wage that reflects their humanity.

**The time for change is now.**
""")

# ---------- Footer ----------
st.markdown("""
<div class="footer">
    Built by <strong>Gesner Deslandes</strong>, Engineer‑in‑Chief at GlobalInternet.py<br>
    Data sourced from historical records and official Haitian government announcements.
</div>
""", unsafe_allow_html=True)
