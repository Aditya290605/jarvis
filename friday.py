import smtplib
import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import os
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import time
import pyjokes

from PyQt5 import QtWidgets , QtCore, QtGui
from PyQt5.QtCore import QTime,QTime, QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from GUI import Ui_Friday

listener = sr.Recognizer()
engine = pyttsx3.init()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate',190)
engine.setProperty('voices',voices[1].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and  hour<=12:
        speak("Good morning sir")
    elif hour>12 and hour<18:
        speak("Good Afternoon sir")
    else:
        speak("Good eveing sir")

    speak("i am friday your assistant. please tell me how may i help you ?")


import requests

def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=83263a48521a48a797182dbc3926e513'

    main_page = requests.get(main_url)
    articles = main_page.json()["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles[:10]:
        head.append(ar["title"])
    for i in range(len(head)):
        speak(f"Today's {day[i]} news is: {head[i]}")

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takecommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening.....")
            r.pause_threshold=1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio,language='en-in')
            print(f"user said: {query}")

        except Exception as e :
            speak("Say that again please ..")
            return "none"
        return query

    def TaskExecution(self):
        wish()
        while True:


            self.query = self.takecommand().lower()

            if "open notepad" in self.query:
                npath = "C:\\Windows\\system32\\notepad.exe"
                os.startfile(npath)

            if "hello friday how are you " in self.query:
                speak("Oh hello sir , i am perfectly fine how are you sir ?")
                continue

            elif "command prompt" in self.query:
                os.system("start cmd")

            elif "play music" in self.query:
                music_dir = "D:\\Drivers\\music"
                song = os.listdir(music_dir)
                rd = random.choice(song)
                os.startfile(os.path.join(music_dir,rd))

            elif "ip address" in self.query:
                ip = get('https://api.ipify.org').text
                speak(f"your IP address is {ip}")


            elif "youtube" in self.query:
                webbrowser.open("www.youtube.com")

            elif "facebook" in self.query:
                webbrowser.open("www.facebook.com")

            elif "instagram" in self.query:
                webbrowser.open("www.instagram.com")

            elif "stackoverflow" in self.query:
                webbrowser.open("www.stackoverflow.com")

            elif "open google" in self.query:
                speak("Sir , what should i search on google ?")
                cm = self.takecommand().lower()
                webbrowser.open(f"{cm}")

            elif "send message" in self.query:
                kit.sendwhatmsg("+918888481528","Hi i am firday hello!",2,25)

            elif "play song on youtube" in self.query:
                speak("Sir , which song would you like to listen?")
                play = self.takecommand().lower()
                kit.playonyt(f"{play}")


            elif "you can sleep" in self.query:
                speak("Okay sir im here if you need me again. good day sir !")

                break


            elif "tell me joke" in self.query:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "shut down system" in self.query:
                os.system("shutdown /s /t 5")

            elif "reset system" in self.query:
                os.system("shutdown /r /t 5")

            elif "sleep down system" in self.query:
                os.system("rundll322.exe powrprof.dll,SetSuspendState 0,1,0")


            elif "change window" in self.query:
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(1)
                pyautogui.keyUp("alt")

            elif "tell me news" in self.query:
                speak("please wait sir, collecting latest news")
                news()

startExecution = MainThread()

class Main(QMainWindow):
        def __init__(self):
            super().__init__()
            self.ui = Ui_Friday()
            self.ui.setupUi(self)
            self.ui.pushButton.clicked.connect(self.startTask)
            self.ui.pushButton_2.clicked.connect(self.close)

        def startTask(self):
            self.ui.movie = QtGui.QMovie("C:/Users/Lenovo/Downloads/05bd96100762b05b616fb2a6e5c223b4.gif")
            self.ui.label_2.setMovie(self.ui.movie)
            self.ui.movie.start()
            self.ui.movie = QtGui.QMovie("C:/Users/Lenovo/Downloads/jjxe0tre9jftihzqp4aw.gif")
            self.ui.label_3.setMovie(self.ui.movie)
            self.ui.movie.start()
            timer = QTimer(self)
            timer.timeout.connect(self.showTime)
            timer.start(1000)
            startExecution.start()

        def showTime(self):
            current_time = QTime.currentTime()
            current_date = QDate.currentDate()
            label_time=current_time.toString('hh:mm:ss')
            label_date = current_date.toString(Qt.ISODate)
            self.ui.textBrowser.setText(label_date)
            self.ui.textBrowser_2.setText(label_time)




app = QApplication(sys.argv)
friday = Main()
friday.show()
exit(app.exec_())