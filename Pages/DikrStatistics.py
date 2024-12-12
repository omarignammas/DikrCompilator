import streamlit as st
from Methods.utils import show_statistics

def DikrStatistics():
      st.title("🟡 Statistiques des lectures 📊 ")
      st.markdown("---")
      show_statistics()