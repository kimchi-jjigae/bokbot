# -*- coding: utf-8 -*-i
# given commands, return strings, or something like that?

from botaction import BotActor
import re

class Response:
    def __init__(self, command, response):
        self.command = command
        self.response = response

class BotResponder:
    __a = BotActor()

    def __init__(self, channel, nick):
        self.__channel = channel
        self.__nick = nick
        self.__responses = {
            '001': self.r_join,
            'PART': self.r_bye,
            'QUIT': self.r_bye,
            'JOIN': self.r_hi,
            'PRIVMSG': self.r_read,
        }
        
    def pong(self, server):
        return "PONG %s\r\n" % server

    def respond(self, command, line):
        if command in self.__responses:
            r = self.__responses[command](line)
            return r

    def r_join(self, line):
        return "JOIN %s\r\n" % self.__channel

    def r_hi(self, line):
        nick = self.__getNick(line)
        if nick == self.__nick:
            msg = "Hello %s! ^_^" % self.__channel
        else:
            msg = "Hello %s :)" % nick
        return self.__PRIVMSGify(msg)

    def r_bye(self, line):
        nick = self.__getNick(line)
        return self.__PRIVMSGify("Good bye %s (:" % nick)

    def r_read(self, line):
        ## to make sure channel name is caps-insensitive
        bajs = re.compile("%s" % self.__channel, re.I)
        channel_message = bajs.findall(line)            
        sender = self.__getNick(line)

        if channel_message: # as opposed to pm
            message = line.split("%s :" % channel_message[0])[1]
            message_words = message.split(" ")

            word1 = message_words[0]
            if(word1 == "lol" or word1 == "haha"):
                a = self.__a.act('lol', message_words)
                return self.__PRIVMSGify(a)
#            elif(word1.isdigit()):
#                self.a_next(int(word1))
#            elif(word1 == ''):
#                self.a_next(1)
#            elif(word1[0] == self.__prefix):
#                action = word1[1:]
#                if action in self.__actions:
#                    self.a_generic(action, message_words)

    def __getNick(self, lineHere):
        num = lineHere.find("!")
        nick = lineHere[1:num]
        return nick

    def __PRIVMSGify(self, message):
        return "PRIVMSG %s :%s\r\n" % (self.__channel, message)
