# -*- coding: utf-8 -*-i
# NB: the IRC protocol limits message lengths to 512 bytes, not just the
# message part but of course the whole command etc.

import re
import sys
import socket
import random
from booksplitter import BookSplitter
from wiktionaryparser import WiktionaryParser

class BokBot:
    __port = 6667
    __nick = "bokbot"
    __ident = "bokbot"
    __realname = "kims bokbot" 

    __readbuffer = ""
    __joinStatus = False
    __names = []
    
    __prefix = "."

    __dances = ["ruffles its pages", "beeps", "dusts itself off", "squeaks rustily", "dances", "flutters its eyelids"]

    __sentence = 0
    __sentence_total = 0

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

    def a_generic(self, action, message_words):
        fn, n = self.__actions[action]
        if(len(message_words) > n):
            fn(self, message_words)
        
    def a_dance(self, message_words):
        random.shuffle(self.__dances)
        self.__sendPRIVMSG("\x01ACTION %s\x01" % self.__dances[0])

    def a_next(self, n):
        # read out the next n sentences
        self.__sendPRIVMSG("Implement this command! (:")

    def a_back(self, message_words):
        # go back n sentences
        n = message_words[1]
        if(n.isdigit()):
            pass
        else:
            return
        self.__sendPRIVMSG("Implement this command! (:")

    def a_define(self, message_words):
        # look up a word on wiktionary
        word = message_words[1]
        self.__sendPRIVMSG("Implement this command! (:")

    def a_sentence(self, message_words):
        # report which sentence the reader is up to
        self.__sendPRIVMSG("Implement this command! (:")

    def a_add(self, message_words):
        self.__sendPRIVMSG("Implement this command! (:")
    def a_list(self, message_words):
        self.__sendPRIVMSG("Implement this command! (:")
    def a_load(self, message_words):
        # load a book from the list
        # also change the topic to say what's being read
        self.__sendPRIVMSG("Implement this command! (:")
    def a_skipto(self, message_words):
        self.__sendPRIVMSG("Implement this command! (:")

    __actions = {
        'dance': (a_dance, 0),
        'back': (a_back, 1),
        'define': (a_define, 1),
        'sentence': (a_sentence, 0),

        'add': (a_add, 1),
        'list': (a_list, 0),
        'load': (a_load, 1),
        'skipto': (a_skipto, 1)
    }

    def r_join(self, line):
        self.__send("JOIN %s\r\n" % self.__channel)

    def r_hi(self, line):
        nick = self.__getNick(line)
        if nick == self.__nick:
            self.__sendPRIVMSG("Hello %s! ^_^" % self.__channel)
        else:
            self.__sendPRIVMSG("Hello %s :)" % nick)

    def r_bye(self, line):
        nick = self.__getNick(line)
        self.__sendPRIVMSG("Good bye %s (:" % nick)

    def r_read(self, line):
        nick = self.__getNick(line)

        ## to make sure channel name is caps-insensitive
        bajs = re.compile("%s" % self.__channel, re.I)
        channel_message = bajs.findall(line)            
        sender = self.__getNick(line)

        if channel_message:                                  
            message = line.split("%s :" % channel_message[0])[1]
            message_words = message.split(" ")

            word1 = message_words[0]
            if(word1 == "lol" or word1 == "haha"):
                self.__sendPRIVMSG("haha")
            elif(word1.isdigit()):
                self.a_next(int(word1))
            elif(word1 == ''):
                self.a_next(1)
            elif(word1[0] == self.__prefix):
                action = word1[1:]
                if action in self.__actions:
                    self.a_generic(action, message_words)

    __responses = {
        '001': r_join,
        'PART': r_bye,
        'QUIT': r_bye,
        'JOIN': r_hi,
        'PRIVMSG': r_read,
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

