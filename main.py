import telebot
from gtts import gTTS
from io import BytesIO
import os
import speech_recognition as sr
from core.function import convert_ogg_to_wav

TOKEN = '6872142181:AAGKP_ysnsNHFXdxfe6nIGUN2Hfkyu8RZvQ'  
bot = telebot.TeleBot(TOKEN,parse_mode="HTML")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text = message.text
    voice_path = text_to_speech(text)
    
    with open(voice_path, 'rb') as voice:
        bot.send_voice(message.chat.id, voice)

    # Faylni o'chirish
    os.remove(voice_path)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open("voice.ogg", 'wb') as new_file:
            new_file.write(downloaded_file)

        text = voice_to_text("voice.ogg")

        if text:
            bot.reply_to(message, "Ovozdan olingan matn:\n<b>{}</b>.".format(text))
        else:
            bot.reply_to(message, "Ovozni taniy olmadim.")

    except Exception as e:
        print(e)
        bot.reply_to(message, "Xatolik yuz berdi.")

def voice_to_text(voice_file):
    recognizer = sr.Recognizer()

    converted_wav_file = "voice.wav"
    convert_ogg_to_wav(voice_file, converted_wav_file)

    with sr.AudioFile(converted_wav_file) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="uz-UZ")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Google API ga so'rovni yuborishda xatolik yuz berdi; {0}".format(e))
        return None

def text_to_speech(text):
    tts = gTTS(text=text)  
    voice_path = "voice.ogg"
    tts.save(voice_path)
    return voice_path

if __name__ == "__main__":
    bot.polling(none_stop=True)
