import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import os
import json

from spotifyvoice import SpotifyVoice

load_dotenv()
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
				
				speech_recognizer.adjust_for_ambient_noise(source2, duration=0.2)
				
				audio2 = speech_recognizer.listen(source2, timeout=10)
				
				recorded_text = speech_recognizer.recognize_google(audio2)
				recorded_text = recorded_text.lower()

				if recorded_text in commands['close_spotify'] or recorded_text in commands['exit']:
					SpeakText("Closing Spotify.")
					sp.play_pause(pause=True)
					return

				tokens = recorded_text.split()
				if(len(tokens) > 1 and tokens[0] == "play"):
					requested_song = " ".join(tokens[1:])
					print(requested_song)
					sp.play_song(requested_song)
				if recorded_text in commands['play']:
					SpeakText("Playing current song.")
					sp.play_pause()
				if recorded_text in commands['pause']:
					sp.play_pause(pause=True)
					SpeakText("Song paused.")
				if recorded_text in commands['volume_up']:
					sp.change_volume(1)
				if recorded_text in commands['volume_down']:
					sp.change_volume(-1)
				if recorded_text in commands['volume_mid']:
					sp.change_volume(0)
				if recorded_text in commands['next_track']:
					sp.next_track()
				if recorded_text in commands['previous_track']:
					sp.previous_track()
				if recorded_text in commands['queue']:
					user_queue = sp.get_queue()
					SpeakText("Next 5 songs in your list are: ")
					for i in range (5):
						SpeakText(user_queue[i])
							
				print(recorded_text)

		except:
			return

while(1):
	try:	
		with sr.Microphone() as src:
			speech_recognizer.adjust_for_ambient_noise(src, duration=0.2)
			audio = speech_recognizer.listen(src)
			recorded_text = speech_recognizer.recognize_google(audio)
			recorded_text = recorded_text.lower()
			print(recorded_text)
			
			if recorded_text in va_wake_words:
				SpeakText("Listening.")
				record()
			if recorded_text == 'quit' or recorded_text == 'exit' or recorded_text == 'close':
				exit()

	except:
		SpeakText("I did not understand that.")

