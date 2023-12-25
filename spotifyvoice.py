import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URI")

scope = ['user-library-read', 
         'playlist-read-private', 
         'user-read-playback-state',
         'user-modify-playback-state', 
         'playlist-modify-public', 
         'user-read-currently-playing']

class SpotifyVoice:    
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URL,
                                                scope=scope, open_browser=False))
        self.device_id = self.sp.devices()['devices'][0]['id']
        
    def play_pause(self, pause=False):
        if pause:
            self.sp.pause_playback(self.device_id)
        else:
            self.sp.start_playback(self.device_id)

    def play_song(self, song="bohemian rhapsody"):
        res = self.sp.search(song)
        song = res['tracks']['items'][0]['uri']
        self.sp.start_playback(self.device_id, uris=[song])

    def stop(self):
        self.sp.pause_playback(self.device_id)

    def change_volume(self, change):
        if change == 1:
            self.sp.volume(95)  # high volume
        if change == -1:
            self.sp.volume(20)  # medium volume
        if change == 0:
            self.sp.volume(50)  # low volume
    
    def next_track(self):
        self.sp.next_track(self.device_id)

    def previous_track(self):
        self.sp.previous_track(self.device_id)
    
    def get_queue(self):
        q = self.sp.queue()
        mylist = [n['name'] for n in q['queue']]
        return mylist