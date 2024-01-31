from pydub import AudioSegment

def convert_ogg_to_wav(ogg_file, wav_file):
    audio = AudioSegment.from_ogg(ogg_file)
    audio.export(wav_file, format="wav")

def text_to_speech(update, context):
    text = update.message.text
    tts = gTTS(text=text, lang='en')  
    tts.save('audio.mp3')
    with open('audio.mp3', 'rb') as audio_file:
        context.bot.send_voice(chat_id=update.effective_chat.id, voice=audio_file)

def speech_to_text(update, context):
    voice_file = context.bot.getFile(update.message.voice.file_id)
    voice_file.download('voice.ogg')
    r = sr.Recognizer()
    with sr.AudioFile('voice.ogg') as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)
        except sr.UnknownValueError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Kechirasiz, buni tushunolmadim.")
        except sr.RequestError as e:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Google Speech Recognition xizmatidan natijalarni soʻrab boʻlmadi; {0}".format(e))
