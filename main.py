import pyttsx3
import datetime
import wikipedia
import speech_recognition as sr
import webbrowser
import smtplib
import os
import requests
# Initialize the engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

# Choose and set the voice
for index, voice in enumerate(voices):
    print(f"Voice {index}: {voice.id}")
engine.setProperty("voice", voices[0].id)  # Default to first voice

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Check network connectivity
def is_connected():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

# Greeting function
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 17:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak(" I  am  Erik  , Satyam sir personal assistant , Please tell me how may I help you.")


# Take command from user
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query.lower()  # Normalize to lowercase
        except sr.UnknownValueError:
           # print("Could not understand the audio. Please try again.")
            speak("I couldn't understand. Please repeat.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            speak("I couldn't connect to the speech recognition service. Please check your connection.")
        return "none"

# Send email
def sendmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email_id", "your_password")
        server.sendmail("your_email_id", to, content)
        server.quit()
        speak("Email has been sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        speak("Sorry, I couldn't send the email.")

# Main logic
if __name__ == "__main__":
    if not is_connected():
        speak("It seems there is no internet connection. Please check your network and try again.")
    else:
        wishMe()
        while True:
            query = takecommand()

            # Execute commands
            if "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia:")
                    print(results)
                    speak(results)
                except Exception as e:
                    speak("Sorry, I couldn't fetch information from Wikipedia.")

            elif "open youtube" in query:
                webbrowser.open("youtube.com")

            elif "open google" in query:
                webbrowser.open("google.com")

            elif "open spotify" in query:
                webbrowser.open("spotify.com")

            elif "open whatsapp" in query:
                webbrowser.open("web.whatsapp.com")

            elif "open linkedin" in query:
                webbrowser.open("linkedin.com")
                
            elif "open chat gpt" in query:
                webbrowser.open("Chat gpt.com")   

            elif "open instagram" in query:
                webbrowser.open("instagram.com")

            elif "Play music" in query:
                music_dir = "C:\\Users\\shiva\\OneDrive\\Desktop\\Songs"
                songs = os.listdir(music_dir)
                print("songs")
                os.startfile(os.path.join(music_dir,songs[0]))
              
            elif "open github" in query:
                webbrowser.open("github.com")

            elif "open telegram" in query:
                webbrowser.open("web.telegram.org")

            elif "the time" in query:
                strtime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {strtime}")

            elif "email to satyam" in query:
                try:
                    speak("What should I say?")
                    content = takecommand()
                    to = "satyam@gmail.com"
                    sendmail(to, content)
                except Exception as e:
                    speak("Sorry, I couldn't send the email.")
                    
           # elif "Thank you" in query :
                #speak("Thank you Satyam sir..")

            elif "exit" in query or "quit" in query:
                speak("Thank you Satyam sir..")
                break

            else:
                speak("I'm sorry, I didn't understand that. Could you rephrase?")
