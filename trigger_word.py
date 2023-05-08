import speech_recognition as sr  # import the library
from gtts import gTTS

trigger_words = ["coffee", "Coffee"]
message = ""

while message not in trigger_words:
    r = sr.Recognizer()  # initialize recognizer
    with sr.Microphone() as source:  # mention source it will be either Microphone or audio files.
        print("Waiting for Trigger Word :")
        audio = r.listen(source)  # listen to the source
        try:
            message = r.recognize_google(
                audio
            )  # use recognizer to convert our audio into text part.
            print("You said : {}".format(message))

        except:
            print(
                "Sorry could not recognize your voice"
            )  # In case of voice not recognized clearly
            message = ""

    # completely stop the bot
    if message == "terminate":
        break

    # if trigger word spoken, start bot
    if message in trigger_words:
        print("In Voice Bot")
        exec(open("voice_bot.py").read())
