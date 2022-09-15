import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import time
from googlesearch import search
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
import smtplib

engine = pyttsx3.init('sapi5')  # to use inbuilt voice
voices = engine.getProperty('voices')


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    t = times()
    if hour >= 0 and hour < 12:
        speak(f"Good Morning")
    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon")
    else:
        speak("Good Evening")


def takeCommand():
    # it takes microphone input from user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.........")
        speak("Listening.........")
        r.pause_threshold = 0.5
        audio = r.listen(source)
    try:
        print("Recognising.......")
        speak("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}")
    except Exception as e:
        print(e)
        print("Can you repeat please")
        speak("Can you repeat please")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smntp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("sheikhaman1979@gmail.com", "Sheikh@1234")
    server.sendmail("sheikhaman1979@gmail.com", to, content)
    server.close()


def times():
    strtime = datetime.datetime.now().strftime("%H:%M:%S")
    return strtime


class WelcomeScreen(Screen):

    def greet(self):
        speak("This is a Virtual Assistant App, PLease choose your desired voice")


class TimerScreen(Screen):
    my_text = StringProperty("Hello!")
    count = 0
    inputTime = ""

    def on_button_click(self):
        self.count += 1
        self.my_text = str(self.count)

    def getTimeValue(self, value):
        self.inputTime = value

    def setTimer(self):
        num = self.count
        q = self.inputTime
        if q == 'minutes':
            timer = 0
            speak(f"timer set for {num} minutes")
            while timer != num:
                time.sleep(60)
                timer += 1
            q = ''
            for _ in range(0, 5):
                speak("Time's up.")
        elif q == "hours":
            timer = 0
            speak(f"timer set for {num} hours")
            while timer != num:
                time.sleep(3600)
                timer += 1
            for _ in range(0, 5):
                speak("Time's up.")
        elif q == "seconds":
            timer = 0
            print(num)
            print(q)
            speak(f"timer set for {num} seconds")
            while timer != num:
                time.sleep(1)
                timer += 1
            for _ in range(0, 5):
                speak("Time's up.")


class MainScreen(Screen):

    def introduction_female(self):
        engine.setProperty('voice', voices[1].id)
        wishMe()
        speak("My name is friday, And I am going to be your virtual assistant")

    def introduction_male(self):
        engine.setProperty('voice', voices[0].id)
        wishMe()
        speak("My name is Jarvis")
        speak("And I am going to be your virtual assistant")
        speak("Please Press the button for input")


class InputScreen(Screen):
    my_text = StringProperty("Click Here for input")
    tasks = []

    def Input(self):
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        query = takeCommand().lower()
        self.my_text = query
        if 'wikipedia' in query:
            print("Searching Wikipedia...")
            speak(f"Searching Wikipedia for {query}")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            print(results)
            speak(results)

        elif 'youtube' in query:
            speak("opening youtube")
            webbrowser.get(chrome_path).open("youtube.com")
            speak("Enjoy watching youtube")

        elif 'google' in query:
            speak("opening google")
            webbrowser.get(chrome_path).open("google.com")

        elif 'search' in query:
            query = query.replace('search', '')
            print(query)
            url = search(query, tld="co.in", num=10, stop=10, pause=2)
            q = next(url)
            speak(f"Searching {query}")
            webbrowser.open(q)

        elif 'hackerrank' in query:
            speak("opening Hackerrank")
            webbrowser.get(chrome_path).open(
                "https://www.hackerrank.com/dashboard")

        elif 'gmail' in query:
            speak("opening gmail")
            webbrowser.get(chrome_path).open("gmail.com")

        elif 'current time' in query:
            ti = times()
            speak(f"The time is {ti}")
            print(ti)

        elif 'code' in query:
            speak("opening Vs code")
            codepath = "C:\\Users\\Aman Sheikh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codepath)

        elif 'studio' in query:
            speak("opening android studio")
            andpath = "C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe"
            os.startfile(andpath)

        elif 'idea' in query:
            speak("opening intellijidea")
            intellipath = "C:\\Program Files\\JetBrains\\IntelliJ IDEA Community Edition 2021.2.1\\bin\\idea64.exe"
            os.startfile(intellipath)
        elif 'send email' in query:
            try:
                speak("what is the content of email")
                content = takeCommand()
                speak("to whom do you want to end it")
                to = takeCommand().lower()
                sendEmail(to+"@gmail.com", content)
                speak("Email has been is sent")
            except Exception as e:
                speak("there was an error")
        elif 'create to do' in query:
            speak("Adding tasks")
            task = ""
            while task != 'finish':
                task = takeCommand()
                self.tasks.append(task)
            self.tasks.pop()
            speak("Your todays todo list is:")
            print("***************************")
            for t in self.tasks:
                speak(t)
                print(t)
            print("***************************")
        elif 'my to do' in query:
            speak("Your todays todo list is")
            for i in range(0, len(self.tasks)):
                speak(self.tasks[i])


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file('va.kv')


class vaApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    vaApp().run()
