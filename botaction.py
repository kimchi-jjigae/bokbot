# -*- coding: utf-8 -*-i
# given commands, return strings, or something like that? socket-independent.

from wiktionaryparser import WiktionaryParser
from bokreader import BokReader

import random
import re

class BotActor:
    __dances = [
        "ruffles its pages",
        "refactors its code",
        "beeps",
        "dusts itself off",
        "squeaks rustily",
        "dances",
        "flutters its eyelids"
    ]
    __parser = WiktionaryParser()

    def __init__(self, name="bokbot"):
        self.__actions = {
            'lol': (self.a_lol, 0),
            'next': (self.a_next, 1),
            'dance': (self.a_dance, 0),
            'back': (self.a_back, 1),
            'define': (self.a_define, 1),
            'sentence': (self.a_sentence, 0),
    
            'add': (self.a_add, 1),
            'list': (self.a_list, 0),
            'load': (self.a_load, 1),
            'skipto': (self.a_skipto, 1)
        }
        if name:
            library = "library_%s" % name
        else:
            library = "library" % name
        self.__bok_reader = BokReader(library=library)

    def act(self, action, message_words):
        # return a list of strings to be PRIVMSGified as a response
        if action in self.__actions:
            fn, n = self.__actions[action]
            if len(message_words) >= n:
                return fn(message_words)

    def a_lol(self, message_words):
        return ["haha"]

    def a_dance(self, message_words):
        d = random.choice(self.__dances)
        return ["\x01ACTION %s\x01" % d]

    def a_next(self, message_words):
        # read out the next n sentences
        # have åtgärder for going out of range etc.
        # reformat for IRC PMs
        n = message_words[0]
        if n.isdigit():
            n = int(n)
            pass
        else:
            return
        return [str(n)]

    def a_back(self, message_words):
        # go back n sentences
        n = message_words[0]
        if n.isdigit():
            n = int(n)
            pass
        else:
            return
        return ["Implement this command! (:"]

    def a_define(self, message_words):
        # look up a word on wiktionary
        word = message_words[0]
        content = self.__parser.fetch(word)
        if not content:
            return ["no definition found :o"]
        else:
            strings = []
            r = re.compile("( [\.a-z]+)[\dA-Z]")
            for c in content:
                string = ""
                counter = 1
                definitions = c["definitions"]
                for d in definitions:
                    speech = d["partOfSpeech"]
                    texts = d["text"].split("\n")
                    word = texts[0]
                    definition = texts[1]
                    # remove any quotes from the definition, determined
                    # by beginning a sentence straight after a previous one;
                    # will probably find false positives but whatevs
                    quote = r.search(definition)
                    if quote:
                        match = quote.group(0)
                        last_word = quote.group(1)
                        definition = definition.split(match)[0] + last_word
                    string = string + "%d. %s: %s " % (
                        counter, speech, definition
                    )
                    counter += 1
                strings.append(string)

        return strings


    def a_sentence(self, message_words):
        return self.bok_reader.sentence_status()
        # report which sentence the reader is up to
#        return "You are on sentence %d of %d." % (
#            self.__sentence, self.__sentence_total
#        )

    def a_add(self, message_words):
        #self.bok_reader.add_book_url(self, url, title="Unknown", author="Unknown"):
        #self.__bok_adder.add_book_url(url, title, author)
        return ["Implement this command! (:"]

    def a_list(self, message_words):
        return self.__bok_reader.list_books()

    def a_load(self, message_words):
        book = message_words[0]
        # load a book from the list
        # also change the topic to say what's being read
        #:kim!kim@Clk-91B7221E.cust.bredband2.com TOPIC #bokbot :asdf
        return ["Implement this command! (:"]

    def a_skipto(self, message_words):
        return ["Implement this command! (:"]
