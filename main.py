import streamlit as st
import DikrApprentissage ,Dikrbot , DikrCompiler , DikrStatistics

def main():
    page = st.sidebar.selectbox("Naviguer vers :", ["DikrCompiler", "Dikrbot", "DikrApprentissage", "DikrStatistics"])

    if page == "DikrCompiler":
      DikrCompiler.DikrCompiler()
    elif page == "Dikrbot":
      Dikrbot.DikrBot()
    elif page == "DikrApprentissage":
      DikrApprentissage.DikrApprentissage() 
    elif page == "DikrStatistics":
      DikrStatistics.DikrStatistics1()

if __name__ == "__main__":
    main()

