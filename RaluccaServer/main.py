import socket
from _thread import *
import sys
import numpy as np
import io
import matplotlib.pyplot as plt
import scipy
from scipy.io.wavfile import write
import sounddevice as sd


serversocket=socket.socket()

host = "127.0.0.1"
port = 1233
ThreadCount=0

try:
    serversocket.bind((host,port))
except socket.error as e:
    print(str(e))
print("waiting for connection")
serversocket.listen(5)

def ConvertStrToList(string):
    finalList = []
    string =string.replace("[", "")
    string = string.replace("]", "")
    listOfNumbers= string.split()
    pair = []
    i=0
    for nr in listOfNumbers:
        pair.append(float(nr))
        i+=1
        if(i==2):
            finalList.append(pair)
            i=0
            pair=[]
    return finalList

def client_thread(connection):
    ThreadId= ThreadCount
    nr_of_command = 0
    while True:
        toReceive = ""

        while True:
            receive = connection.recv(4096)
            if receive.decode('utf-8')=="I finnished":
                break
            toReceive+= receive.decode('utf-8')
        recording=ConvertStrToList(toReceive)
        recordingNp = np.array(recording, dtype=float)

        write("Commands/Command" + str(nr_of_command) + "_" + str(ThreadId) + ".wav", 44100, recordingNp)

        #reply="helloCommand"
        #reply = "timeCommand"
        #reply = "byeCommand"
        reply = "jokeCommand"
        connection.send(str.encode(reply))
        nr_of_command+=1
    connection.close()

while True:
    client,address=serversocket.accept()
    print("connecte to " + str(address[0])+str(address[1]))
    start_new_thread(client_thread, (client,))
    ThreadCount+=1
    print("ThreadNumber"+str(ThreadCount))
serversocket.close()
