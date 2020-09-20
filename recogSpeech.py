import speech_recognition as sr 
r = sr.Recognizer()
mytext = ["cat","dog","bat","sit","mad","apple","ball","clap","help","yellow"]
for i in mytext:
  print(i)
  with sr.Microphone() as source:
    # read the audio data from the default microphone
    audio_data = r.record(source, duration=5)
    print("Recognizing...")
    # convert speech to text
    text = r.recognize_google(audio_data)
  if(text==i):
    print("correct")
  else:
    print("wrong")