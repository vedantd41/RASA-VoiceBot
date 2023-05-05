# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction

import webbrowser as web
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from rasa_sdk.events import SlotSet
import pyautogui
import pyttsx3
import speech_recognition as sr
import os
from rasa.core import constants

constants.MAX_NUMBER_OF_PREDICTIONS = 50

# import sys
# sys.path.append('C:\Users\DELL\.conda\envs\rasa_be_proj\Lib\site-packages')

# from openai_secret_manager import get_secret
# mapbox_token = openai_secret_manager.get_secret("mapbox_token")["pk.eyJ1IjoieWFzaDIzMDEiLCJhIjoiY2xnbDE0YXZmMHhtdzNpbHZlNDRhcHBpaCJ9.zL8ziUyE5pCZDw1Hk9IUAA"]
# from mapbox import Directions

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


def tts(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)  # set the speaking rate (words per minute)
    engine.setProperty("volume", 1.0)  # set the volume level (0 to 1)
    engine.setProperty("voice", "en")
    engine.say(text)
    engine.runAndWait()


def record_audio():
    # Record audio from microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        audio = r.listen(source)

    # Use Google speech recognition API to transcribe audio
    try:
        text = r.recognize_google(audio)
        print(text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None


class ActionGetSong(Action):
    def name(self) -> Text:
        return "action_get_song"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text = record_audio()
        print(text)
        # pyautogui.press("enter")
        return [SlotSet("song_name", text)]


class ActionGetLocation(Action):
    def name(self) -> Text:
        return "action_get_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        text = record_audio()
        print(text)
        # pyautogui.press("enter")
        return [SlotSet("location_name", text)]


class ActionSpeakIntent(Action):
    def name(self) -> Text:
        return "action_speak_intent"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Get the previous user intent
        for event in tracker.events:
            if (event.get("event") == "bot") and (event.get("event") is not None):
                text = event.get("text")
        tts(text)

        return []


class ActionCheckSong(Action):
    def name(self) -> Text:

        return "action_check_song"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check song method")
        # user_choice = tracker.get_slot("song_name")
        # dispatcher.utter_message(text=f"You chose the song {user_choice}")
        user_input = tracker.latest_message.get("text")
        return [SlotSet("song_name", user_input)]
        # return []


class ActionCheckLocation(Action):
    def name(self) -> Text:

        return "action_check_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check location method")
        # return {
        #     "location_name": [
        #         self.from_entity(entity="location_name", intent="input_location"),
        #         self.from_text(),
        #     ]
        # }
        user_input = tracker.latest_message.get("text")
        return [SlotSet("location_name", user_input)]

        # user_choice = tracker.get_slot("location_name")
        # dispatcher.utter_message(text=f"You chose the location {user_choice}")
        # tts("You chose the location {user_choice}")

        # dispatcher.utter_message(template="utter_confirm_location", location_name=tracker.get_slot('location_name'),
        #                          headset=tracker.get_slot('BRAND'))

        # return []


class ActionCheckContact(Action):
    def name(self) -> Text:

        return "action_check_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        print("reached check contact method")
        # user_choice = tracker.get_slot("contact_name")
        # dispatcher.utter_message(text=f"You chose the person {user_choice}")
        user_input = tracker.latest_message.get("text")
        return [SlotSet("contact_name", user_input)]
        return []


class ConfirmSong(Action):
    def name(self) -> Text:

        return "action_confirm_song"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # text = record_audio()
        # print(text)
        # user_conf = tracker.get_slot("input_confirmation")
        # SlotSet("input_confirmation", text)
        # print(tracker.latest_message["intent"].get("name"))
        # print(user_conf)
        # print(type(user_conf))
        # if tracker.latest_message['intent'].get('name') == 'confirm_input':
        #     print("reached")
        #     return [FollowupAction("action_set_api_slot_music")]

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)
        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_spotify_api")]


class ConfirmLocation(Action):
    def name(self) -> Text:

        return "action_confirm_location"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # user_conf = tracker.get_slot("input_confirmation")
        # print(tracker.latest_message["intent"].get("name"))

        # text = record_audio()
        # print(text)

        # user_conf = tracker.get_slot("input_confirmation")

        # print(user_conf)
        # print(type(user_conf))
        # if tracker.latest_message['intent'].get('name') == 'confirm_input':
        #     print("reached")
        #     return [FollowupAction("action_set_api_slot_music")]
        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)

        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]
        # print(type(resp_list[0]))

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_maps_api")]


class ConfirmContact(Action):
    def name(self) -> Text:

        return "action_confirm_contact"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # user_conf = tracker.get_slot("input_confirmation")
        # print(tracker.latest_message["intent"].get("name"))
        # print(user_conf)
        # print(type(user_conf))
        # text = record_audio()
        # print(text)
        # user_conf = tracker.get_slot("input_confirmation")
        # if tracker.latest_message['intent'].get('name') == 'confirm_input':
        #     print("reached")
        #     return [FollowupAction("action_set_api_slot_music")]

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)
        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]
        # print(type(resp_list[0]))

        if user_input in resp_list:
            print("reached")
            return [FollowupAction("action_call_contacts_api")]


class ActionCallSpotifyAPI(Action):
    def name(self) -> Text:

        return "action_call_spotify_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # user_choice = tracker.get_slot("song_name")
        # print(f"Now calling the Spotify API to play the song {user_choice}")
        # dispatcher.utter_message(f"I will now call the Spotify API to play the song {user_choice}")

        user_input = tracker.get_slot("song_name")
        print(user_input)

        client_id = "b98db0c89cf143a7bba3370cf13b2b96"
        client_secret = "eef5b8588cee4e06b2166da5795e3b2f"
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Search for the song and artist on Spotify
        query = "track:{}".format(user_input)
        # query = "track:{} artist:{}".format(song_name, artist_name)
        result = spotify.search(q=query)

        # Get the Spotify URI of the first track in the search results
        track_uri = result["tracks"]["items"][0]["uri"]

        # subprocess.Popen(["C:\\Users\\Vedant\\AppData\\Roaming\\Spotify\\Spotify.exe"])
        # web.open(f"spotify:search:{song_name}")
        web.open(track_uri)

        # Play the track on Spotify
        # spotify.start_playback(uris=[track_uri])

        # Send a message to the user confirming that the song is playing
        message = "Playing {} on Spotify".format(user_input)
        # message = "Playing {} by {}".format(song_name, artist_name)
        # tts(message)
        dispatcher.utter_message(text=message)

        return []


class ActionCallMapsAPI(Action):
    def name(self) -> Text:

        return "action_call_maps_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_choice = tracker.get_slot("location_name")
        # user_choice_dest = tracker.get_slot("dest_location_name")
        # print(f"Now calling the Maps API to play the song {user_choice_src}")
        print(f"Now calling the Maps API to find the location {user_choice}")
        dispatcher.utter_message(f"Here are the directions to {user_choice}")
        # dispatcher.utter_message(f"Now calling the Maps API to find the location {user_choice_dest}")

        # origin = ""
        # directions = Directions(access_token=mapbox_token)

        # response = directions.directions(
        #     coordinates=[[origin], [user_choice]],
        #     profile='mapbox/driving',
        #     steps=True,
        #     language='en'
        # )

        url = (
            "https://www.google.com/maps/dir/?api=1&origin=pune&destination="
            + user_choice
        )
        web.open(url)

        return []


class ActionCallContactsAPI(Action):
    def name(self) -> Text:

        return "action_call_contacts_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        user_choice = tracker.get_slot("contact_name")

        # if user_choice in contact_list:
        #     print(f"Now calling the Contacts API to call the person {user_choice}")
        #     dispatcher.utter_message(f"Now calling the Contacts API to call the person {user_choice}")
        # else:
        #     dispatcher.utter_message("The person you are trying to search is not in your contacts")

        print(f"Now calling the Contacts API to call the person {user_choice}")
        dispatcher.utter_message(
            f"Now calling the Contacts API to call the person {user_choice}"
        )

        return []
