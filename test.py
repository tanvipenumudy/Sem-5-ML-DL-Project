from gtts import gTTS
from playsound import playsound
mytext = ["cat","dog","bat","sit","mad","apple","ball","clap","help","yellow"]
count = 0
language = 'en'
for i in mytext:
  if(count==5):
    break
  else:
    tts = gTTS(i, lang='en')
    hlo = i+".mp3"
    tts.save(hlo)
    playsound(hlo)  
    inp = input("Enter text: ")
    if(inp.strip() != i):
      count=count+1
      print("wrong")
    else:
      print("correct")
print("Number of wrongs: ",count)