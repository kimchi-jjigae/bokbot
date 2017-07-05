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
    
    def __send(self, string):
        self.__s.send(string.encode())
        
    def __sendPRIVMSG(self, message):
        msg = "PRIVMSG %s :%s\r\n" % (self.__channel, message)
        self.__send(msg)

    def __getNick(self, lineHere):
        num = lineHere.find("!")
        nick = lineHere[1:num]
        return nick

    def __dance(self, line):
        dances = ["ruffles its pages", "beeps", "dusts itself off", "squeaks rustily", "dances", "flutters its eyelids"]
        random.shuffle(dances)
        self.__sendPRIVMSG("\x01ACTION %s\x01" % dances[0])

    def r_join(self, line):
        self.__send("JOIN %s\r\n" % self.__channel)

    def r_hi(self, line):
        nick = self.__getNick(line)
        if nick == self.__nick:
            self.__sendPRIVMSG("Hello %s! ^_^" % self.__channel)
        else:
            self.__sendPRIVMSG("Hello %s! :)" % nick)

    def r_bye(self, line):
        nick = self.__getNick(line)
        self.__sendPRIVMSG("Good bye %s! (:" % nick)

    __responses = {
        '001': r_join,
        'PART': r_bye,
        'QUIT': r_bye,
        'JOIN': r_hi,
        #'PRIVMSG': r_join,
    }

    def run(self):
        while 1:
            self.__readbuffer = self.__readbuffer + self.__s.recv(1024).decode()
            temp = self.__readbuffer.split("\r\n")
            self.__readbuffer = temp.pop()

            for line in temp:
                print(line)

                words = line.split(" ")       # split line into words
                if words[0] == "PING":
                    self.__send("PONG %s\r\n" % words[1])
                else:
                    command = words[1]
                    if command in self.__responses:
                        self.__responses[command](self, line)

                #elif words[1] == "PART" or words[1] == "QUIT":

                #elif words[1] == "KICK":                     # not tested yet
                #    partingNick = words[3]
                #    self.__names.remove(partingNick)
                #    
                #elif words[1] == "JOIN":
                #    joiningNick = self.__getNick(line)
                #    self.__names.append(joiningNick)

                #elif words[1] == "NICK":
                #    changingNick = self.__getNick(line)
                #    newNick = words[2]
                #    newNick = newNick.replace(":", "", 1)
                #    self.__names.append(newNick)
                #    self.__names.remove(changingNick)

                if words[1] == "PRIVMSG":
                    ## to make sure channel name is caps-insensitive
                    bajs = re.compile("%s" % self.__channel, re.I)
                    channelMessage = bajs.findall(line)            
                    sender = self.__getNick(line)

                    if channelMessage:                                  
                        message = line.split("%s :" % channelMessage[0])[1]
                        messageAsWords = message.split(" ")

                        if messageAsWords[0] == ".dance":
                            self.__dance()

