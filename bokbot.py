# -*- coding: utf-8 -*-i
# NB: the IRC protocol limits message lengths to 512 bytes, not just the
# message part but of course the whole command etc.
import re
import sys
import socket
import random
from booksplitter import BookSplitter

class BokBot:
    __port = 6667
    __nick = "bokbot"
    __ident = "bokbot"
    __realname = "kims bokbot" 

    __readbuffer = ""
    __joinStatus = False
    __names = []
    
    __prefix = "."

    def __init__(self, host, channel):
        self.__host = host
        self.__channel = channel

        self.__s=socket.socket()	
        self.__s.connect((self.__host, self.__port))

        nick_string = "NICK %s\r\n" % self.__nick
        user_string = "USER %s %s plopp :%s\r\n" % (self.__ident,
            self.__host, self.__realname)
        self.__s.send(nick_string.encode())
        self.__s.send(user_string.encode())
    
    def __sendPRIVMSG(self, message):
        msg = "PRIVMSG %s :%s\r\n" % (self.__channel, message)
        self.__s.send(msg.encode())

    def __getNick(self, lineHere):
        num = lineHere.find("!")
        nick = lineHere[1:num]
        return nick

    def __dance(self):
        dances = ["ruffles its pages", "beeps", "dusts itself off"]
        random.shuffle(dances)
        self.__sendPRIVMSG("\x01ACTION %s\x01" % dances[0])

    def run(self):
        while 1:
            self.__readbuffer = self.__readbuffer + self.__s.recv(1024).decode()
            temp = self.__readbuffer.split("\r\n")
            self.__readbuffer = temp.pop()
            print(temp)

            for line in temp:

                words = line.split(" ")       # split line into words
                if words[0] == "PING":
                    test = "PONG %s\r\n" % words[1]
                    self.__s.send(test.encode())
                    #self.__s.send("PONG %s\r\n" % words[1])

                elif words[1] == "001":
                    print(u"Received WELCOME message. :)")
                    test = "JOIN %s\r\n" % self.__channel
                    self.__s.send(test.encode())
                    #self.__s.send("JOIN %s\r\n" % self.__channel)
                    joinStatus = True

                elif words[1] == "353":
                    pattern = re.compile('[&@~+%]')
                    nnicks = line.split("%s :" % self.__channel)[1]
                    self.__names = nnicks.split(" ")             
                    if "" in self.__names:
                        self.__names.remove("")
                    for i, item in enumerate(self.__names):
                        self.__names[i] = re.sub(pattern, "", self.__names[i])

                elif words[1] == "PART" or words[1] == "QUIT":
                    partingNick = self.__getNick(line)
                    self.__names.remove(partingNick)

                elif words[1] == "KICK":                     # not tested yet
                    partingNick = words[3]
                    self.__names.remove(partingNick)
                    
                elif words[1] == "JOIN":
                    joiningNick = self.__getNick(line)
                    self.__names.append(joiningNick)

                elif words[1] == "NICK":
                    changingNick = self.__getNick(line)
                    newNick = words[2]
                    newNick = newNick.replace(":", "", 1)
                    self.__names.append(newNick)
                    self.__names.remove(changingNick)

                elif words[1] == "PRIVMSG":
                    ## to make sure channel name is caps-insensitive
                    bajs = re.compile("%s" % self.__channel, re.I)
                    channelMessage = bajs.findall(line)            
                    sender = self.__getNick(line)

                    if channelMessage:                                  # make one day a function, to be able to reply to others, too, perhaps even multichannel :o
                        message = line.split("%s :" % channelMessage[0])[1]
                        messageAsWords = message.split(" ")

                        if messageAsWords[0] == ".dance":
                            self.__dance()

bokbot = BokBot("irc.boxbox.org", "#bokbot")
bokbot.run()
