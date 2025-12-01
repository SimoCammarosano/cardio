import streamlit as st

st.set_page_config(page_title="Progetto tesi Simone Cammarosano MDA24/25", layout="centered")

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

# Titolo centrato
st.markdown("<h1 style='text-align: center;'>Progetto tesi Simone Cammarosano MDA24/25</h1>", unsafe_allow_html=True)

# CSS per centrare il bottone
st.markdown("""
<style>
div.stButton > button {
    display: block;
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# Bottone centrato
if st.button("Inizia da qui"):
    st.switch_page("pages/0_Home.py")
