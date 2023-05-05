## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr  # import the library
import subprocess
from gtts import gTTS
import pyttsx3

# sender = input("What is your name?\n")


def tts(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # set the speaking rate (words per minute)
    engine.setProperty("volume", 1.0)  # set the volume level (0 to 1)
    engine.setProperty("voice", "en")
    engine.say(text)
    engine.runAndWait()


bot_message = ""
message = ""

r = requests.post(
    "http://localhost:5002/webhooks/rest/webhook", json={"message": "Hello"}
)

# print("Bot says, ", end=" ")
# for i in r.json():
#     bot_message = i["text"]
#     print(f"{bot_message}")

# myobj = gTTS(text=bot_message)
# myobj.save("welcome.mp3")
# print("saved")
# Playing the converted file
# subprocess.call(["mpg321", "welcome.mp3", "--play-and-exit"])

initial_msg = "Hi, this is Rasa!"
print(initial_msg)
tts(initial_msg)
stop_list = ["bye", "thanks", "goodbye", "Bye", "Goodbye", "Thanks"]
while bot_message not in stop_list:
    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Speak Anything :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(
                audio
            )  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

        except:
            print(
                "Sorry could not recognize your voice"
            )  # In case of voice not recognized  clearly
    if len(message) == 0:
        continue
    print("Sending message now")

    r = requests.post(
        "http://localhost:5002/webhooks/rest/webhook", json={"message": message}
    )

    print("Bot says, ", end=" ")
    for i in r.json():
        bot_message = i["text"]
        print(f"{bot_message}")

    tts(bot_message)

    # myobj = gTTS(text=bot_message)
    # myobj.save("welcome.mp3")
    # Playing the converted file
    # subprocess.call(["mpg321", "welcome.mp3", "--play-and-exit"])
