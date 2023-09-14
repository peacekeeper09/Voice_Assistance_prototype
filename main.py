import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Initialize the recognizer, engine, and voices
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to speak
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user commands
def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening...')
            listener.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '').strip()
                print(command)
            return command
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    return ""

# Function to play a song on YouTube
def play_song(song):
    try:
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)
    except Exception as e:
        talk('Sorry, could not play the song')

# Function to get and speak the current time
def get_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    talk('Current time is ' + time)

# Function to search for information on Wikipedia
def search_info(query):
    try:
        info = wikipedia.summary(query, sentences=1)
        print(info)
        talk(info)
    except wikipedia.exceptions.DisambiguationError as e:
        talk(f"Multiple results found for {query}. Please specify your search.")
    except wikipedia.exceptions.PageError as e:
        talk(f"No information found for {query}.")
    except Exception as e:
        talk('Sorry, could not find any information')

# Function to tell a joke
def tell_joke():
    talk(pyjokes.get_joke())

# Function to respond to greetings
def respond_to_greeting():
    talk('Yes, I am here. How can I help you?')

# Function to run the voice assistant
def run_alexa():
    while True:
        command = take_command()
        print(command)
        if 'play' in command:
            song = command.replace('play', '').strip()
            play_song(song)
        elif 'time' in command:
            get_time()
        elif any(keyword in command for keyword in ['search for', 'what is']):
            query = command.replace('search for', '').replace('what is', '').strip()
            search_info(query)
        elif 'joke' in command:
            tell_joke()
        elif any(greeting in command for greeting in ['hello', 'hi', 'hey']):
            respond_to_greeting()
        else:
            talk('Sorry, I did not understand that. Please say the command again.')

if __name__ == "__main__":
    run_alexa()
