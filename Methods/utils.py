import streamlit as st
import speech_recognition as sr
import ply.lex as lex
import ply.yacc as yacc
import time
import random
from datetime import datetime
import pandas as pd
import json
import os


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


def show_statistics():
    try:
        with open("readings_log.json", "r") as f:
            readings = json.load(f)
        df = pd.DataFrame(readings)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df["hour"] = df["timestamp"].dt.hour
        df["date"] = df["timestamp"].dt.date

        # Afficher le nombre de lectures par jour
        st.subheader("Lectures par jour")
        daily_readings = df.groupby("date").size()
        st.bar_chart(daily_readings)

        # Afficher le nombre de lectures par heure
        st.subheader("Lectures par heure")
        hourly_readings = df.groupby("hour").size()
        st.bar_chart(hourly_readings)
    except FileNotFoundError:
        st.error("Aucune donnée de lecture disponible.")


# Chemin du fichier de log
log_file = "readings_log.json"

def log_reading():
    # Récupérer l'heure actuelle au format ISO 8601
    now = datetime.now().isoformat()  # Inclut les fractions de secondes

    # Si le fichier de log n'existe pas, le créer avec une liste vide
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            json.dump([], f)

    # Lire les entrées existantes
    with open(log_file, "r") as f:
        log_data = json.load(f)

    # Ajouter un nouvel enregistrement avec le timestamp actuel
    log_data.append({"timestamp": now})

    # Sauvegarder les nouvelles entrées dans le fichier
    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=4)

# Fonction pour lire et convertir les timestamps
def parse_timestamps():
    if not os.path.exists(log_file):
        print("Le fichier de log est vide ou n'existe pas.")
        return

    with open(log_file, "r") as f:
        log_data = json.load(f)

    for entry in log_data:
        try:
            # Utiliser datetime.fromisoformat pour supporter les fractions de secondes
            timestamp = datetime.fromisoformat(entry["timestamp"])
            print("Timestamp converti :", timestamp)
        except ValueError as e:
            print(f"Erreur lors de la conversion du timestamp {entry['timestamp']}: {e}")

def learning_mode_with_audio(repetition_count):
    st.title("Mode Apprentissage")
    st.write("Ce mode vous aide à apprendre Ayat al-Kursi grâce à la récitation et à la reconnaissance vocale.")
    completed_repetitions = 0
    def process_audio_apprentissage():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Veuillez réciter Ayat al-Kursi...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Ajuster pour le bruit ambiant
            
            recognizer.pause_threshold = 2 
            audio = recognizer.listen(source, phrase_time_limit=120)  # Limite de temps d'écoute

            try:
                transcript = recognizer.recognize_google(audio, language="ar")
                st.write(f"Texte transcrit : {transcript}")
                analysis_result = analyze_text_with_yacc(transcript)
                st.markdown(f"{analysis_result}", unsafe_allow_html=True)

                # Vérification de l'exactitude
                if ayat_alkursi_correct in transcript:
                    return True  # Récitation correcte
                else:
                    return False  # Erreurs dans la récitation
            except sr.UnknownValueError:
                st.error("La reconnaissance vocale n'a pas pu comprendre le discours.")
                return False
            except sr.RequestError:
                st.error("Erreur de connexion avec le service de reconnaissance vocale.")
                return False

    for i in range(repetition_count):
        st.write(f"Répétition {i + 1} sur {repetition_count} :")
        if process_audio_apprentissage():
            st.success("Bravo ! Votre récitation est correcte.")
            completed_repetitions += 1
            log_reading()  # Journaliser cette récitation réussie
        else:
            st.warning("Votre récitation est incomplète ou contient des erreurs. Essayez à nouveau.")

        time.sleep(3)  # Pause entre les répétitions

    st.write(f"Apprentissage terminé. Récitations correctes : {completed_repetitions}/{repetition_count}.")
    if completed_repetitions == repetition_count:
        st.success("Félicitations pour avoir complété toutes les récitations avec succès !")
    elif completed_repetitions > 0:
        st.info("Continuez à pratiquer pour perfectionner votre récitation.")
