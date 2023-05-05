# rasa modules
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from typing import Any, Text, Dict, List

# modules for supporting API calls
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser as web


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
        user_input = tracker.latest_message.get("text")
        return [SlotSet("song_name", user_input)]


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
        user_input = tracker.latest_message.get("text")
        return [SlotSet("location_name", user_input)]


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
        user_input = tracker.latest_message.get("text")
        return [SlotSet("contact_name", user_input)]


class ConfirmSong(Action):
    def name(self) -> Text:

        return "action_confirm_song"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

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

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)

        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

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

        user_input = tracker.latest_message.get("text")
        SlotSet("input_confirmation", user_input)
        resp_list = ["yes", "YES", "yess", "yessir", "Yes", "Ya"]

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

        user_input = tracker.get_slot("song_name")
        print(user_input)

        client_id = "b98db0c89cf143a7bba3370cf13b2b96"
        client_secret = "eef5b8588cee4e06b2166da5795e3b2f"
        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Search for the song and artist on Spotify
        query = "track:{}".format(user_input)
        result = spotify.search(q=query)

        # Get the Spotify URI of the first track in the search results
        track_uri = result["tracks"]["items"][0]["uri"]
        web.open(track_uri)

        # Send a message to the user confirming that the song is playing
        message = "Playing {} on Spotify".format(user_input)
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
        print(f"Now calling the Maps API to find the location {user_choice}")
        dispatcher.utter_message(f"Here are the directions to {user_choice}")
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
        print(f"Now calling the Contacts API to call the person {user_choice}")
        dispatcher.utter_message(
            f"Now calling the Contacts API to call the person {user_choice}"
        )
        return []
