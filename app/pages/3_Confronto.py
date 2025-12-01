import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configurazione pagina confronto
st.set_page_config(page_title="Confronto Paziente", page_icon="🧍", layout="wide")


hide_menu_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# ------------------- Sidebar personalizzata -------------------
with st.sidebar:
    if st.button("🏠 Home"):
        st.switch_page("0_Home.py")
    if st.button("🩺 Calcola rischio"):
        st.switch_page("pages/1_Predizione.py")
    if st.button("📊 Dashboard"):
        st.switch_page("pages/2_Grafici.py")
    st.markdown("🧍 **Confronto Paziente**")

# ------------------- RECUPERO DATI PAZIENTE -------------------
last = st.session_state.get("last_values", None)

if last is None:
    st.warning("⚠️ Non sono presenti dati di un paziente. Torna nella pagina 'Calcolo rischio'.")
    if st.button("🩺 Calcola rischio", key="to_prediction"):
        st.switch_page("pages/1_Predizione.py")
    st.stop()

st.title("Confronta i tuoi risultati con il resto della popolazione")


# ------------------- CARICO DB -------------------
df = pd.read_csv("data/cardio_db.csv")
df = df[(df["BMI"] > 10) & (df["BMI"] < 60)]  # pulizia BMI

# ------------------- SEZIONE 1 — DATI DEL PAZIENTE -------------------

st.header("📌 Profilo del Paziente")

col1, col2, col3 = st.columns(3)

# --- Età ---
eta = last["age"]
mean_age = df["age"].mean()
if eta < mean_age - 5:
    age_status = ("🟢 Età sotto la media", "green")
elif eta > mean_age + 5:
    age_status = ("🟡 Età sopra la media", "orange")
else:
    age_status = ("🟢 Età nella media", "green")

with col1:
    st.metric("Età", f"{eta} anni")
    st.write(age_status[0])

# --- BMI ---
bmi = last["BMI"]
if bmi < 18.5:
    bmi_status = ("🔵 Sottopeso", "blue")
elif bmi < 25:
    bmi_status = ("🟢 Normopeso", "green")
elif bmi < 30:
    bmi_status = ("🟡 Sovrappeso", "orange")
else:
    bmi_status = ("🔴 Obesità", "red")

with col2:
    st.metric("BMI", f"{bmi:.1f}")
    st.write(bmi_status[0])

# --- Pressione ---
ap_hi = last["ap_hi"]
if ap_hi <= 120:
    press_status = ("🟢 Pressione normale", "green")
elif ap_hi < 140:
    press_status = ("🟡 Pre-ipertensione", "orange")
else:
    press_status = ("🔴 Pressione alta", "red")

with col3:
    st.metric("Pressione sistolica", f"{ap_hi} mmHg")
    st.write(press_status[0])


st.markdown("---")

# ------------------- SEZIONE 2 — GUIDA GRAFICI -------------------

st.header("📊 Confronto Grafico")

st.write("Ogni grafico mostra la distribuzione dei valori nella popolazione. Il **punto rosso** indica il tuo valore.")

# ------------------- GRAFICO 1 — ETÀ -------------------
st.subheader("📍 Dove ti trovi rispetto all’età della popolazione")

fig = px.histogram(df, x="age", nbins=30, color_discrete_sequence=["#4a90e2"])
fig.add_scatter(x=[eta], y=[0], mode="markers",
                marker=dict(size=16, color="red"),
                name="Tu")

st.plotly_chart(fig, width="stretch")

percentile_age = (df["age"] < eta).mean() * 100
st.write(f"➡ Sei più giovane del **{percentile_age:.1f}%** della popolazione.")

st.markdown("---")

# ------------------- GRAFICO 2 — BMI -------------------
st.subheader("📍 Dove ti trovi nel BMI della popolazione")

fig = px.histogram(df, x="BMI", nbins=30, color_discrete_sequence=["#7b8ba4"])
fig.add_scatter(x=[bmi], y=[0], mode="markers",
                marker=dict(size=16, color="red"),
                name="Tu")

st.plotly_chart(fig, width="stretch")

percentile_bmi = (df["BMI"] < bmi).mean() * 100
st.write(f"➡ Il tuo BMI è superiore a **{percentile_bmi:.1f}%** della popolazione.")

st.markdown("---")

# ------------------- GRAFICO 3 — PRESSIONE -------------------
st.subheader("📍 Pressione sistolica vs popolazione")

fig = px.histogram(df, x="ap_hi", nbins=30, color_discrete_sequence=["#9bb7d4"])
fig.add_scatter(x=[ap_hi], y=[0], mode="markers",
                marker=dict(size=16, color="red"),
                name="Tu")

st.plotly_chart(fig, width="stretch")

percentile_press = (df["ap_hi"] < ap_hi).mean() * 100
st.write(f"➡ La tua pressione sistolica è più alta del **{percentile_press:.1f}%** della popolazione.")

st.markdown("---")

# ------------------- SEZIONE — RADAR Paziente vs Media -------------------

st.header("Confronto Paziente vs Media del Campione")

def normalize(val, minv, maxv):
    # evita valori fuori dai limiti clinici
    val = max(min(val, maxv), minv)
    return (val - minv) / (maxv - minv)

# Variabili da confrontare
categories = ["Età", "BMI", "Pressione", "Colesterolo", "Glucosio"]

# Normalizzazione clinica fissa
norm_patient = [
    normalize(last["age"], 18, 100),          # Età reale
    normalize(last["BMI"], 10, 50),           # BMI clinico 10–50
    normalize(last["ap_hi"], 80, 200),        # Pressione sistolica 80–200
    normalize(last["cholesterol"], 1, 3),     # Colesterolo 1–3
    normalize(last["gluc"], 1, 3),            # Glucosio 1–3
]

norm_mean = [
    normalize(df["age"].mean(), 18, 100),
    normalize(df["BMI"].mean(), 10, 50),
    normalize(df["ap_hi"].mean(), 80, 200),
    normalize(df["cholesterol"].mean(), 1, 3),
    normalize(df["gluc"].mean(), 1, 3),
]

# Chiusura poligono
norm_patient += [norm_patient[0]]
norm_mean += [norm_mean[0]]
all_categories = categories + [categories[0]]

fig = go.Figure()

# Media
fig.add_trace(go.Scatterpolar(
    r=norm_mean,
    theta=all_categories,
    fill='toself',
    name='Media popolazione',
    line=dict(color="rgba(80, 90, 255, 0.8)", width=3)
))

# Paziente
fig.add_trace(go.Scatterpolar(
    r=norm_patient,
    theta=all_categories,
    fill='toself',
    name='Paziente',
    line=dict(color="rgba(255, 80, 80, 0.9)", width=3)
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            tickvals=[0, 0.5, 1],
            ticktext=["Basso", "Medio", "Alto"],
            gridcolor="lightgray",
            linecolor="gray",
        ),
    ),
    showlegend=True,
    height=550
)

st.plotly_chart(fig, width="stretch")


# ------------------- ANALISI TESTUALE-------------------


confronti = []

# Età
mean_age = df["age"].mean()
if last["age"] > mean_age + 5:
    confronti.append("• **Età:** superiore alla media del campione (🟡)")
elif last["age"] < mean_age - 5:
    confronti.append("• **Età:** inferiore alla media del campione (🟢)")
else:
    confronti.append("• **Età:** in linea con la media (🟢)")

# BMI
if last["BMI"] >= 30:
    confronti.append("• **BMI:** in fascia obesità (🔴)")
elif last["BMI"] >= 25:
    confronti.append("• **BMI:** in fascia sovrappeso (🟡)")
else:
    confronti.append("• **BMI:** in fascia salutare (🟢)")

# Pressione
if last["ap_hi"] >= 140:
    confronti.append("• **Pressione:** valore alto, da monitorare (🔴)")
elif last["ap_hi"] > 120:
    confronti.append("• **Pressione:** leggermente sopra la media (🟡)")
else:
    confronti.append("• **Pressione:** nella norma (🟢)")

# Colesterolo
if last["cholesterol"] == 3:
    confronti.append("• **Colesterolo:** molto alto (🔴)")
elif last["cholesterol"] == 2:
    confronti.append("• **Colesterolo:** sopra la norma (🟡)")
else:
    confronti.append("• **Colesterolo:** normale (🟢)")

# Glucosio
if last["gluc"] == 3:
    confronti.append("• **Glucosio:** molto alto (🔴)")
elif last["gluc"] == 2:
    confronti.append("• **Glucosio:** sopra la norma (🟡)")
else:
    confronti.append("• **Glucosio:** nella norma (🟢)")

st.write("\n".join(confronti))


st.write("---")
