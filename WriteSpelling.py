from gtts import gTTS
from playsound import playsound
mytext = ["cat","dog","bat","sit","mad","apple","ball","clap","help","yellow"]
student = []
count = 0
#tss = gTTS("Hello, you can consider me as your friend, please feel type the spelling of #each word you hear", lang='en')
#    hlo2 = i+".mp3"
#   tss.save(hlo2)
#   playsound(hlo2) 
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
    student.append(inp)
    if(inp.strip() != i):
      count=count+1
      print("wrong")
    else:
      print("correct")
print("Number of wrongs: ",count)
print(student)