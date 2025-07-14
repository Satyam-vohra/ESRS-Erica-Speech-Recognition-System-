from flask import Flask, render_template, request, jsonify
import datetime, pyttsx3, wikipedia, speech_recognition as sr
import webbrowser, os, smtplib, requests, cv2, mediapipe as mp
from multiprocessing import Process
app = Flask(__name__)

# =============== Voice Engine ==================
engine = pyttsx3.init("sapi5")
engine.setProperty("voice", engine.getProperty("voices")[0].id)

def speak(text):
    print("SPEAK:", text)
    engine.say(text)
    engine.runAndWait()

# =============== Wish ==================
def wish_me():
    hour = datetime.datetime.now().hour
    if hour < 12:
        greet = "Good morning!"
    elif hour < 17:
        greet = "Good afternoon!"
    else:
        greet = "Good evening!"
    speak(f"{greet} I am Erik. Please tell me how may I help you.")

# =============== Take Voice Command ==================
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = r.listen(source)
        try:
            speak("Recognizing...")
            return r.recognize_google(audio, language='en-in').lower()
        except:
            speak("Please say again.")
            return "none"
# =============== Send Email ==================
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("your_email", "your_password")
        server.sendmail("your_email", to, content)
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        speak("Could not send the email.")
        print(e)

# =============== Finger Detection ==================
def detect_fingers(handLms):
    fingers = []
    fingers.append(handLms.landmark[4].x < handLms.landmark[3].x)  # Thumb
    for tip_id in [8, 12, 16, 20]:
        fingers.append(handLms.landmark[tip_id].y < handLms.landmark[tip_id - 2].y)
    return fingers

# =============== Gesture Control ==================
def gesture_control():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        if not ret:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        label = "Waiting..."

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
                fingers = detect_fingers(handLms)

                # ========== Gesture Match ==========
                if fingers == [True, True, True, True, True]:
                    label = "🖐️ Hello - Ready to help"
                    speak("Hello Satyam sir, how can I help you?")

                elif fingers == [False, False, False, False, False]:
                    label = "✊ Fist - Exiting"
                    speak("Exiting Erik. Bye Satyam sir!")
                    os._exit(0)

                elif fingers == [False, True, False, False, False]:
                    label = "👉 Point - Open Google"
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")

                elif fingers == [False, True, True, False, False]:
                    label = "✌️ Victory - Play Music"
                    speak("Playing music")
                    music_dir = "C:\\Users\\shiva\\OneDrive\\Desktop\\Songs"
                    songs = os.listdir(music_dir)
                    if songs:
                        os.startfile(os.path.join(music_dir, songs[0]))

                elif fingers == [True, False, False, False, False]:
                    label = "👍 Thumbs Up - Motivation"
                    speak("Keep going Satyam sir, you're doing great!")

                elif fingers == [True, True, False, False, True]:
                    label = "🤟 Rock - Love You"
                    speak("I love you too, Satyam sir!")

                elif fingers == [True, False, False, False, True]:
                    label = "🤙 Call Me - WhatsApp Web"
                    speak("Opening WhatsApp Web")
                    webbrowser.open("https://web.whatsapp.com")

                else:
                    label = "❓ Unknown Gesture"

                # Overlay label
                h, w, _ = img.shape
                cx = int(handLms.landmark[9].x * w)
                cy = int(handLms.landmark[9].y * h)
                cv2.putText(img, label, (cx - 120, cy - 30), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, (0, 255, 255), 2)

        cv2.imshow("Erik AI - Hand Gesture", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# =============== Flask Routes ==================
@app.route('/')
def index():
    return render_template("interface.html")

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    query = data.get("query", "").lower()

    if "how are you" in query:
        speak("I’m functioning optimally, Satyam sir.")
    elif "your name" in query:
        speak("My name is Erik.")
    elif "motivate" in query:
        speak("Believe in yourself, Satyam sir.")
    elif "wikipedia" in query:
        topic = query.replace("wikipedia", "")
        results = wikipedia.summary(topic, sentences=2)
        speak(results)
    elif "open google" in query:
        webbrowser.open("https://google.com")
    elif "play music" in query:
        music_dir = "C:\\Users\\shiva\\OneDrive\\Desktop\\Songs"
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
    elif "time" in query:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")
    elif "email to satyam" in query:
        speak("What should I say?")
        content = take_command()
        send_email("satyam@gmail.com", content)
    elif "exit" in query:
        speak("Goodbye Satyam sir.")
        return jsonify({"exit": True})
    else:
        speak("Sorry, I didn't understand.")

    return jsonify({"status": "done"})

# =============== Run ==================
if __name__ == '__main__':
    gesture_process = Process(target=gesture_control)
    gesture_process.start()

    speak("Starting Erik System")
    wish_me()
    app.run(debug=True)

    gesture_process.terminate()
