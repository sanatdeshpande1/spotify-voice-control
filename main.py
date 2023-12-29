import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import os
import json
import requests
from datetime import datetime

from spotifyvoice import SpotifyVoice

load_dotenv()
WIT_AI_TOKEN = os.getenv("WIT_AI_TOKEN")
VOICE_ASSISTANT_NAME = os.getenv("VOICE_ASSISTANT_NAME")
va_wake_words = [VOICE_ASSISTANT_NAME, 'hi ' + VOICE_ASSISTANT_NAME, 'hello']

with open('commands.json') as file:
	commands = json.load(file)

speech_recognizer = sr.Recognizer() 
engine = None
def SpeakText(command):
	engine = pyttsx3.init()
	engine.setProperty('voice', 0)
	engine.setProperty('volume', 100)
	engine.setProperty('rate', 200)
	engine.say(command)
	engine.runAndWait()

def modify_engine_properties(property, value):
	engine.setProperty(property, value)

def record():
	sp = SpotifyVoice()
	while(1): 
		try:	
			with sr.Microphone() as source2:
				
				speech_recognizer.adjust_for_ambient_noise(source2, duration=1)
				
				audio2 = speech_recognizer.listen(source2, timeout=5)
				
				recorded_text = speech_recognizer.recognize_google(audio2)
				recorded_text = recorded_text.lower()
				print(recorded_text)

				# if recorded_text == "exit":
				# 	break

				url = "https://api.wit.ai/message"
				date = datetime.today().strftime('%Y%m%d')
				headers = {"Authorization": f"Bearer {WIT_AI_TOKEN}"}
				params = {"v": date, "q": recorded_text}
				resp = requests.get(url, headers=headers, params=params)
				if resp.status_code == 200:
					data = resp.json()
				
				intent = max(data['intents'], key=lambda x : x['confidence'])
				intent_name = intent['name']
				if 'action:action' in data['entities']:
					action = max(data['entities']['action:action'], key=lambda x : x['confidence'])

				print(intent_name)

				if action['value'] == 'exit':
					break

				if intent_name == 'wit$play_music' or intent_name == 'wit$resume_music':
					SpeakText("Playing current song.")
					sp.play_pause()
				
				if intent_name == 'playSong':
					if 'requestedSong:requestedSong' in data['entities']:
						search_queries = data['entities']['requestedSong:requestedSong']
						requested_song = ' '.join(query['value'] for query in search_queries)
						sp.play_song(requested_song)
					else:
						if action['value'] == 'play':
							sp.play_pause()
				
				if intent_name == 'wit$pause_music' or intent_name == 'wit$stop_music':
					sp.play_pause(pause=True)
					SpeakText("Song paused.")

				if intent_name == 'wit$skip_track':
					sp.next_track()
				
				if intent_name == 'wit$previous_track':
					sp.previous_track()
				
				if intent_name == 'changeVolume':
					new_volume = 50
					if action['value'] == 'high':
						new_volume = 80
					elif action['value'] == 'low':
						new_volume = 20

					if 'volumeLevel:volumeLevel' in data['entities']:
						requestedVolume = max(data['entities']['volumeLevel:volumeLevel'], key=lambda x : x['confidence'])
						new_volume = int(requestedVolume['value'])
					sp.change_volume(new_volume)
				
		except:
			pass

# while(1):
# 	try:	
# 		with sr.Microphone() as src:
# 			speech_recognizer.adjust_for_ambient_noise(src, duration=0.2)
# 			audio = speech_recognizer.listen(src)
# 			recorded_text = speech_recognizer.recognize_google(audio)
# 			recorded_text = recorded_text.lower()
# 			print(recorded_text)
			
# 			if recorded_text in va_wake_words:
# 				SpeakText("Listening.")
# 				record()
# 			if recorded_text == 'quit' or recorded_text == 'exit' or recorded_text == 'close':
# 				exit()

# 	except:
		# SpeakText("I did not understand that.")

record()
