## Run this command in terminal  before executing this program
## rasa run -m models --endpoints endpoints.yml --port 5002 --credentials credentials.yml
## and also run this in seperate terminal
## rasa run actions

import requests
import speech_recognition as sr  # import the library
import pyttsx3


def tts(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)  # set the voice to a male voice
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

initial_msg = (
    "Hi, this is Rasa! How may I help you?"  # initial message after starting the bot
)
print(initial_msg)
tts(initial_msg)
stop_list = [
    "bye",
    "thanks",
    "goodbye",
    "Bye",
    "Goodbye",
    "Thanks",
]  # bot stops if one of the words is said
while message not in stop_list:
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
            message = ""  # reset message if input not obtained

    if len(message) != 0:
        print("Sending message now")

        r = requests.post(
            "http://localhost:5002/webhooks/rest/webhook", json={"message": message}
        )

        print("Bot says:  ", end=" ")
        for i in r.json():
            bot_message = i["text"]
            print(f"{bot_message}")

        tts(bot_message)  # Read Bot's message aloud
