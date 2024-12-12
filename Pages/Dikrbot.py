import streamlit as st
import time
import random
import speech_recognition as sr


def DikrBot():
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
            <div class="title">⚪ Dikr Bot - 🤖ساعدك لآيات الذكر</div>
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



