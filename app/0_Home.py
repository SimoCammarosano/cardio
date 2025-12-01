import streamlit as st

#-----------Configurazione pagina------------

st.set_page_config(
    page_title="Home",
    layout="centered"
)

hide_sidebar = """
<style>
/* Nasconde la sidebar */
[data-testid="stSidebar"] {
    display: none !important;
}

/* Espande il contenuto su tutta la pagina */
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# --- SPAZIO ---
st.write("")
st.write("")


st.title("Calcolatore di Rischio Cardiaco")

# --- SPAZIO ---
st.write("")
st.write("")

#-----------Expander per la navigazione tra le pagine------------

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    with st.expander("❤️ Predizione", expanded=True):
        st.write("Predizione del rischio cardiaco tramite Machine Learning.")
        if st.button("Vai →", key="vai_predizione"):
            st.switch_page("pages/1_Predizione.py")

with info_col2:
    with st.expander("📊 Dashboard", expanded=True):
        st.write("Esplora i valori del dataset e osserva le relazioni tra variabili.")
        if st.button("Vai →", key="vai_grafici"):
            st.switch_page("pages/2_Grafici.py")

with info_col3:
    with st.expander("📈 Confronto", expanded=True):
        st.write("Confronta i tuoi valori con quelli della popolazione del dataset.")
        if st.button("Vai →", key="vai_confronto"):
            st.switch_page("pages/3_Confronto.py")


# --- SPAZIO ---
st.write("")
st.write("")

# --- BOX DESCRITTIVO (BELLO SENZA CSS) ---
with st.expander("📘 Come funziona questa applicazione?", expanded=False):
    st.write(
        """
        Questa applicazione ti permette di:
        
        - Analizzare il dataset tramite grafici e statistiche  
        - Calcolare il rischio cardiaco usando un modello di Machine Learning (Logistic Regression)  
        - Confrontare i tuoi valori con quelli della popolazione del dataset 

        """
    )


st.write("---")
st.caption("di **Simone Cammarosano**")
