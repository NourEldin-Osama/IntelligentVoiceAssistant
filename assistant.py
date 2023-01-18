import os
import random

import pyttsx3 as p
import speech_recognition as sr
from playsound import playsound

from commands import *
from speaker_recognition import SpeakerRecognition

# Initialize the text-to-speech engine
engine = p.init()
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')

# Initialize the speech recognition engine
r = sr.Recognizer()
r.energy_threshold = 10000

# Initialize the speaker recognition
speaker_recognizer = SpeakerRecognition()


def speak(text):
    """
    Speak the given text using the text-to-speech engine.
    :param text: the text to be spoken
    """
    engine.say(text)
    engine.runAndWait()


def listen():
    """
    Listen for user input and return it as a string.
    :return: the user's input
    """
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, 1)
            print("listening")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("user input:", text)
                return text.lower()
            except:
                print("error")
                speak("I didn't hear you. please tell me again")


def save_my_voice(name):
    """
    Record and save the user's voice with the given name.
    :param name: the name to save the user's voice as
    """
    speak("Speak for 3 seconds")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source)
    file_name = f"user_{name}.wav"
    with open(file_name, "wb") as file:
        file.write(audio.get_wav_data())
    vi_response = speaker_recognizer.add_known_voice(file_name, name)
    os.remove(file_name)
    speak(vi_response)


def know_who_am_i():
    """
    Attempt to recognize the speaker and return the result.
    :return: the speaker's name
    """
    speak("Speak for 3 seconds")
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, 1)
        audio = r.listen(source)
    file_name = f"user_{random.randint(0, 100_000)}.wav"
    with open(file_name, "wb") as file:
        file.write(audio.get_wav_data())
    vi_response = speaker_recognizer.get_unknown_voice(file_name)
    os.remove(file_name)
    speak("you are " + vi_response)


speak("Hello sir, i'm your voice assistant. How are you? Do you want to continue with a male or female voice assistant")
response = listen()

while True:
    if "female" in response:
        engine.setProperty('voice', voices[1].id)
        break
    elif "male" in response:
        engine.setProperty('voice', voices[0].id)
        break
    else:
        speak(
            "Who you want to you continue with you? a male or a female voice assistant?")
        response = listen()

speak("Hello sir, thank you for choosing me. what can i do for you ?")
response = listen()
while True:
    if "information" in response:
        speak("okay sir but which topic?")
        response = listen()
        result = query_wikipedia(response)
        speak(result)

    elif "youtube" in response:
        speak("Okay sir but which video?")
        response = listen()
        search_youtube(response)

    elif "time" in response or "date" in response:
        speak(get_current_datetime())

    elif "translate" in response:
        # speak("from which language?")
        # source = listen()
        # speak("to which language?")
        # destination = listen()
        speak("What you want me translate for you ?")
        words = listen()
        speak(translate_text(words, ))

    elif "prayer" in response:
        speak(get_next_prayer_time())

    elif "temperature" in response:
        speak(get_current_temperature())

    elif "news" in response:
        for news in get_latest_news():
            speak(news)

    elif "send" in response or "whatsapp" in response:
        speak("What is the phone number with the Country code?")
        phone_number = listen()
        speak("What is the message?")
        message = listen()
        speak("I am sending the message now")
        send_whatsapp_message(message, phone_number)
        speak("Message sent!")

    elif "sport" in response:
        playsound(r"audio.wav")

    elif "save" in response:
        speak("What's your name")
        name = listen()
        save_my_voice(name)
    elif "who" in response:
        know_who_am_i()

    elif "exit" in response or "quit" in response:
        speak("Goodbye, have a nice day")
        break

    speak("anything else ?")
    response = listen()
