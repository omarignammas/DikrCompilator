import streamlit as st
from datetime import datetime
import pandas as pd
from Methods.utils import learning_mode_with_audio 


def DikrApprentissage():
    st.title("🟢 Mode Apprentissage 📈")
    st.markdown("---")
    # Contenu de la section d'apprentissage
    repetition_count = st.number_input("Nombre de répétitions :", min_value=1, max_value=10, value=3)
    if st.button("Commencer l'apprentissage 🎯"):
        learning_mode_with_audio(repetition_count)

