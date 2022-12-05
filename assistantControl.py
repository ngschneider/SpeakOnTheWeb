#!/usr/bin/env python
from torch.nn.modules.activation import Softmax
from listen import startListening
from communicate import speak
from variousSearch import play, findInfo
import torch
import json
from training.model import NeuralNet
from training.nltkutilities import tokenize, bag_of_words
from userInterfacePy import *
import random
# from uiControls import *

from PyQt5 import QtCore
myReply2 = open('history/reply.txt', 'a')
    
# Wake word in Listen Function
WAKE = "Browsie"
class AssistantSignals(QtCore.QObject):
    welcome = QtCore.pyqtSignal()
    openNewTab = QtCore.pyqtSignal()
    openNewWindow = QtCore.pyqtSignal()
    closeCurrentTab = QtCore.pyqtSignal()
    closeCurrentWindow = QtCore.pyqtSignal()
    reload = QtCore.pyqtSignal()
    back = QtCore.pyqtSignal()
    forward = QtCore.pyqtSignal()
    homepage = QtCore.pyqtSignal()
    bye  = QtCore.pyqtSignal()
    search = QtCore.pyqtSignal(str)

def do_search(self,cmd):
        kwords = cmd.split()
        if len(kwords)>1:
            kwords = kwords[1:]
            query = ""
            for w in kwords:
                query += w
            speak("Searching "+query+" on the web for you.")
            myReply2.write("Searching "+query+" on the web for you.")
            AssistantSignals().search.emit(query)
        else :
            self.speak("What do you want me to search ?")
            myReply2.write("What do you want me to search ?")

def do_open_new_tab(self):
    speak("Opening new tab for you")
    myReply2.write("Opening new tab for you")
    AssistantSignals().openNewTab.emit()

def do_close_tab(self):
    speak("Okay, closing current tab")
    myReply2.write("Okay, closing current tab")
    AssistantSignals().closeCurrentTab.emit()


def do_open_new_window(self):
    speak("Opening new window for you")
    myReply2.write("Opening new window for you")
    AssistantSignals().openNewWindow.emit()

def do_close_window(self):
    speak("Okay, closing  current window")
    myReply2.write("Okay, closing  current window")
    AssistantSignals().closeCurrentWindow.emit()

def do_exit_browser(self):
    speak("Okay, exiting")
    myReply2.write("Okay, exiting")
    AssistantSignals().bye.emit()


def do_goback(self):
    speak("Opening new tab for you")
    myReply2.write("Opening new tab for you")
    AssistantSignals().back.emit()

def do_goforward(self):
    speak("Going back to previous web page")
    myReply2.write("oing back to previous web page")
    AssistantSignals().forward.emit()

def do_reload_page(self):
    speak("Wait a second reloading current web page")
    myReply2.write("Wait a second reloading current web page")
    AssistantSignals().reload.emit()

def do_gohome(self):
    speak("Going back to homepage")
    myReply2.write("Going back to homepage")
    AssistantSignals().homepage.emit()



def assistantController():
    #Allows use of cuda or cpu for computing prediction
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    #read from json data for getting responses based on asked questions
    with open('intents.json', 'r') as json_data:
       intents = json.load(json_data) 

    #File contains model trained
    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data["all_words"]
    tags = data["tags"]
    model_state = data["model_state"]

    #Gets model up and running
    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    f1 = False
    #listening starts here
    #readFromFile()
    myCommands = open('history/commands.txt', 'w')
    myCommands.write('')
    myReply = open('history/reply.txt', 'w')
    myReply.write('')
    myCommands.close()
    myReply.close()
    while True:
        command = startListening()
        # if stopEvent.is_set():
        #     break
        myCommands = open('history/commands.txt', 'a')
        myReply = open('history/reply.txt', 'a')
        myCommands.write(command)
        if "hey browser" in command:
            speak("Listening...")
            f1 = True
            
        # After activating the listener the browser will continue
        # to listen for instructions until user utters the exit command.
        # Another approach will be a timeout after a specific amount of 
        # seconds. 
        elif 'exit' in command or 'go away' in command:
            myFile = open('history/closure.txt', 'w')
            myFile.write('1')
            myFile.close()
            myCommands.close()
            myReply.close()
            myReply2.close()
            break
        elif 'dark mode' in command or 'light mode' in command or 'change mode' in command:
            with open('images/savedState.txt') as f:
                lines = f.readlines()
            if lines[0] == '0':
                bGround = 'w'
            else:
                bGround = 'd'
            if 'dark mode' in command:
                if bGround == 'd':
                    speak('Already in dark mode')
                    myReply.write('Already in dark mode')
                else:
                    myFile = open('images/savedState.txt', 'w')
                    myFile.write('1')
                    myFile.close()

            elif 'light mode' in command:
                if bGround == 'w':
                    speak('Already in light mode')
                    myReply.write('Already in light mode')
                else:
                    myFile = open('images/savedState.txt', 'w')
                    myFile.write('0')
                    myFile.close()
            else:
                myFile = open('images/savedState.txt', 'w')
                if bGround == 'w':
                    myFile.write('0')
                else:
                    myFile.write('1')
                myFile.write('0')  
                
        elif f1:
            
            #convert command into a tokenized array
            command = tokenize(command)

            #get arrays to compare and predict
            X = bag_of_words(command, all_words)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(device)

            output = model(X)
            _, predicted  = torch.max(output, dim=1)

            tag = tags[predicted.item()]

            probs = torch.softmax(output, dim=1)
            prob = probs[0][predicted.item()]
            print(prob)
            #runs if probability high
            if prob.item() > 0.5 :
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        response = random.choice(intent["responses"])
                        if tag == "youtube":
                            #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                tokenizeTokens = tokenize(tokens)
                                for t in tokenizeTokens:
                                    if t in command:
                                        command.remove(tokens)
                            videoTitle = ' '.join(command)
                            speak(response+videoTitle)
                            myReply.write(response+videoTitle)
                            play(videoTitle)

                        elif tag == "search":
                            do_search(command)

                        elif tag == "open_tab":
                            do_open_new_tab()

                        elif tag == "open_window":
                            do_open_new_window()

                        elif tag == "close_window":
                            do_close_window()

                        elif tag == "close_tab":
                            do_close_tab()

                        elif tag == "goBack":
                            do_goback()

                        elif tag == "go_forward":
                            do_goforward()

                        elif tag == "home":
                            do_gohome()

                        elif tag == "reload":
                            do_reload_page()

                        elif tag == "exit":
                            do_exit_browser()           
                         
            else:
                #response if user talks jibberish
                if command == []:
                    f1 = False
                else:
                    speak("Sorry, cannot process current request.")
                    myReply.write("Sorry, cannot process current request.")
        