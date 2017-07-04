# -*- coding: utf-8 -*-i
# NB: the IRC protocol limits message lengths to 512 bytes, not just the
# message part but of course the whole command etc.
import re
import sys
import socket
import random
from booksplitter import BookSplitter

class BokBot:
    def __init__(self, host, channel):
        __host = host
        __port = 6667
        __channel = channel
        __nick = "bokbot"
        __ident = "bokbot"
        __realname = "kims bokbot" 

        s=socket.socket()	
        s.connect((HOST, PORT))

        nick_string = "NICK %s\r\n" % self.__nick
        user_string = "USER %s %s plopp :%s\r\n" % (self.__ident,
            self.__host, self.__realname)
        s.send(nick_string.encode())
        s.send(user_string.encode())
        # username hostname servername realname

        __readbuffer = ""
        __joinStatus = False
        __names = []
        
        __prefix = "."
    
    def __sendPRIVMSG(self, message):
        msg = "PRIVMSG %s :%s\r\n" % (self.__channel, message)
        s.send(msg.encode())

    def __getNick(self, lineHere):
        num = lineHere.find("!")
        nick = line[1:num]
        return nick

    def __dance(self):
        dances = ["ruffles its pages", "beeps", "dusts itself off"]
        random.shuffle(dances)
        self.__sendPRIVMSG("\x01ACTION %s\x01" % dances[0])

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
                partingNick = self.__getNick(line)
                names.remove(partingNick)

            elif words[1] == "KICK":                     # not tested yet
                print("names before kick:", names)
                partingNick = words[3]
                names.remove(partingNick)
                print("names after kick:", names)
                
            elif words[1] == "JOIN":
                joiningNick = self.__getNick(line)
                names.append(joiningNick)

            elif words[1] == "NICK":
                changingNick = self.__getNick(line)
                newNick = words[2]
                newNick = newNick.replace(":", "", 1)
                names.append(newNick)
                names.remove(changingNick)

            elif words[1] == "PRIVMSG":
                ## to make sure channel name is caps-insensitive
                bajs = re.compile("%s" % CHANNEL, re.I)
                channelMessage = bajs.findall(line)            
                sender = self.__getNick(line)

                if channelMessage:                                  # make one day a function, to be able to reply to others, too, perhaps even multichannel :o
                    message = line.split("%s :" % channelMessage[0])[1]
                    messageAsWords = message.split(" ")

                    if messageAsWords[0] == ".dance":
                        self.__dance()

bokbot = BokBot("irc.boxbox.org", "#bokbot")
