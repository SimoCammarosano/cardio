import sys
import streamlit as st
import pickle
import pandas as pd
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from utilis.feature_preprocessing import preprocess_input


#-----------Configurazione pagina------------
st.set_page_config(page_title="Calcolo rischio", page_icon="🩺", layout="wide")

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
    st.markdown("🩺 **Calcolo rischio**")
    if st.button("📊 Dashboard"):
        st.switch_page("pages/2_Grafici.py")
    if st.button("🧍Confronto paziente"):
        st.switch_page("pages/3_Confronto.py")


#-----------Caricamento modello ML e SCALER------------
@st.cache_resource # per evitare ricaricamenti multipli
def load_model():
    with open("model/model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_resource # per evitare ricaricamenti multipli
def load_scaler():
    with open("model/scaler.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()
scaler = load_scaler()


#-----------Titolo------------
st.title("Calcolatore di Rischio Cardiaco")

st.markdown("Inserisci i tuoi dati per ottenere una stima personalizzata del rischio cardiaco.")

st.write("")
st.write("")

# SEZIONE ANAGRAFICA
with st.container():
    st.subheader("👤 Informazioni Personali")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Età", 18, 100, 50)

    with col2:
        height = st.slider("Altezza (cm)", 120, 220, 170)

    with col3:
        weight = st.slider("Peso (kg)", 40, 200, 70)



st.write("")
st.write("")


#PRESSIONE ARTERIOSA
with st.container():
    st.subheader("🫀 Pressione Arteriosa")

    col1, col2 = st.columns(2)

    with col1:
        ap_hi = st.number_input(
            "Pressione sistolica (ap_hi)",
            min_value=80, max_value=250, value=120,
            help='mmHg'
        )

    with col2:
        ap_lo = st.number_input(
            "Pressione diastolica (ap_lo)",
            min_value=40, max_value=150, value=80,
            help='mmHg'
        )


st.write("")
st.write("")


#GENERE
with st.container():
    st.subheader("🚻 Genere")

    gender = st.radio(
        "Seleziona il genere",
        options=[1, 2],
        format_func=lambda x: "👩 Donna" if x == 1 else "👨 Uomo",
        horizontal=True
    )


st.write("")
st.write("")


#VALORI CLINICI
with st.container():
    st.subheader("🧪 Valori Clinici")

    col1, col2 = st.columns(2)

    with col1:
        cholesterol = st.radio(
            "Livello colesterolo",
            options=[1, 2, 3],
            horizontal=True,
            help="1: normale, 2: sopra la norma, 3: molto alto"
        )

    with col2:
        gluc = st.radio(
            "Livello glucosio",
            options=[1, 2, 3],
            horizontal=True,
            help="1: normale, 2: sopra la norma, 3: molto alto"
        )


st.write("")
st.write("")


#STILE DI VITA
with st.container():
    st.subheader("🏃 Stile di Vita")

    col1, col2, col3 = st.columns(3)

    with col1:
        smoke = st.radio(
            "Fumatore",
            options=[0, 1],
            format_func=lambda x: "Sì" if x == 1 else "No",
            horizontal=True
        )

    with col2:
        alco = st.radio(
            "Consumo di alcol",
            options=[0, 1],
            format_func=lambda x: "Sì" if x == 1 else "No",
            horizontal=True
        )

    with col3:
        active = st.radio(
            "Attività fisica",
            options=[0, 1],
            format_func=lambda x: "Sì" if x == 1 else "No",
            horizontal=True
        )


st.write("")
st.write("")



#  PREDIZIONE
if st.button("Calcola rischio"):

    #Simulo attesa
    with st.spinner("Sto calcolando il rischio..."):
        time.sleep(3)


    #Preprocessing
    X = preprocess_input(
        age, height, weight, ap_hi, ap_lo,
        gender, cholesterol, gluc, smoke, alco, active
    )

    #Scaling
    X_scaled = scaler.transform(X)

    #Predizione
    proba = model.predict_proba(X_scaled)[0][1]
    pred = model.predict(X_scaled)[0]

    #Output
    st.subheader("🎯 Risultato della Predizione")
    st.write(f"**Probabilità stimata di rischio cardiaco: {proba:.2%}**")

    if pred == 1:
        st.error("🔴 **Alto rischio**")
    else:
        st.success("🟢 **Basso rischio**")

    #Salvataggio per confronti futuri
    st.session_state["last_values"] = {
        "age": age,
        "height": height,
        "weight": weight,
        "BMI": round(weight / ((height/100)**2), 2),
        "ap_hi": ap_hi,
        "ap_lo": ap_lo,
        "gender": gender,
        "cholesterol": cholesterol,
        "gluc": gluc,
        "smoke": smoke,
        "alco": alco,
        "active": active,
        "predicted_risk": float(proba),
        "predicted_class": int(pred)
    }






#Sezione: Ultimi valori inseriti
if "last_values" in st.session_state:

    st.subheader("🧾 Ultimi valori inseriti")

    # Recupero dati
    d = st.session_state["last_values"]

    gender_str = "Donna 👩" if d.get("gender") == 1 else "Uomo 👨"
    smoke_str = "Sì" if d.get("smoke") == 1 else "No"
    alco_str = "Sì" if d.get("alco") == 1 else "No"
    active_str = "Sì" if d.get("active") == 1 else "No"

    st.info( #!!!LASCIARE QUESTA INDENTAZIONE!!!
        f"""**👤 Informazioni personali**
- Età: **{d.get('age')}**
- Altezza: **{d.get('height')} cm**
- Peso: **{d.get('weight')} kg**

**🫀 Pressione arteriosa**
- Sistolica: **{d.get('ap_hi')} mmHg**
- Diastolica: **{d.get('ap_lo')} mmHg**

**🚻 Genere**
- {gender_str}

**🧪 Valori clinici**
- Colesterolo: **{d.get('cholesterol')}**
- Glucosio: **{d.get('gluc')}**

**🏃 Stile di vita**
- Fumatore: **{smoke_str}**
- Alcol: **{alco_str}**
- Attività fisica: **{active_str}**
"""
    )

#-----------Bottone per andare alla pagina del confronto------------

    st.markdown("Confronta i tuoi risultati con il resto della popolazione del dataset")
    if st.button("🧍Confronto paziente", key="to_comparison"):
        st.switch_page("pages/3_Confronto.py")


st.write("---")
st.caption("Progetto tesi di **Simone Cammarosano** – MDA 2024/25")
