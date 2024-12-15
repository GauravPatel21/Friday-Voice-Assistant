import speech_recognition as sr
import pyttsx3
import webbrowser
import musicLibrary
import webAppsLibrary
import yt_dlp
import logging

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Wake Word

wakeWord= "hello"
exitWord = "exit"


def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def webSearch(query):
    logging.info(f"Searching web for: {query}")
    searchUrl = f"https://www.google.com/search?q={query}"
    webbrowser.open(searchUrl)
    print(f"I have opened the web browser for your search.")

def getYtLink(query):
    """Get a YouTube link for the given query using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'default_search': 'ytsearch',
        'noplaylist': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            return result['entries'][0]['url'] if result['entries'] else None
    except Exception as e:
        logging.error(f"Error fetching YouTube link: {e}")
        return None

def openApp(command):
    """Open a web app based on the command."""
    app= command.split(" ")[1]
    logging.info(f"Attempting to open app: {app}")
    link = webAppsLibrary.webApps.get(app)
    if link:
        webbrowser.open(link)
        speak(f"Opening {app}.")
    else:
        speak(f"Sorry, I couldn't find {app} in the app list.")

def playMusic(command):
    """Play music based on the command."""
    songName = command.replace("play", "").strip()
    logging.info(f"Attempting to play song: {songName}")
    link = musicLibrary.music.get(songName)
    if link:
        webbrowser.open(link)
        speak(f"Playing {songName}.")
    else:
        speak("Searching for the song on YouTube.")
        link = getYtLink(songName)
        if link:
            webbrowser.open(link)
            speak(f"Playing {songName} from YouTube.")
        else:
            speak("Sorry, I couldn't find the song.")

def processCommand(command):
    """Process the recognized command."""
    logging.info(f"Command received: {command}")
    
    # For Opening Web Apps
    if command.startswith("open"):
        openApp(command)

    # For Playing Music
    elif command.startswith("play"):
        playMusic(command)

    # For Exiting Friday    
    elif command == exitWord:
        speak("Goodbye!")
        exit()

    #For Searching Online
    else:
        speak(f"Let me Search {command}")
        webSearch(command)

def recognizeSpeech(prompt="Listening..."):
    """Recognize speech using the microphone."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=3)  # Adjust for ambient noise for 3 seconds
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Increased timeout and phrase time
            recognized_text = recognizer.recognize_google(audio)
            print(f"Recognized: {recognized_text}")  # Debugging line
            return recognized_text
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.WaitTimeoutError:
            speak("No input detected.")
        return None


def listenForWakeWord():
    """Continuously listen for the wake word."""
    try:
        while True:
            word = recognizeSpeech("Listening for the wake word...")  # Listening for wake word
            if word and word.lower() == wakeWord:
                speak("Yes, how can I assist?")
                command = recognizeSpeech("Listening for your command...")  # Listen for user command after wake word
                if command:
                    processCommand(command.lower())
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        speak("An error occurred. Please try again.")

# Initialize Friday
speak("Initializing Friday...")
listenForWakeWord()