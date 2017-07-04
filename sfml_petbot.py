# -*- coding: utf-8 -*-i
# NB: the IRC protocol limits message lengths to 512 bytes, not just the
# message part but of course the whole command etc.
import re
import sys
import socket
import string
import random
from booksplitter import BookSplitter

HOST = "irc.boxbox.org"
PORT = 6667
CHANNEL = "#bokbot"
NICK = "bokbot"
IDENT = "bokbot"
REALNAME = "kims bokbot" 

s=socket.socket()	
s.connect((HOST, PORT))
test = "NICK %s\r\n" % NICK
s.send(test.encode())
#s.send("NICK %s\r\n" % NICK)
test = "USER %s %s plopp :%s\r\n" % (IDENT, HOST, REALNAME)
s.send(test.encode())
#s.send("USER %s %s plopp :%s\r\n" % (IDENT, HOST, REALNAME))
# username hostname servername realname

readbuffer = ""
joinStatus = False
names = []
    
def sendPRIVMSG(message):
    test = "PRIVMSG %s :%s\r\n" % (CHANNEL, message)
    s.send(test.encode())
    #s.send("PRIVMSG %s :%s\r\n" % (CHANNEL, message))

def grabFirstNick(lineHere):
    num = lineHere.find("!")
    firstNick = line[1:num]
    return firstNick

def petCommand(names, messageAsWords):
    if len(messageAsWords) > 1:
        nicke = messageAsWords[1]
        if nicke != "" and nicke in names:
            sendPRIVMSG("\x01ACTION pets %s\x01" % nicke)                  
        else:
            sendPRIVMSG("No such nick.")
    else:
        sendPRIVMSG("Usage: '.pet <nick>'")

def help():
    sendPRIVMSG("I will drown your sorrows, comfort you when you are in need, be the light in your darkest moments.")
    
while 1:
    readbuffer = readbuffer + s.recv(1024).decode()
    temp = readbuffer.split("\r\n")
    readbuffer = temp.pop()
    print(temp)

    for line in temp:

        words = line.split(" ")       # split line into words
        if words[0] == "PING":
            test = "PONG %s\r\n" % words[1]
            s.send(test.encode())
            #s.send("PONG %s\r\n" % words[1])

        elif words[1] == "001":
            print(u"Received WELCOME message. :)")
            test = "JOIN %s\r\n" % CHANNEL
            s.send(test.encode())
            #s.send("JOIN %s\r\n" % CHANNEL)
            joinStatus = True

        elif words[1] == "353":
            pattern = re.compile('[&@~+%]')
            nnicks = line.split("%s :" % CHANNEL)[1]
            names = nnicks.split(" ")             
            if "" in names:
                names.remove("")
            for i, item in enumerate(names):
                names[i] = re.sub(pattern, "", names[i])

        elif words[1] == "PART" or words[1] == "QUIT":
            partingNick = grabFirstNick(line)
            names.remove(partingNick)

        elif words[1] == "KICK":                     # not tested yet
            print("names before kick:", names)
            partingNick = words[3]
            names.remove(partingNick)
            print("names after kick:", names)
            
        elif words[1] == "JOIN":
            joiningNick = grabFirstNick(line)
            names.append(joiningNick)

        elif words[1] == "NICK":
            changingNick = grabFirstNick(line)
            newNick = words[2]
            newNick = newNick.replace(":", "", 1)
            names.append(newNick)
            names.remove(changingNick)

        elif words[1] == "PRIVMSG":
            ## to make sure channel name is caps-insensitive
            bajs = re.compile("%s" % CHANNEL, re.I)
            channelMessage = bajs.findall(line)            
            sender = grabFirstNick(line)

            if channelMessage:                                  # make one day a function, to be able to reply to others, too, perhaps even multichannel :o
                message = line.split("%s :" % channelMessage[0])[1]
                messageAsWords = message.split(" ")
                #smileyRE = re.compile("([>D)\]]-?[:=])|([:=]-?[cC(\[<])")             #implement this pls: like "if smileyRE.findall(message)" instead of foundSmilies
                smilies = ['D:', ':C', '):', ':(', ':-(', ')-:', ':[', ':<']
                foundSmilies = [smiley for smiley in smilies if smiley in message]

                if joinStatus and foundSmilies:
                    sendPRIVMSG("\x01ACTION pets %s\x01" % sender)             

                if message == "\x01ACTION pets %s\x01" % NICK or message == "\x01ACTION pets %s \x01" % NICK:
                    replies = ["Yay! ^_^", ":)", "Thank you!"]
                    random.shuffle(replies)
                    sendPRIVMSG("%s" % replies[0])             

                if messageAsWords[0] == ".pet":
                    petCommand(names, messageAsWords)

                if messageAsWords[0] == ".help":
                    help()
