import tkinter as tk
import os
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt
import socket
import sys
import numpy as np
import io
from datetime import datetime
import time
from random import randint
from PIL import ImageTk,Image
images= None

current_image_number=0

globalcanvas2 = None
image_id=0

Page2= None
Page1= None

record= None

_entryName = None
_entrySurname = None
_entryDate = None
_entryCountry = None
_entryCity = None

globalSocket = None
globalChatText = None

def connectToServer():
    global globalSocket
    clientsocket=socket.socket()
    host="127.0.0.1"
    port = 1233

    print("waiting connection")
    try:
        clientsocket.connect((host,port))
    except socket.error as e:
        print(str(e))
    globalSocket= clientsocket

def sendToServer(toSend):
    globalSocket.send(toSend)

def recvFromServer():
    response= globalSocket.recv(1024)
    return response

def CountDown(i):
    global globalChatText
    globalChatText.insert(tk.END, str(5 - i) + "...\n")

def ClosePage():
    global Page2
    Page2.destroy()

def SayHello():
    global globalChatText
    f = open("Resources/datas.txt", "r")
    f.readline()
    nickname = f.readline()

    globalChatText.insert(tk.END, "Hello, " + nickname[0:len(nickname) - 1] + "\n")
    f.close()

def TellTheTime():
    global globalChatText
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    globalChatText.insert(tk.END, "The time is: " + current_time + "\n")

def SayGoodBye():
    global globalChatText
    f = open("Resources/datas.txt", "r")
    f.readline()
    nickname = f.readline()
    globalChatText.insert(tk.END, "Good bye, " + nickname[0:len(nickname) - 1] + "!\n")
    f.close()
    globalChatText.insert(tk.END, "The program will close in:\n")
    for i in range(5):
        Page2.after(1000 * i, CountDown, i)
    Page2.after(6000, ClosePage)

def TellAJoke():
    global globalChatText
    numberofjoke = randint(1, 6)
    f = open("Resources/Jokes/joke" + str(numberofjoke) + ".txt", "r")
    joke = f.read()
    globalChatText.insert(tk.END, joke + "\n")

def ChooseTheImage(type):
    global current_image_number
    global globalcanvas2
    global images
    global image_id
    if type=="Hello":
        current_image_number = 0
    if type=="Listen":
        current_image_number = 1
    if type=="Smile":
        current_image_number = 2
    if type=="Thinking":
        current_image_number = 3
    globalcanvas2.itemconfig(image_id, image=images[current_image_number])

def SendRecording(myrecording):

    toSend = ""
    i = 0
    for pair in myrecording:
        toSend += str(pair) + " "
        i += 1
        if i == 19:
            i = 0
            sendToServer(toSend.encode('utf-8'))
            toSend = ""
    if toSend:
        sendToServer(toSend.encode('utf-8'))
    sendToServer("I finnished".encode('utf-8'))
    receive = recvFromServer()

    if receive.decode('utf-8') == "helloCommand":
        SayHello()
    if receive.decode('utf-8') == "timeCommand":
        TellTheTime()
    if receive.decode('utf-8') == "byeCommand":
        SayGoodBye()
    if receive.decode('utf-8') == "jokeCommand":
        TellAJoke()
    Page2.after(10, ChooseTheImage, "Smile")

def Recording():
    fs = 44100
    seconds = 2
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    Page2.after(10, ChooseTheImage, "Thinking")
    Page2.after(50, SendRecording, myrecording)

def Record():
    global globalChatText
    global Page2
    Page2.after(0, ChooseTheImage, "Listen")
    Page2.after(100, Recording)

    #plt.plot(myrecording)
    #plt.show()

def createPageDatas():
    global Page1
    global _entryName
    global _entrySurname
    global _entryDate
    global _entryCountry
    global _entryCity
    root = tk.Tk()
    Page1=root
    canvas1 = tk.Canvas(root, width=800, height=500)
    canvas1.pack()

    labelName = tk.Label(root, text="Name")
    labelSurname = tk.Label(root, text="Surname")
    labelDate = tk.Label(root, text="Date of birth")
    labelCountry = tk.Label(root, text="Country")
    labelCity = tk.Label(root, text="City")
    entryName = tk.Entry(root)
    _entryName=entryName
    entrySurname = tk.Entry(root)
    _entrySurname=entrySurname
    entryDate = tk.Entry(root)
    _entryDate= entryDate
    entryCountry = tk.Entry(root)
    _entryCountry=entryCountry
    entryCity = tk.Entry(root)
    _entryCity=entryCity

    canvas1.create_window(100, 10, window=labelName)
    canvas1.create_window(200, 10, window=entryName)

    canvas1.create_window(100, 30, window=labelSurname)
    canvas1.create_window(200, 30, window=entrySurname)

    canvas1.create_window(100, 50, window=labelDate)
    canvas1.create_window(200, 50, window=entryDate)

    canvas1.create_window(100, 70, window=labelCountry)
    canvas1.create_window(200, 70, window=entryCountry)

    canvas1.create_window(100, 90, window=labelCity)
    canvas1.create_window(200, 90, window=entryCity)

    buttonFinish = tk.Button(text='Finish', command=getDatas)
    canvas1.create_window(700, 400, window=buttonFinish)
    root.mainloop()

def createRalucca():
    global Page2
    global globalChatText
    global globalcanvas2
    global image_id
    global images
    global current_image_number
    connectToServer()

    root2 = tk.Tk()
    root2.configure(background='white')
    root2.title("Ralucca")
    root2.iconphoto(False, tk.PhotoImage(file="Resources/Images/AppIcon.png"))
    Page2=root2
    canvas2=tk.Canvas(root2, width=800, height=500, bg='white')


    buttonChange = tk.Button(text='Change User', command=destroyul)
    canvas2.create_window(700, 400, window=buttonChange)

    buttonRecord = tk.Button(text='Start Rec.', command=Record)
    canvas2.create_window(600, 400, window=buttonRecord)

    images2 = [
        tk.PhotoImage(file="Resources/Images/Hello.png"),
        tk.PhotoImage(file="Resources/Images/Listen.png"),
        tk.PhotoImage(file="Resources/Images/Smile.png"),
        tk.PhotoImage(file="Resources/Images/Thinking.png"),
    ]
    images = images2
    current_image_number=0
    image_id = canvas2.create_image(300,-500,anchor='nw',image=images[current_image_number])

    chatText = tk.Text(root2,height=20,width=50)
    globalChatText=chatText
    canvas2.create_window(250,200,window=chatText)
    canvas2.pack()

    globalcanvas2= canvas2
    root2.mainloop()

def destroyul():
    Page2.destroy()
    createPageDatas()

def getDatas():
    f = open("Resources/datas.txt", "w")
    name= _entryName.get()
    surname= _entrySurname.get()
    date = _entryDate.get()
    country = _entryCountry.get()
    city = _entryCity.get()
    f.write(name+"\n"+surname+"\n"+date+"\n"+country+"\n"+city)
    print(name,surname,date,country,city)
    f.close()
    Page1.destroy()
    createRalucca()


def main():
    f = open("Resources/datas.txt", "a")
    if os.stat("Resources/datas.txt").st_size==0:
        f.close()
        createPageDatas()
    else:
        f.close()
        createRalucca()

main()
