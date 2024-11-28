import streamlit as st
import speech_recognition as sr
import ply.lex as lex
import ply.yacc as yacc
import time
import random
from datetime import datetime

# Verset correct d'Ayat al-Kursi
ayat_alkursi_correct = (
    "الله لا اله الا هو الحي القيوم "
    "لا تاخذه سنه ولا نوم "
    "له ما في السماوات وما في الارض "
    "من ذا الذي يشفع عنده الا باذنه "
    "يعلم ما بين ايديهم وما خلفهم "
    "ولا يحيطون بشيء من علمه الا بما شاء "
    "وسع كرسيه السماوات والارض "
    "ولا يؤوده حفظهما وهو العلي العظيم"
)

# Dictionnaire de traduction (arabe vers français et anglais)
translations = {
    "الله": {"fr": "Allah", "en": "Allah"},
    "لا": {"fr": "ne", "en": "no/not"},
    "اله": {"fr": "dieu", "en": "god"},
    "الا": {"fr": "sauf", "en": "except"},
    "هو": {"fr": "il", "en": "He"},
    "الحي": {"fr": "le Vivant", "en": "the Ever-Living"},
    "القيوم": {"fr": "le Soutien éternel", "en": "the Sustainer"},
    "تاخذه": {"fr": "Il n'est affecté par", "en": "He is not affected by"},
    "سنه": {"fr": "une somnolence", "en": "a drowsiness"},
    "ولا نوم": {"fr": "ni un sommeil", "en": "nor sleep"},
    "له": {"fr": "A Lui", "en": "To Him"},
    "ما": {"fr": "ce qui", "en": "what"},
    "في": {"fr": "dans", "en": "in"},
    "السماوات": {"fr": "les cieux", "en": "the heavens"},
    "و": {"fr": "et", "en": "and"},
    "الارض": {"fr": "la terre", "en": "the earth"},
    "من": {"fr": "qui", "en": "who"},
    "ذا": {"fr": "celui", "en": "that"},
    "الذي": {"fr": "qui", "en": "who"},
    "يشفع": {"fr": "intercède", "en": "intercedes"},
    "عنده": {"fr": "près de Lui", "en": "with Him"},
    "الا باذنه": {"fr": "sauf par Sa permission", "en": "except by His permission"},
    "يعلم": {"fr": "Il sait", "en": "He knows"},
    "ما بين": {"fr": "ce qui est entre", "en": "what is between"},
    "ايديهم": {"fr": "leurs mains", "en": "their hands"},
    "وما خلفهم": {"fr": "et ce qui est derrière eux", "en": "and what is behind them"},
    "ولا يحيطون": {"fr": "et ils ne comprennent", "en": "and they do not encompass"},
    "بشيء": {"fr": "en rien", "en": "anything"},
    "من علمه": {"fr": "de Son savoir", "en": "of His knowledge"},
    "الا بما شاء": {"fr": "sauf ce qu'Il veut", "en": "except what He wills"},
    "وسع كرسيه": {"fr": "Son trône englobe", "en": "His Throne encompasses"},
    "السماوات": {"fr": "les cieux", "en": "the heavens"},
    "والارض": {"fr": "et la terre", "en": "and the earth"},
    "ولا يؤوده": {"fr": "et cela ne Lui pèse pas", "en": "and it does not burden Him"},
    "حفظهما": {"fr": "la préservation de ceux-ci", "en": "the preservation of them"},
    "وهو": {"fr": "et Il est", "en": "and He is"},
    "العلي": {"fr": "le Très-Haut", "en": "the Most High"},
    "العظيم": {"fr": "le Magnifique", "en": "the Mighty"},
}

# Token list
tokens = ('WORD',)

# Regular expression for tokens
def t_WORD(t):
    r'\S+'
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caractère invalide : {t.value[0]}")
    t.lexer.skip(1)

# Analyseur lexical de texte
lexer = lex.lex()

# Parser rules
def p_text(p):
    '''text : words'''
    p[0] = p[1]

def p_words(p):
    '''words : words WORD
             | WORD'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_error(p):
    print("Erreur de syntaxe")

parser = yacc.yacc()

# Fonction pour analyser un texte
correct_words = ayat_alkursi_correct.split()

def analyze_text_with_yacc(text):
    parsed_words = parser.parse(text)

    errors = []
    highlighted_text = ""
    order_errors = []

    for i, word in enumerate(parsed_words):
        if i >= len(correct_words) or word != correct_words[i]:
            errors.append(word)
            highlighted_text += f"<span style='color:red;'>{word}</span> "
        else:
            highlighted_text += f"{word} "

        if i < len(correct_words) and word != correct_words[i]:
            order_errors.append((word, correct_words[i]))

    highlighted_text = highlighted_text.strip()

    order_error_message = ""
    if order_errors:
        order_error_message = "Erreur d'ordre des mots :<br>"
        for incorrect, correct in order_errors:
            order_error_message += f"<span style='color:orange;font-weight: bold;'>Mauvais mot : {incorrect}  (devrait être {correct})</span><br>"

    if errors:
        missing_words = [word for word in correct_words if word not in parsed_words]
        st.markdown("-----")
        missing_words_message = f"<div style='background-color:white;font-weight: bold;border-radius: 8px; padding:18px;color:black;'>Vous avez besoin de ces mots : {', '.join(missing_words)}</div>"
        return f"Le texte contient des erreurs lexicales :  {', '.join(errors)}<br>Texte avec erreurs mises en évidence : {highlighted_text}<br>{order_error_message}<br>{missing_words_message}"
    else:
        return "<div style='background-color:green; color:white;margin:10px; padding:18px;border-radius: 8px;font-weight: bold;'>Le texte est correct.</div>"

# Fonction de traduction complète
def translate_expression(text):
    words = text.split()
    translated_fr = []
    translated_en = []
    st.markdown("-----")
    for word in words:
        if word in translations:
            translated_fr.append(translations[word]["fr"])
            translated_en.append(translations[word]["en"])
        else:
            translated_fr.append(f"[Traduction non disponible: {word}]")
            translated_en.append(f"[Translation not available: {word}]")
    
    translated_fr_expression = " ".join(translated_fr)
    translated_en_expression = " ".join(translated_en)
    
    return translated_fr_expression, translated_en_expression

# Fonction pour fournir un retour phonétique
def phonetic_feedback(transcript):
    # Ici, nous pourrions intégrer un modèle de phonétique (par exemple, phoneme matching ou un modèle plus complexe)
    errors = []
    for word in transcript.split():
        if word not in correct_words:
            errors.append(word)
    return errors

# Fonction de répétition espacée (simple exemple)
def spaced_repetition():
    last_review = st.session_state.get("last_review", None)
    if last_review:
        elapsed_time = (datetime.now() - last_review).total_seconds()
        interval = random.choice([3600, 86400, 604800])  # 1h, 1 jour, 1 semaine
        if elapsed_time > interval:
            return True
        else:
            return False
    return True

# Fonction pour les suggestions spirituelles
def spiritual_practices_suggestions():
    suggestions = [
        "Reprenez la récitation du verset et méditez sur ses significations.",
        "Essayez de prier avec une intention profonde de comprendre la signification du verset.",
        "Faites des invocations de protection après chaque récitation.",
    ]
    return random.choice(suggestions)

# Interface Streamlit
st.title("Dikr Bot - Ayat al-Kursi ")
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
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
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

        