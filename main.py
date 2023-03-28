import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return ""
    return command


def play_song(song):
    try:
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    except:
        talk('Sorry, could not play the song')


def get_time():
    time = datetime.datetime.now().strftime('%I:%M %p')
    talk('Current time is ' + time)


def search_info(query):
    try:
        info = wikipedia.summary(query, 1)
        print(info)
        talk(info)
    except:
        talk('Sorry, could not find any information')


def tell_joke():
    talk(pyjokes.get_joke())


def respond_to_greeting():
    talk('Yes, I am here. How can I help you?')


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        play_song(song)
    elif 'time' in command:
        get_time()
    elif 'search for' in command or 'what is' in command:
        query = command.replace('search for', '').replace('what is', '').strip()
        search_info(query)
    elif 'joke' in command:
        tell_joke()
    elif 'hello' in command or 'hi' in command or 'hey' in command:
        respond_to_greeting()
    else:
        talk('Sorry, I did not understand that. Please say the command again.')


while True:
    run_alexa()
