import streamlit as st
import pandas as pd
import plotly.express as px
import asyncio
import tempfile
import os
import base64

st.set_page_config(
    page_title="Historique du Salaire Minimum en Haïti | GlobalInternet.py",
    layout="wide",
    page_icon="🇭🇹"
)

# ---------- Style personnalisé ----------
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

# ---------- Données ----------
data = {
    "Décennie": ["1970", "1980", "1990", "2000", "2026"],
    "Salaire nominal (HTG/jour)": [15, 15, 30, 70, 1000],
    "Valeur réelle (par rapport à 1980)": [1.5, 1.0, 0.35, 0.18, 0.12],
    "Équivalent USD/jour": [3.00, 2.50, 1.80, 2.02, 7.70],
    "Pouvoir d'achat (indice)": [100, 60, 30, 18, 10],
}
df = pd.DataFrame(data)
df["Salaire réel (gourdes de 1981)"] = [15*1.5, 15*1.0, 30*0.35, 70*0.18, 1000*0.12]

# ---------- Titre ----------
st.markdown("""
<div class="main-title">
    <h1>🇭🇹 Salaire Minimum des Ouvriers d'Usine en Haïti</h1>
    <p>Un demi‑siècle de promesses non tenues — De 15 gourdes à 1 000 gourdes, mais le pouvoir d'achat s'est effondré</p>
</div>
""", unsafe_allow_html=True)

# ---------- Indicateurs clés ----------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="stat-box">
        <div class="label">Salaire – années 1970</div>
        <div class="value">15 HTG/jour</div>
        <div style="font-size:0.9rem; color:#666;">~ 3,00 USD</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="stat-box">
        <div class="label">Salaire – 2026</div>
        <div class="value">1 000 HTG/jour</div>
        <div style="font-size:0.9rem; color:#666;">~ 7,70 USD</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="label">Perte de pouvoir d'achat (vs 1980)</div>
        <div class="value" style="color:#cc0000;">-88 %</div>
        <div style="font-size:0.9rem; color:#666;">Le pouvoir d'achat s'est effondré</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ---------- Tableau des données ----------
st.subheader("📊 Données historiques des salaires")
st.dataframe(df.style.format({
    "Salaire nominal (HTG/jour)": "{:,.0f}",
    "Salaire réel (gourdes de 1981)": "{:.2f}",
    "Pouvoir d'achat (indice)": "{:.0f}"
}), use_container_width=True)

# ---------- Graphique ----------
st.subheader("📈 Salaire nominal vs. Salaire réel (pouvoir d'achat)")
fig = px.line(
    df,
    x="Décennie",
    y=["Salaire nominal (HTG/jour)", "Pouvoir d'achat (indice)"],
    title="Le salaire nominal s'envole, mais le pouvoir d'achat s'effondre",
    labels={"value": "Valeur", "variable": "Indicateur"},
    markers=True,
    color_discrete_map={
        "Salaire nominal (HTG/jour)": "#003366",
        "Pouvoir d'achat (indice)": "#cc0000"
    }
)
fig.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis_title="",
    yaxis_title="HTG / Indice",
    template="plotly_white",
    height=500,
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Comparaison avec le coût de la vie ----------
st.markdown("---")
st.subheader("💰 La réalité du coût de la vie")
st.markdown("""
À **Port‑au‑Prince**, le coût mensuel estimé pour une personne seule est de **125 086 HTG**.
Un ouvrier d'usine qui gagne 1 000 HTG/jour pendant 26 jours touche **26 000 HTG/mois**.
Cela ne représente que **~21 %** de ce qu'il faut pour vivre.
""")

col1, col2 = st.columns(2)
with col1:
    st.metric("Coût mensuel de la vie", "125 086 HTG", delta=None)
with col2:
    st.metric("Salaire mensuel d'usine", "26 000 HTG", delta="-99 086 HTG", delta_color="inverse")

# ---------- Narration audio complète (script en français) ----------
st.markdown("---")
st.subheader("🎧 Écouter l'histoire complète")

SCRIPT_NARRATION_FR = """
🇭🇹 Salaire minimum des ouvriers d'usine en Haïti.
Un demi-siècle de promesses non tenues. De 15 gourdes à 1 000 gourdes, mais le pouvoir d'achat s'est effondré.

Dans les années 1970, un ouvrier haïtien gagnait 15 gourdes par jour, environ trois dollars américains.
Dans les années 1980, le salaire est resté à 15 gourdes, mais l'inflation a rongé sa valeur. Le pouvoir d'achat a chuté de près de moitié.
Dans les années 1990, le salaire a doublé pour atteindre 30 gourdes, mais la gourde s'est effondrée. En 1999, le salaire réel valait 65 % de moins qu'en 1980.
Dans les années 2000, le salaire est monté à 70 gourdes, mais cela ne valait qu'environ deux dollars américains.
Aujourd'hui, en 2026, le salaire minimum pour les ouvriers d'usine est de 1 000 gourdes par jour, soit environ sept dollars soixante-dix américains.

Cela ressemble à un progrès, mais le coût de la vie a explosé. Une personne seule a besoin de cent vingt-cinq mille quatre-vingt-six gourdes par mois rien que pour vivre à Port-au-Prince. Un ouvrier d'usine ne gagne que vingt-six mille gourdes par mois. C'est à peine un cinquième de ce dont il a besoin.

Cinquante ans d'augmentations salariales, mais le pouvoir d'achat du travailleur a été anéanti. La promesse d'un salaire décent reste inachevée.

✊ Rejoignez le mouvement pour un salaire décent.
Les ouvriers qui fabriquent les vêtements que nous portons, qui assemblent les appareils électroniques que nous utilisons, qui alimentent l'avenir industriel d'Haïti – ils méritent plus que des miettes. Ils méritent un salaire qui reflète leur humanité.

Le moment du changement est venu.

Conçu par Gesner Deslandes, ingénieur en chef chez GlobalInternet.py.
Données issues des archives historiques et des annonces officielles du gouvernement haïtien.
"""

async def generer_audio(texte):
    try:
        import edge_tts
        voix = "fr-FR-DeniseNeural"  # voix féminine native française
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            chemin = tmp.name
        comm = edge_tts.Communicate(texte, voix)
        await comm.save(chemin)
        return chemin
    except Exception as e:
        st.error(f"Échec de la génération audio : {e}")
        return None

def lire_audio(chemin):
    if chemin and os.path.exists(chemin):
        with open(chemin, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
            st.markdown(f'<audio controls src="data:audio/mp3;base64,{b64}" autoplay style="width:100%;"></audio>', unsafe_allow_html=True)
        os.unlink(chemin)

if st.button("🔊 Écouter l'histoire complète"):
    with st.spinner("Génération de l'audio..."):
        fichier_audio = asyncio.run(generer_audio(SCRIPT_NARRATION_FR))
        if fichier_audio:
            lire_audio(fichier_audio)
        else:
            st.error("Impossible de générer l'audio.")

st.caption("La voix IA raconte toute l'histoire – des années 1970 à l'appel au changement.")

# ---------- Appel à l'action ----------
st.markdown("---")
st.markdown("""
### ✊ Rejoignez le mouvement pour un salaire décent

Les ouvriers qui fabriquent les vêtements que nous portons, qui assemblent les appareils électroniques que nous utilisons, qui alimentent l'avenir industriel d'Haïti – ils méritent plus que des miettes. Ils méritent un salaire qui reflète leur humanité.

**Le moment du changement est venu.**
""")

# ---------- Pied de page ----------
st.markdown("""
<div class="footer">
    Conçu par <strong>Gesner Deslandes</strong>, ingénieur en chef chez GlobalInternet.py<br>
    Données issues des archives historiques et des annonces officielles du gouvernement haïtien.
</div>
""", unsafe_allow_html=True)
