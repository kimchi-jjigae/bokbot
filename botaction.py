# -*- coding: utf-8 -*-i
# given commands, return strings, or something like that? socket-independent.

class BotActor:
    def __init__(self):
        self.__actions = {
            'lol': (self.a_lol, 0),
            'next': (self.a_next, 1),
#        'dance': (a_dance, 0),
#        'back': (a_back, 1),
#        'define': (a_define, 1),
#        'sentence': (a_sentence, 0),
#
#        'add': (a_add, 1),
#        'list': (a_list, 0),
#        'load': (a_load, 1),
#        'skipto': (a_skipto, 1)
        }

    def act(self, action, message_words):
        if action in self.__actions:
            fn, n = self.__actions[action]
            if(len(message_words) >= n):
                return fn(message_words)

    def a_lol(self, message_words):
        return "haha"
#
#    def a_dance(self, message_words):
#        random.shuffle(self.__dances)
#        self.__sendPRIVMSG("\x01ACTION %s\x01" % self.__dances[0])
#
    def a_next(self, message_words):
        # read out the next n sentences
        n = int(message_words[0])
        return str(n)

#    def a_back(self, message_words):
#        # go back n sentences
#        n = message_words[1]
#        if(n.isdigit()):
#            pass
#        else:
#            return
#        self.__sendPRIVMSG("Implement this command! (:")
#
#    def a_define(self, message_words):
#        # look up a word on wiktionary
#        word = message_words[1]
#        self.__sendPRIVMSG("Implement this command! (:")
#
#    def a_sentence(self, message_words):
#        # report which sentence the reader is up to
#        self.__sendPRIVMSG("You are on sentence %d of %d."
#            % (self.__sentence, self.__sentence_total))
#
#    def a_add(self, message_words):
#        self.__sendPRIVMSG("Implement this command! (:")
#    def a_list(self, message_words):
#        self.__sendPRIVMSG("Implement this command! (:")
#    def a_load(self, message_words):
#        # load a book from the list
#        # also change the topic to say what's being read
#        #:kim!kim@Clk-91B7221E.cust.bredband2.com TOPIC #bokbot :asdf
#        self.__sendPRIVMSG("Implement this command! (:")
#    def a_skipto(self, message_words):
#        self.__sendPRIVMSG("Implement this command! (:")
