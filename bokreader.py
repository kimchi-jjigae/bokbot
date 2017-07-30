# -*- coding: utf-8 -*-i

class BokReader:
    """Class which reads boks from a MongoDB database."""
    def __init__(self):
        __sentence = 0
        __sentence_total = 0
        __books = []
        __currentBook = {}

    def load_book(self, book):
        # return some dict, maybe
        # load a book and return its title and which sentence up to
        pass

    def list_books(self):
        # list books available and which sentence up to
        pass

    def next_sentence(self):
        pass

    def back_up(self, n):
        # have åtgärder for going out of range etc.
        pass

    def skip_to(self, n):
        # have åtgärder for going out of range etc.
        pass

    def sentence_status(self):
        # reports which sentence it is up to and the total amount of sentences in the book
        return "You are on sentence %d of %d." % (
            self.__sentence, self.__sentence_total
        )

    def add_book(self, url):
        #.add this.url/book.txt adds a book to its database
        pass
