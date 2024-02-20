import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import tkinter as tk

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
listening = False


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as mic:
            print('listening...')
            listener.adjust_for_ambient_noise(mic, duration=0.2)
            audio = listener.listen(mic)
            command = listener.recognize_google(audio)
            command = command.lower()
            print(command)
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except:
        pass
    return command


def get_weather(city):
    api_key = "dde28fb43f34c6caf3cbc6edd076a1e0"
    base_url = "https://api.openweathermap.org/data/2.5/weather?q="
    cmpltURL = base_url + city + "&appid=" + api_key
    response = requests.get(cmpltURL)
    weather_data = response.json()
    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    talk(f'The weather in {city} is {description} with a temperature of {temperature} degrees Celsius.')


def run_alexa():
    global listening
    while listening:
        command = take_command()
        if 'stop' in command:
            listening = False
            talk('Ok,nice helping you. Stopping Alexa. Click the button to start again.')
            break
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing ' + song)
            print('playing', song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            print(current_time)
            talk('Current time is ' + current_time)
        elif 'temperature' in command:
            city = command.split(" ")[-1]
            get_weather(city)
        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'date' in command:
            talk('Sorry, I am not a human just a Mushkan\'s Alexa')
        elif 'are you single' in command:
            talk('I am not a human, made and handled by Mushkan')
        elif 'joke' in command:
            print(pyjokes.get_joke())
            talk(pyjokes.get_joke())
        elif 'who are you' in command:
            talk('I am Mushkan\'s Alexa')
        elif 'what is your name' in command:
            talk('Myself MusAlex')
        elif 'your age' in command:
            talk('I was born on 21st December, 2023. Now just calculate on your own.')
        elif 'what you doing now' in command:
            talk('Nothing,just working for you.')
        elif 'what you doing' in command:
            talk('Nothing,just working for you.')
        elif 'who created you' in command:
            talk('Mushkan Bothra created me.')
        elif 'are you well' in command:
            talk('Don\'t worry about me. I am good!')
        elif 'how are you' in command:
            talk('I am fine.What about you?')
        elif 'i am good' in command:
            talk('oh good to know')
        elif 'i am fine' in command:
            talk('oh good to know')
        else:
            talk('Please could you repeat the command again')


def on_button_click():
    global listening
    if not listening:
        talk("Alexa is now listening. Say 'Stop' to stop.")
        listening = True
        run_alexa()
    else:
        listening = False
        talk('Ok,nice helping you.Stopping Alexa. Click the button to start again.')


# Create GUI
root = tk.Tk()
root.title("MusAlex Virtual Assistant")
root.geometry("400x200")  # set window size
root.configure(bg='lightgrey')  # set background color

button = tk.Button(root, text="Start/Stop Alexa", command=on_button_click, bg='green', fg='white', font=('Arial', 14), padx=10, pady=5,
                   borderwidth=2, relief="solid", highlightthickness=2, highlightbackground="black", highlightcolor="black")
button.pack(pady=20)

root.mainloop()
