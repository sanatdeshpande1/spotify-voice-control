import speech_recognition as sr
import pyttsx3

from spotifyvoice import SpotifyVoice

speech_recognizer = sr.Recognizer() 

def SpeakText(command):
	engine = pyttsx3.init()
	engine.say(command) 
	engine.runAndWait()
	
def record():
	sp = None
	spotify_open = False
	while(1): 
		try:	
			with sr.Microphone() as source2:
				
				speech_recognizer.adjust_for_ambient_noise(source2, duration=0.2)
				
				audio2 = speech_recognizer.listen(source2)
				
				recorded_text = speech_recognizer.recognize_google(audio2)
				recorded_text = recorded_text.lower()

				if recorded_text == "close spotify":
					sp.play_pause(pause=True)
					spotify_open = False

				if(spotify_open):
					tokens = recorded_text.split()
					if(len(tokens) > 1 and tokens[0] == "play"):
						requested_song = " ".join(tokens[1:])
						print(requested_song)
						sp.play_song(requested_song)
					if(recorded_text == "play" or recorded_text == "start" or recorded_text == "start song"):
						SpeakText("Playing current song.")
						sp.play_pause()
					if(recorded_text == "pause" or recorded_text == "stop" or recorded_text == "stop song"):
						sp.play_pause(pause=True)
						SpeakText("Song paused.")
					if(recorded_text == "increase volume" or recorded_text == "volume high"):
						sp.change_volume(1)
					if(recorded_text == "decrease volume" or recorded_text == "reduce volume" or recorded_text == "volume low"):
						sp.change_volume(-1)
					if recorded_text == "volume medium":
						sp.change_volume(0)
					if(recorded_text == "next" or recorded_text == "next song"):
						sp.next_track()
					if(recorded_text == "previous" or recorded_text == "previous song"):
						sp.previous_track()
					if(recorded_text == "my list"):
						user_queue = sp.get_queue()
						SpeakText("Next 5 songs in your list are: ")
						for i in range (5):
							SpeakText(user_queue[i])


				if(recorded_text == "quit" or recorded_text == "exit" or recorded_text == "stop"):
					SpeakText("Have a good one! Bye!")
					exit()
				
				if(recorded_text == "open spotify"):
					spotify_open = True
					if sp == None:
						sp = SpotifyVoice()
					SpeakText("Spotify is ready!")				
				print(recorded_text)

		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))
			
		except sr.UnknownValueError:
			print("unknown error occurred")

record()