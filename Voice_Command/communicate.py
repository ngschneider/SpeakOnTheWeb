import pyttsx3
import random
import os
from gtts import gTTS
import playsound
engine = pyttsx3.init()

#It allows Speak rather than print out words
def speak(command):
    tts = gTTS(text=command, lang='en')
    r = random.randint(1,10000000)
    audiofile = 'audio-'+str(r) + '.mp3'
    tts.save(audiofile)
    print(command)
    playsound.playsound(audiofile)
    os.remove(audiofile)

    # engine.say(command)
    engine.runAndWait()

