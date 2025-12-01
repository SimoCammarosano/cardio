import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

#-----------Configurazione pagina dashboard------------
st.set_page_config(page_title="Grafici", page_icon="📊", layout="wide")

hide_menu_style = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

#-----------Sidebar personalizzata------------
with st.sidebar:
    if st.button("🏠 Home"):
        st.switch_page("0_Home.py")
    if st.button("🩺 Calcola rischio"):
        st.switch_page("pages/1_Predizione.py")
    st.markdown("📊 **Dashboard**")
    if st.button("🧍Confronto paziente"):
        st.switch_page("pages/3_Confronto.py")

st.title("📊 Analisi Grafica del Dataset")

#-----------Dati dal db------------
df = pd.read_csv("data/cardio_db.csv")

# Rimuovo OUTLIER estremi nel BMI
df = df[(df["BMI"] > 10) & (df["BMI"] < 60)]

df = df.dropna(subset=["age", "BMI", "cardio", "gender"])

# ------------------- FILTRI -------------------
col1, col2= st.columns(2)
with col1:
    with st.expander("Filtri"):
        col1, col2 = st.columns(2)

        sesso = col1.multiselect(
            "Genere",
            options=[1, 2],
            format_func=lambda x: "Donna" if x == 1 else "Uomo"
        )

        eta_range = col2.slider(
            "Età",
            int(df.age.min()), int(df.age.max()),
            (int(df.age.min()), int(df.age.max()))
        )

df_filtered = df.copy()

if sesso:
    df_filtered = df_filtered[df_filtered["gender"].isin(sesso)]

df_filtered = df_filtered[
    (df_filtered["age"] >= eta_range[0]) &
    (df_filtered["age"] <= eta_range[1])
]

# ------------------- Indicatori principali -------------------
st.subheader("Indicatori principali")
colA, colB, colC, colD = st.columns(4)

colA.metric("Pazienti", len(df_filtered))
colB.metric("Età media", f"{df_filtered.age.mean():.0f}")
colC.metric("BMI medio", f"{df_filtered.BMI.mean():.1f}")
colD.metric("Rischio medio (%)", f"{df_filtered.cardio.mean()*100:.1f}%")

st.markdown("---")

# ------------------- Distribuzioni -------------------
st.subheader("Distribuzioni cliniche")

#Prima riga

col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(df_filtered, x="age", nbins=30,
                       color_discrete_sequence=["#4a90e2"])
    fig.update_layout(showlegend=False, title="Distribuzione Età")
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.histogram(df_filtered, x="BMI", nbins=30,
                       color_discrete_sequence=["#7b8ba4"])
    fig.update_layout(showlegend=False, title="Distribuzione BMI")
    st.plotly_chart(fig, width="stretch")

# Seconda riga

col3, col4, col5 = st.columns(3)

with col3:
    fig = px.histogram(df_filtered, x="ap_hi", nbins=30,
                       color_discrete_sequence=["#9bb7d4"])
    fig.update_layout(showlegend=False, title="Pressione Sistolica (ap_hi)")
    st.plotly_chart(fig, width="stretch")

with col4:
    fig = px.histogram(df_filtered, x="cholesterol", nbins=3,
                       color_discrete_sequence=["#b0c4de"])
    fig.update_layout(showlegend=False, title="Colesterolo")
    st.plotly_chart(fig, width="stretch")

with col5:
    fig = px.histogram(df_filtered, x="gluc", nbins=3,
                       color_discrete_sequence=["#92a7c2"])
    fig.update_layout(showlegend=False, title="Glucosio")
    st.plotly_chart(fig, width="stretch")

st.markdown("---")

# ------------------- FUNZIONE % CARDIO -------------------
def percentuali(df, col):
    grouped = df.groupby(col)["cardio"].mean().reset_index()
    grouped["percentuale"] = grouped["cardio"] * 100
    return grouped

# ------------------- INCIDENZA CARDIACA -------------------
st.subheader("Incidenza rischio cardiaco (%)")

col1, col2 = st.columns(2)

# ---- Per fasce età
with col1:
    df_age_bins = df_filtered.copy()
    df_age_bins["fasce_età"] = pd.cut(df_age_bins["age"], bins=[0,30,45,60,75,120])
    df_age_bins["fasce_età"] = df_age_bins["fasce_età"].astype(str)
    p = percentuali(df_age_bins, "fasce_età")
    fig = px.bar(p, x="fasce_età", y="percentuale",
                 color_discrete_sequence=["#4a90e2"])
    fig.update_layout(title="Per fasce d’età", yaxis_title="% cardio")
    st.plotly_chart(fig, width="stretch")

# ---- Per genere
with col2:
    p = percentuali(df_filtered, "gender")
    p["gender"] = p["gender"].map({1:"Donna", 2:"Uomo"})
    fig = px.bar(p, x="gender", y="percentuale",
                 color_discrete_sequence=["#7b8ba4"])
    fig.update_layout(title="Per genere", yaxis_title="% cardio")
    st.plotly_chart(fig, width="stretch")

# Terza riga
col3, col4 = st.columns(2)

# ---- Per fasce BMI
with col3:
    df_bmi_bins = df_filtered.copy()
    df_bmi_bins["fasce_BMI"] = pd.qcut(df_bmi_bins["BMI"], q=4)
    df_bmi_bins["fasce_BMI"] = df_bmi_bins["fasce_BMI"].astype(str)  # FIX
    p = percentuali(df_bmi_bins, "fasce_BMI")
    fig = px.bar(p, x="fasce_BMI", y="percentuale",
                 color_discrete_sequence=["#9bb7d4"])
    fig.update_layout(title="Per fasce BMI", yaxis_title="% cardio")
    st.plotly_chart(fig, width="stretch")

# ---- Per glucosio
with col4:
    p = percentuali(df_filtered, "gluc")
    fig = px.bar(p, x="gluc", y="percentuale",
                 color_discrete_sequence=["#b0c4de"])
    fig.update_layout(title="Per glucosio", yaxis_title="% cardio")
    st.plotly_chart(fig, width="stretch")

st.markdown("---")

# ------------------- BOXPLOT CONFRONTI CARDIO -------------------
st.subheader("Confronto assenza di problemi cardiaci(0) e presenza di problemi cardiaci(1)")

# Prima riga boxplot
col1, col2 = st.columns(2)

with col1:
    fig = px.box(df_filtered, x="cardio", y="age",
                 color="cardio",
                 color_discrete_sequence=["#7b8ba4", "#4a90e2"],
                 labels={"cardio": "Rischio", "age": "Età"})
    fig.update_layout(title="Età vs rischio", showlegend=False)
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.box(df_filtered, x="cardio", y="BMI",
                 color="cardio",
                 color_discrete_sequence=["#7b8ba4", "#4a90e2"],
                 labels={"cardio": "Rischio", "BMI": "BMI"})
    fig.update_layout(title="BMI vs rischio", showlegend=False)
    st.plotly_chart(fig, width="stretch")

# Seconda riga boxplot
col3, col4 = st.columns(2)

with col3:
    fig = px.box(df_filtered, x="cardio", y="ap_hi",
                 color="cardio",
                 color_discrete_sequence=["#7b8ba4", "#4a90e2"],
                 labels={"cardio": "Rischio", "ap_hi": "Pressione Sistolica"})
    fig.update_layout(title="Pressione vs rischio", showlegend=False)
    st.plotly_chart(fig, width="stretch")

st.subheader("Dataset")
with st.expander(f"📄({len(df_filtered)} righe)"):
    st.dataframe(df_filtered, hide_index=True)


st.write("---")
