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

# Fonction pour journaliser la récitation dans le fichier JSON
def log_reading():
    # Récupérer l'heure actuelle au format ISO
    now = datetime.now().isoformat()  # Formater l'heure au format ISO 8601

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
def learning_mode_with_audio(completed_repetitions):
    st.title("Mode Apprentissage")
    st.write("Ce mode vous aide à apprendre Ayat al-Kursi grâce à la récitation et à la reconnaissance vocale.")



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

page = st.sidebar.selectbox("Naviguer vers :", ["Accueil","DikrBot", "Apprentissage", "Statistiques des lectures"])

if page == "Accueil":
    # Interface Streamlit
   st.title("Dikr Compiler - Ayat al-Kursi ") 
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
elif page == "Apprentissage":
    st.title("Mode Apprentissage")
    # Contenu de la section d'apprentissage
    repetition_count = st.number_input("Nombre de répétitions :", min_value=1, max_value=10, value=3)
    completed_repetitions = 0
    if st.button("Commencer l'apprentissage"):
        learning_mode_with_audio(completed_repetitions)
elif page == "Statistiques des lectures":
    st.title("Statistiques des lectures")
    show_statistics()

elif page == "DikrBot":
    st.markdown(
        """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <style>
            .title-container {
                display: flex;
                align-items: center;
                justify-content: center;
                margin-top: 20px;
            }
            .title {
                font-size: 30px;
                font-weight: bold;
                color: #FFFFFF;
                margin-right: 15px;
            }
            lottie-player {
                width: 50px;
                height: 50px;
            }
        </style>
        <div class="title-container">
            <div class="title">Dikr Bot - مساعدك لآيات الذكر</div>
            <lottie-player
                src="https://assets9.lottiefiles.com/private_files/lf30_editor_40zqjokg.json"
                background="transparent"
                speed="1"
                loop
                autoplay>
            </lottie-player>
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown("---")


    def generate_response(user_input):
     normalized_input = user_input.strip().lower()

     if normalized_input == "ايه الكرسي":

        return "آية الكرسي هي: \"اللّهُ لا إِلٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ، لا تَأخُذُهُ سِنَةٌ وَلَا نَوْمٌ، لَهُ مَا فِي السَّمَاوَاتِ وَمَا فِي الْأَرْضِ. مَن ذَا الَّذِي يَشْفَعُ عِندَهُ إِلَّا بِإِذْنِهِ؟ يَعْلَمُ مَا بَيْنَ أَيْدِيهِمْ وَمَا خَلْفَهُمْ، وَلَا يُحِيطُونَ بِشَيْءٍ مِّنْ عِلْمِهِ إِلَّا بِمَا شَاءَ. وَسِعَ كُرْسِيُّهُ السَّمَاوَاتِ وَالْأَرْضَ، وَلَا يَئُودُهُ حِفْظُهُمَا، وَهُوَ الْعَلِيُّ الْعَظِيمُ.\" (البقرة 255)."
   
     elif normalized_input == "الفاتحه":

        return """سورة الفاتحة هي: \"الْحَمْدُ لِلّهِ رَبِّ الْعَالَمِينَ، الرَّحْمَـٰنِ الرَّحِيمِ، مَالِكِ يَوْمِ الدِّينِ، إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ، اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ، صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ.
            سورة الفاتحة تُعتبر السورة الأولى في القرآن الكريم وتجمع معاني التوحيد والدعاء بالهداية. تُقرأ في كل ركعة من الصلاة."""
 
     elif normalized_input == "معنى ايه الكرسي":
        
        return  """آية الكرسي تبرز عظمة الله وتفرده بالملك والعلم المطلق. تشير إلى أن الله هو الحي القيوم الذي لا تأخذه سنة ولا نوم.
            معنى آية الكرسي يبيّن قوة الله وسلطانه وحفظه للكون. الله يعلم ما بين أيدينا وما خلفنا ولا يحيطون بشيء من علمه إلا بما شاء.\n
            آية الكرسي تحفظ المسلم من الشرور وتبعث الطمأنينة. تُعتبر تلاوتها من أسباب الحماية من الأذى.\n
            قراءة آية الكرسي بعد كل صلاة تجلب البركة والحماية حتى الصلاة التالية.\n
            آية الكرسي تبرز عظمة الله وسلطانه وحفظه للكون بأكمله.\n
            تلاوة آية الكرسي قبل النوم تمنح الطمأنينة وتحفظ من الأذى."""
    

     elif normalized_input == "فضل ايه الكرسي":
      
        return   """فضل آية الكرسي عظيم، فهي تحفظ المسلم من الشرور وتُعتبر من أقوى آيات الحفظ والتحصين. يُستحب قراءتها في أوقات متعددة للحماية.",
            قراءة آية الكرسي بعد كل صلاة تجلب البركة والحفظ حتى الصلاة التالية، وتمنح القارئ الطمأنينة والسكينة.\n
            تُعتبر آية الكرسي وسيلة لحفظ النفس والأهل، وتوصى بقراءتها قبل النوم لحماية الإنسان من الأذى.\n
            آية الكرسي تُعين المسلم على تذكر عظمة الله وسلطانه، مما يعزز الإيمان واليقين بالله."""
   
    
     elif normalized_input == "تفسير الفاتحه" or normalized_input == "تفسير سوره الفاتحه":
           return """بِسْمِ اللهِ الرَّحْمنِ الرَّحِيمِ (1)
            \nسورة الفاتحة سميت هذه السورة بالفاتحة; لأنه يفتتح بها القرآن العظيم, وتسمى المثاني; لأنها تقرأ في كل ركعة, ولها أسماء أخر. أبتدئ قراءة القرآن باسم الله مستعينا به, (اللهِ) علم على الرب -تبارك وتعالى- المعبود بحق دون سواه, وهو أخص أسماء الله تعالى, ولا يسمى به غيره سبحانه. (الرَّحْمَنِ) ذي الرحمة العامة الذي وسعت رحمته جميع الخلق, (الرَّحِيمِ) بالمؤمنين, وهما اسمان من أسمائه تعالى، يتضمنان إثبات صفة الرحمة لله تعالى كما يليق بجلاله.
            الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ (2)
            \n(الحَمْدُ للهِ رَبِّ العَالَمِينَ) الثناء على الله بصفاته التي كلُّها أوصاف كمال, وبنعمه الظاهرة والباطنة، الدينية والدنيوية، وفي ضمنه أَمْرٌ لعباده أن يحمدوه, فهو المستحق له وحده, وهو سبحانه المنشئ للخلق, القائم بأمورهم, المربي لجميع خلقه بنعمه, ولأوليائه بالإيمان والعمل الصالح.
            الرَّحْمَنِ الرَّحِيمِ (3)
            \n(الرَّحْمَنِ) الذي وسعت رحمته جميع الخلق, (الرَّحِيمِ), بالمؤمنين, وهما اسمان من أسماء الله تعالى.
            مَالِكِ يَوْمِ الدِّينِ (4)
            \nوهو سبحانه وحده مالك يوم القيامة, وهو يوم الجزاء على الأعمال. وفي قراءة المسلم لهذه الآية في كل ركعة من صلواته تذكير له باليوم الآخر, وحثٌّ له على الاستعداد بالعمل الصالح, والكف عن المعاصي والسيئات.
            إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ (5)
            \nإنا نخصك وحدك بالعبادة, ونستعين بك وحدك في جميع أمورنا, فالأمر كله بيدك, لا يملك منه أحد مثقال ذرة. وفي هذه الآية دليل على أن العبد لا يجوز له أن يصرف شيئًا من أنواع العبادة كالدعاء والاستغاثة والذبح والطواف إلا لله وحده, وفيها شفاء القلوب من داء التعلق بغير اله, ومن أمراض الرياء والعجب, والكبرياء.
            اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ (6)
            \nدُلَّنا, وأرشدنا, ووفقنا إلى الطريق المستقيم, وثبتنا عليه حتى نلقاك, وهو الإسلام، الذي هو الطريق الواضح الموصل إلى رضوان الله وإلى جنته, الذي دلّ عليه خاتم رسله وأنبيائه محمد صلى الله عليه وسلم, فلا سبيل إلى سعادة العبد إلا بالاستقامة عليه.
            صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلا الضَّالِّينَ (7)
            طريق الذين أنعمت عليهم من النبيين والصدِّيقين والشهداء والصالحين, فهم أهل الهداية والاستقامة, ولا تجعلنا ممن سلك طريق المغضوب عليهم, الذين عرفوا الحق ولم يعملوا به, وهم اليهود, ومن كان على شاكلتهم, والضالين, وهم الذين لم يهتدوا, فضلوا الطريق, وهم النصارى, ومن اتبع سنتهم. وفي هذا الدعاء شفاء لقلب المسلم من مرض الجحود والجهل والضلال, ودلالة على أن أعظم نعمة على الإطلاق هي نعمة الإسلام, فمن كان أعرف للحق وأتبع له, كان أولى بالصراط المستقيم, ولا ريب أن أصحاب رسول الله صلى الله عليه وسلم هم أولى الناس بذلك بعد الأنبياء عليهم السلام, فدلت الآية على فضلهم, وعظيم منزلتهم, رضي الله عنهم. ويستحب للقارئ أن يقول في الصلاة بعد قراءة الفاتحة: (آمين), ومعناها: اللهم استجب, وليست آية من سورة الفاتحة باتفاق العلماء; ولهذا أجمعوا على عدم كتابتها في المصاحف."""
        
        
     elif normalized_input == "متى تقرا ايه الكرسي":       
        return """تقرأ آية الكرسي بعد كل صلاة وقبل النوم للحفظ والتحصين.
                يمكن قراءة آية الكرسي في أي وقت، لكن لها فضل خاص بعد الصلوات وقبل النوم,
                يُفضل قراءتها بعد صلاة الفجر والمغرب للحفظ."""
        
     elif normalized_input == "ماذا تعني الفاتحه":
       
            return """الفاتحة هي السورة التي تبدأ بها الصلاة وتسمى أم الكتاب.
             سورة الفاتحة تشمل معاني الثناء على الله وطلب الهداية.
             الفاتحة تركز على أهمية العبادة والدعاء لله."""
 
     else:
        return ("عذرًا، لا أستطيع فهم سؤالك. من فضلك اختر من بين الخيارات التالية: \n"
                "- آية الكرسي \n"
                "- الفاتحة \n"
                "- معنى آية الكرسي \n"
                "- فضل آية الكرسي \n"
                "- تفسير الفاتحة \n"
                "- متى تقرأ آية الكرسي \n"
                "- ماذا تعني الفاتحة")

                # Initialize the recognizer
    recognizer = sr.Recognizer()

    # Function to capture speech and convert to text
    def recognize_speech():
    # Créer des conteneurs pour les messages "Listening..." et "Processing..."
     listening_message = st.empty()
     processing_message = st.empty()
    
     with sr.Microphone() as source:
        # Afficher le message Listening
        listening_message.markdown(f'<div style="width: 715px; background-color: #5F9EA0; color: white; font-weight: bold; padding: 15px; border-radius: 8px; margin: 10px; text-align: center;">Listening...</div>', unsafe_allow_html=True)
        
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            
            # Attendre quelques secondes avant de cacher le message Listening
            time.sleep(1)
            listening_message.empty()

            # Afficher le message Processing
            processing_message.markdown(f'<div style="width: 715px; background-color: #B0C4DE ; color: black; font-weight: bold; padding: 15px; border-radius: 8px; margin: 10px; text-align: center;">Processing...</div>', unsafe_allow_html=True)
            
            query = recognizer.recognize_google(audio, language='ar')
            
            # Attendre quelques secondes avant de cacher le message Processing
            time.sleep(1)
            processing_message.empty()

            # Afficher le message de réponse
            st.markdown(f'<div style="width: 715px; background-color: #45c82b; padding: 15px; border-radius: 8px; margin: 10px; color: white; text-align: center;"><b>You said : {query}</b></div>', unsafe_allow_html=True)
            
            return query
            
        except sr.UnknownValueError:
            # Attendre avant d'afficher le message d'erreur
            time.sleep(1)
            processing_message.empty()
            st.markdown(f'<div style="width: 715px; background-color: #ff4040; color: white; font-weight: bold; padding: 30px; border-radius: 8px; margin: 10px; text-align: center;">Sorry, I could not understand the audio.</div>', unsafe_allow_html=True)
            return ""
        except sr.RequestError:
            # Attendre avant d'afficher l'erreur de connexion
            time.sleep(1)
            processing_message.empty()
            st.markdown(f'<div style="width: 715px; background-color: #ff8f66; color: white; font-weight: bold; padding: 30px; border-radius: 8px; margin: 10px; text-align: center;">Request failed; please check your internet connection.</div>', unsafe_allow_html=True)
            return ""
        
    # Initialiser l'état de session pour l'historique des messages
    if "messages" not in st.session_state:
     st.session_state.messages = []


# Créer un conteneur principal pour contrôler la largeur
    with st.container(): 
     for message in st.session_state.messages:
        # Utiliser un conteneur avec une largeur spécifiée pour l'affichage
        st.markdown(
            f'<div style="width: 700px; background-color: #808080; padding: 15px; border-radius: 8px; margin: 10px; color: white;">{message["content"]}</div>',
            unsafe_allow_html=True
        )

    # Ajouter un espace pour séparer les messages de la zone d'entrée
    st.markdown("---")

    # Créer un conteneur horizontal pour le bouton et l'entrée de texte
    col1, col2 = st.columns([1,4])  # Ajustez les proportions pour modifier la largeur des colonnes

    with col1:
    # Bouton de reconnaissance vocale
     if st.button("Voice Record"):
        user_query = recognize_speech()
        user_input = user_query.strip().lower()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").markdown(
        f"""
        <div style="width: 700px; background-color: #E9ECEF; padding: 15px; border-radius: 8px; margin: auto; color: #000;">
            {user_input}
        </div>
        """, unsafe_allow_html=True
    )

            # Générer et afficher la réponse
            response = generate_response(user_input)
            placeholder = st.chat_message("assistant").markdown("")
            full_response = ""

            # Loop to display the response with a simulated typing effect
            for word in response.split():
                full_response += word + " "
                time.sleep(0.08)  # Simuler un délai de saisie
                # Update the placeholder with a styled container for width control
                placeholder.markdown(
                    f"""
                    <div style="width: 700px; background-color: #E9ECEF; padding: 15px; border-radius: 8px; margin: auto; color: #000;">
                        {full_response}
                    </div>
                    """, unsafe_allow_html=True
                )

            # Ajouter la réponse à l'historique
            st.session_state.messages.append({"role": "assistant", "content": response})


    with col2:
     user_input = st.chat_input("ما الذي تريد أن تعرفه ؟")

    if user_input:
        # Ajouter le message utilisateur
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Afficher le message utilisateur
        st.chat_message("user").markdown(
            f"""
            <div style="width: 100%; max-width: 700px; background-color: #E9ECEF; padding: 15px; border-radius: 8px; margin: 10px; color: #000;">
                {user_input}
            </div>
            """, unsafe_allow_html=True
        )

        # Générer et afficher la réponse
        response = generate_response(user_input)
        placeholder = st.chat_message("assistant").markdown(
            f"""
            <div style="width: 100%; max-width: 700px; background-color: #E9ECEF; padding: 15px; border-radius: 8px; margin: 10px; color: #000;">
                {response}
            </div>
            """, unsafe_allow_html=True
        )

       # Affichage progressif de la réponse
    def display_progressive_response(response, placeholder):
     full_response = ""
     for word in response.split():
        full_response += word + " "
        time.sleep(0.08)  # Simuler un délai de saisie
        placeholder.markdown(
            f"""
            <div style="width: 100%; max-width: 700px; background-color: #E9ECEF; padding: 15px; border-radius: 8px; margin: 10px; color: #000;">
                {full_response}
            </div>
            """, unsafe_allow_html=True
        )

    # Ajouter la réponse à l'historique une seule fois
        if "messages" not in st.session_state:
         st.session_state.messages = []
    
     st.session_state.messages.append({"role": "assistant", "content": full_response})



