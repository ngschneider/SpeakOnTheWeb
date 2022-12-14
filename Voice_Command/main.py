#!/usr/bin/env python
from torch.nn.modules.activation import Softmax
from listen import startListening
from communicate import speak
import PySimpleGUI as sg
from PIL import Image, ImageTk, ImageSequence 
from calculations import addition, subtraction, division, multiplication, tothePower, percentages
from variousSearch import googleSearch, play, findInfo, chooseGenre
import datetime
import random
import torch
import json
import os
from training.model import NeuralNet
from training.nltkutilities import tokenize, bag_of_words

# from userinterface import *
#checking import

from PyQt5 import QtCore

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
            AssistantSignals().search.emit(query)
        else :
            self.speak("What do you want me to search ?")

def do_open_new_tab(self):
    speak("Opening new tab for you")
    AssistantSignals().openNewTab.emit()

def do_close_tab(self):
    speak("Okay, closing current tab")
    AssistantSignals().closeCurrentTab.emit()


def do_open_new_window(self):
    speak("Opening new window for you")
    AssistantSignals().openNewWindow.emit()

def do_close_window(self):
    speak("Okay, closing  current window")
    AssistantSignals().closeCurrentWindow.emit()

def do_exit_browser(self):
    speak("Okay, exiting")
    AssistantSignals().bye.emit()


def do_goback(self):
    speak("Opening new tab for you")
    AssistantSignals().back.emit()

def do_goforward(self):
    speak("Going back to previous web page")
    AssistantSignals().forward.emit()

def do_reload_page(self):
    speak("Wait a second reloading current web page")
    AssistantSignals().reload.emit()

def do_gohome(self):
    speak("Going back to homepage")
    AssistantSignals().homepage.emit()


if __name__ == '__main__':


    #Allows use of cuda or cpu for computing prediction
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    print(os.getcwd())
    #read from json data for getting responses based on asked questions
    with open('Voice_Command/intents.json', 'r') as json_data:
       intents = json.load(json_data) 

    #File contains model trained
    FILE = "Voice_Command/data.pth"
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

    
    #listening starts here
    #readFromFile()
    while True:
        command = startListening()
        # After activating the listener the browser will continue
        # to listen for instructions until user utters the exit command.
        # Another approach will be a timeout after a specific amount of 
        # seconds. 
        if 'exit' in command or 'go away' in command:
            break

        elif('time' in command):
            time = datetime.datetime.now().strftime('%I:%M:%p')
            speak("The current time is, " + time)
        else:
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

            #runs if probability high
            if prob.item() > 0.75 :
                for intent in intents["intents"]:
                    if tag == intent["tag"]:
                        response = random.choice(intent["responses"])
                        ActionController.browserAction()
                        if tag == "youtube":
                            #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                tokenizeTokens = tokenize(tokens)
                              
                                for t in tokenizeTokens:
                                    
                                    if t in command:
                                        command.remove(tokens)
                            videoTitle = ' '.join(command)
                            speak(response+videoTitle)
                            play(videoTitle)
                            
                        
                        
                        elif tag == "search":
                            print(command)
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

                        elif tag == 'info':
                        #removes what users say and tells the remaining words for searching and informing user
                            for tokens in intent["patterns"]:
                                if tokens in command:
                                    command.remove(tokens)
                            searchInfo = ' '.join(command)
                            speak(response)
                            speak(findInfo(searchInfo))

                        #calculations
                        elif tag == 'add':
                            searchInfo =' '.join(command)
                            speak(response+addition(searchInfo))
                        
                        elif tag == 'subtract':
                            searchInfo =' '.join(command)
                            speak(response+subtraction(searchInfo))
                        
                        elif tag == 'multiply':
                            searchInfo =' '.join(command)
                            speak(response+multiplication(searchInfo))
                        
                        elif tag == 'divide':
                            searchInfo =' '.join(command)
                            speak(response+division(searchInfo))
                        
                        elif tag == 'percent':
                            searchInfo =' '.join(command)
                            speak(response+percentages(searchInfo))
                        
                        elif tag == 'power':
                            searchInfo =' '.join(command)
                            speak(response+tothePower(searchInfo))
                        
                        elif tag == 'suggest':
                            speak("Sorry, that is not available yet")

                        else:
                            #A response generated by AI
                            speak(response)
                            
                    
                         
            else:
                #response if user talks jibberish
                #speak("Ok")
                print()
            

    quit()
  
        






