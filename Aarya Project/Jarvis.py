import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import pywhatkit as kit
import pyautogui as p
import requests  # For making the request
from decouple import config   #For weather report
import openai  #pip insatll open ai ---> For chatGPT

OPENAI_KEY = config("OPENAI_KEY")
openai.api_key = OPENAI_KEY
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir!")

    else:
        speak("Good Evening Sir!")

    speak("I am Aarya,how may I help you")
    
    
def chatgpt_response(messages, model="gpt-3.5-turbo"):
    try:
        response = openai.Completion.create(
           engine=model,
           prompt=messages,
           max_tokens=150,
           temperature=0.5,
           n=1
         )

        message = response['choices'][0]['text'].strip()
        return message.lower()

    except Exception as e:
        print(f"Error generating response from ChatGPT: {e}")
        speak("Sorry, I couldn't generate a response at the moment.")
        return "None"
    
def chatgpt_conversation(messages, model="gpt-3.5-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": messages}  # assuming messages is the user input
            ],
            max_tokens=150,
            temperature=0.5,
            n=1
        )
        message = response.choices[0].message['content']
        return message.lower()

    except Exception as e:
        print(f"Error generating response from ChatGPT: {e}")
        speak("Sorry, I couldn't generate a response at the moment.")
        return "None"


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.6
        audio = r.listen(source)
        print("Audio recorded.")

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query.lower()

    except Exception as e:
        print("Could not recognize speech. Trying ChatGPT...")
        return ''


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('raisamarth2794@gmail.com', 'Raisam2794@')
    server.sendmail('raisamarth2794@gmail.com', to, content)
    server.close()

def get_weather_report(city):
    res = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

if __name__ == "__main__":
    def taskexecution():
     p.press('esc')
     speak("Verification Successfull")
     from GUI import GUI
     GUI
     speak("Welcome back Samarth Sir !!")
     wishMe()
     while True:
        query = takeCommand().lower()
        if not query:
           continue 
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            print("Opening YouTube")
            speak("Opening YouTube")
            webbrowser.open("youtube.com")
            
        elif 'open notepad' in query:
            print("Opening Notepad")
            speak("Opening Notepad")
            NotepadPath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(NotepadPath)
            
        elif 'open cmd' in query:
            print("Opening CMD")
            speak("Opening CMD")
            CMDPath = "C:\\Windows\\system32\\cmd.exe"
            os.startfile(CMDPath)

        elif 'open google' in query:
            print("Opening Google")
            speak("what do you want to search on google sir ??")
            cm = takeCommand().lower()
            webbrowser.open(f"{cm}")

        elif 'open stackoverflow' in query:
            print("Opening Stack Overflow")
            speak("Opening Stack Overflow")
            webbrowser.open("stackoverflow.com")
            
        elif 'play music' in query:
            print("Playing your favourite music")
            speak("Playing your favourite music")
            webbrowser.open("https://www.youtube.com/watch?v=fTauOK8J-U8&list=RDfTauOK8J-U8&index=1")

        elif 'what is the time going on' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'open vscode' in query:
            print("Opening VScode")
            speak("Opening VScode")
            VScodePath = "C:\\Users\\Samarth Rai\\AppData\\Local\\Programs\\Microsoft VS Code"
            os.startfile(VScodePath)
            
        elif 'send whatsapp message' in query:
            speak("Please enter phone number to send message")
            phone_number = input("Enter the recipient's phone number (with country code): ")
            speak("Please type what do you want to send")
            message = input("Enter the message you want to send: ")
            # Send the message instantly
            kit.sendwhatmsg(phone_number, message,2,25)
            
        elif 'tell me the weather report' in query:
            weather_data = get_weather_report(city="Varanasi")
            speak(f"The weather in Varanasi is currently {weather_data[0]} with a temperature of {weather_data[1]} and feels like {weather_data[2]}")
        
        elif 'ok thanks' in query:
            speak("Welcome Sir")
            
        elif 'what is your name ??' in query:
            speak("My name is Q Sir")

        elif 'exit' in query:
            speak("ok,thank you sir for using me,system now dissconnected")
            exit(0)
            
        elif 'open camera' in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret , img = cap.read()
                cv2.imshow('webcam',img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif 'send email' in query:
            try:
                speak("Please enter your email address")
                to = input("Please enter your email address : ")
                speak("What should I say?")
                content = takeCommand()   
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry I am not able to send this email right now")  
                
        else:
            # Create a list of messages for the chat model
                messages = f"You are a helpful assistant.\nUser: {query}"
                
                # Get response from ChatGPT
                response = chatgpt_conversation(messages)

                # Speak and print the response
                speak(response)
                print(response)

##############################################################################################################################


recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
recognizer.read('trainer/trainer.yml')   #load trained model
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath) #initializing haar cascade for object detection approach

font = cv2.FONT_HERSHEY_SIMPLEX #denotes the font type


id = 2 #number of persons you want to Recognize


names = ['','avi']  #names, leave first empty bcz counter starts from 0


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #cv2.CAP_DSHOW to remove warning
cam.set(3, 640) # set video FrameWidht
cam.set(4, 480) # set video FrameHeight

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# flag = True

while True:

    ret, img =cam.read() #read the frames using the above created object

    converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #The function converts an input image from one color space to another

    faces = faceCascade.detectMultiScale( 
        converted_image,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #used to draw a rectangle on any image

        id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w]) #to predict on every single image

        # Check if accuracy is less them 100 ==> "0" is perfect match
        if (accuracy < 100):
           if id < len(names):  # Check if id is within valid range
              id = names[id]
              accuracy = "  {0}%".format(round(100 - accuracy))
              taskexecution()
           else:
              id = "unknown"  # Handle unknown ID
              accuracy = "  {0}%".format(round(100 - accuracy))
              speak("You are not authorized to use this system")
              break
          
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
        cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("Thanks for using this program, have a good day.")
cam.release()
cv2.destroyAllWindows()