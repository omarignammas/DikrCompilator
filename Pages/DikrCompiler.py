import streamlit as st
import speech_recognition as sr
import pandas as pd
from Methods.utils import analyze_text_with_yacc , translate_expression , phonetic_feedback , spaced_repetition , spiritual_practices_suggestions

def DikrCompiler():
    # Interface Streamlit
   st.title("🟢 Dikr Compiler - Ayat al-Kursi 🕌") 
   st.markdown("---")
   image_path = 'Dikrco.webp'
    # Affichage de l'image
   st.image(image_path, caption='', use_container_width=True)

    # Ajouter une CSS pour ajuster la largeur et la hauteur
   st.markdown(f"""
    <style>
        .stImage img {{
            width: 200px;
            height: 200px;
        }}
    </style>
    """, unsafe_allow_html=True)
   mode = st.selectbox("Choisissez le mode d'entrée :", ("Texte", "Audio"))

   if mode == "Texte":
    # Mode texte
      user_input = st.text_area("Veuillez saisir le verset Ayat al-Kursi :", height=200)
      if st.button("Analyser Ayat al-Kursi"):
       if user_input:
        # Analyse du texte
        analysis_result = analyze_text_with_yacc(user_input)
        st.markdown(f"{analysis_result}", unsafe_allow_html=True)

        translated_fr, translated_en = translate_expression(user_input)
        st.markdown(f"**Traduction en français :** {translated_fr}")
        st.markdown(f"**Traduction en anglais :** {translated_en}")

        phonetic_errors = phonetic_feedback(user_input)
        if phonetic_errors:
            st.markdown(f"Erreurs phonétiques possibles : {', '.join(phonetic_errors)}")
        else:
            st.markdown("La prononciation semble correcte.")

        if spaced_repetition():
            st.markdown("Il est temps de revoir ce verset !")
        
        st.markdown(f"Suggestion spirituelle : {spiritual_practices_suggestions()}")

   elif mode == "Audio":
    # Mode audio
     def process_audio():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Veuillez lire le verset Ayat al-Kursi...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Ajuste pour le bruit ambiant

            # Configurer la durée et la sensibilité de l'écoute
            recognizer.pause_threshold = 2  # Augmenter la pause pour éviter les coupures prématurées
            audio = recognizer.listen(source, phrase_time_limit=120)

            try:
                transcript = recognizer.recognize_google(audio, language="ar")
                st.write(f"Texte transcrit : {transcript}")
                
                # Analyse et traduction
                analysis_result = analyze_text_with_yacc(transcript)
                st.markdown(f" {analysis_result}", unsafe_allow_html=True)

                translated_fr, translated_en = translate_expression(transcript)
                st.markdown(f"**Traduction en français :** {translated_fr}")
                st.markdown(f"**Traduction en anglais :** {translated_en}")

                phonetic_errors = phonetic_feedback(transcript)
                if phonetic_errors:
                    st.markdown(f"Erreurs phonétiques possibles : {', '.join(phonetic_errors)}")
                else:
                    st.markdown("La prononciation semble correcte.")

                if spaced_repetition():
                    st.markdown("Il est temps de revoir ce verset !")
                
                st.markdown(f"Suggestion spirituelle : {spiritual_practices_suggestions()}")
            except sr.UnknownValueError:
                st.error("La reconnaissance vocale n'a pas pu comprendre le discours.")
            except sr.RequestError:
                st.error("Erreur de connexion avec le service de reconnaissance vocale.")

     if st.button("Lire Ayat al-Kursi"):
        process_audio()

