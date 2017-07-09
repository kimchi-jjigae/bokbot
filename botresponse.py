# -*- coding: utf-8 -*-i
# given commands, return strings, or something like that?

class Response:
    def __init__(self, command, response):
        self.command = command
        self.response = response

class BotResponder:
    __responses = {
#        '001': r_join,
#        'PART': r_bye,
#        'QUIT': r_bye,
#        'JOIN': r_hi,
#        'PRIVMSG': r_read,
    }
#
#    def __getNick(self, lineHere):
#        num = lineHere.find("!")
#        nick = lineHere[1:num]
#        return nick
#
    def __init__(self, channel):
        self.__channel = channel
        self.__responses = {
            '001': self.r_join,
        }
        
    def pong(self, server):
        return "PONG %s\r\n" % server

    def respond(self, command, line):
        if command in self.__responses:
            r = self.__responses[command](line)
            return r
        return ""

    def r_join(self, line):
        return "JOIN %s\r\n" % self.__channel

#    def r_hi(self, line):
#        nick = self.__getNick(line)
#        if nick == self.__nick:
#            self.__sendPRIVMSG("Hello %s! ^_^" % self.__channel)
#        else:
#            self.__sendPRIVMSG("Hello %s :)" % nick)
#
#    def r_bye(self, line):
#        nick = self.__getNick(line)
#        self.__sendPRIVMSG("Good bye %s (:" % nick)
#
#    def r_read(self, line):
#        nick = self.__getNick(line)
#
#        ## to make sure channel name is caps-insensitive
#        bajs = re.compile("%s" % self.__channel, re.I)
#        channel_message = bajs.findall(line)            
#        sender = self.__getNick(line)
#
#        if channel_message:                                  
#            message = line.split("%s :" % channel_message[0])[1]
#            message_words = message.split(" ")
#
#            word1 = message_words[0]
#            if(word1 == "lol" or word1 == "haha"):
#                self.__sendPRIVMSG("haha")
#            elif(word1.isdigit()):
#                self.a_next(int(word1))
#            elif(word1 == ''):
#                self.a_next(1)
#            elif(word1[0] == self.__prefix):
#                action = word1[1:]
#                if action in self.__actions:
#                    self.a_generic(action, message_words)
