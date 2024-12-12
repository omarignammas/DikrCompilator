import streamlit as st
import Pages.DikrApprend as DikrApprend
import Pages.Dikrbot as Dikrbot
import Pages.DikrCompiler as DikrCompiler
import Pages.DikrStatistics as DikrStatistics

def Functionalities():
    # Sidebar pour naviguer entre les pages
    page = st.sidebar.selectbox(
        "Choisissez une page :",
        ["DikrCompiler", "DikrBot", "DikrApprentissage", "DikrStatistics"]
    )

    # Navigation vers la page sélectionnée
    if page == "DikrCompiler":
        DikrCompiler.DikrCompiler()
    elif page == "DikrBot":
        Dikrbot.DikrBot()
    elif page == "DikrApprentissage":
        DikrApprend.DikrApprentissage()
    elif page == "DikrStatistics":
        DikrStatistics.DikrStatistics()

if __name__ == "__main__":
   Functionalities()





