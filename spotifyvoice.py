import spotipy
from spotipy.oauth2 import SpotifyOAuth
from difflib import get_close_matches
from dotenv import load_dotenv
import os
from pprint import pprint

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URI")

scope = ['user-library-read', 
         'playlist-read-private', 
         'user-read-playback-state',
         'user-modify-playback-state', 
         'playlist-modify-public', 
         'playlist-modify-private',
         'user-read-currently-playing',
         'user-top-read']

class SpotifyVoice:
    tracks = []
    user_playlists = dict()
    user_top_tracks = dict()
    user_top_artists = dict()
    playlist_no = 1

    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URL,
                                                scope=scope, open_browser=False))
        self.device_id = self.sp.devices()['devices'][0]['id']

        playlists = self.sp.current_user_playlists(limit=50)
        for item in playlists['items']:
            self.user_playlists[item['name']] = item['uri']
        
    def play_pause(self, pause=False):
        if pause:
            self.sp.pause_playback(self.device_id)
        else:
            self.sp.start_playback(self.device_id)

    def search_track(self, track_name):
        res = self.sp.search(track_name)
        track = [item['uri'] for item in res['tracks']['items']][0]
        return track

    def play_song(self, track="bohemian rhapsody"):
        track_uri = self.search_track(track_name=track)
        self.sp.start_playback(self.device_id, uris=[track_uri])

    def stop(self):
        self.sp.pause_playback(self.device_id)

    def change_volume(self, change):
        self.sp.volume(change)
    
    def next_track(self):
        self.sp.next_track(self.device_id)

    def previous_track(self):
        self.sp.previous_track(self.device_id)
    
    def get_queue(self):
        q = self.sp.queue()
        mylist = [n['name'] for n in q['queue']]
        return mylist

    def create_playlist(self, playlist_name="playlist"):
        user_id = self.sp.me()['id']
        if playlist_name == "playlist":
            playlist_name += self.playlist_no
            self.playlist_no += 1
        self.sp.user_playlist_create(user_id, playlist_name)
    
    def search_playlist_by_name(self, playlist_name="playlist1"):
        user_playlist_matches = get_close_matches(playlist_name, self.user_playlists.keys())
        if len(user_playlist_matches) == 0:
            playlists = self.sp.search(playlist_name, limit=1, type="playlist")
            return {'playlist_name': playlists['playlists']['items'][0]['name'], 
                    'playlist_uri': playlists['playlists']['items'][0]['uri']
                    }
        best_user_playlist_match = max(user_playlist_matches, key=lambda x : len(set(x) & set(playlist_name)))
        return {'playlist_name': best_user_playlist_match, 
                'playlist_uri': self.user_playlists[best_user_playlist_match]
                }

    def play_tracks_from_playlist(self, playlist_name="playlist1"):
        playlist_to_play = self.search_playlist_by_name(playlist_name=playlist_name)
        playlist_tracks = self.sp.playlist_items(playlist_to_play['playlist_uri'])
        for item in playlist_tracks['items']:
            self.sp.add_to_queue(item['track']['uri'])

        return playlist_to_play['playlist_name']
    
    def add_track_to_playlist(self, track, playlist_name):
        playlist_name_lower = playlist_name.lower()
        user_playlist_matches = get_close_matches(playlist_name_lower, (key.lower() for key in self.user_playlists.keys()))
        if len(user_playlist_matches) == 0:
            print("Invalid playlist")
            return
        
        best_user_playlist_match = max(user_playlist_matches, key=lambda x : len(set(x) & set(playlist_name_lower)))
        matched_playlist_name = next(key for key in self.user_playlists.keys() if key.lower() == best_user_playlist_match)
        matched_playlist_uri = self.user_playlists[matched_playlist_name]

        track_uri = self.search_track(track_name=track)
        self.sp.playlist_add_items(matched_playlist_uri, [track_uri])
