# -*- coding: utf-8 -*-i
from pymongo import MongoClient
from bson.objectid import ObjectId

class BokReader:
    """Class which reads boks from a MongoDB database."""
    def __init__(self):
        __sentence = 0
        __sentence_total = 0
        __books = []
        __currentBook = {}
        _client = MongoClient()
        _db = _client.book_db # the database to be written to and read from
        __library = _db.library # the collection within the database

    def load_book(self, book_id):
        book = __library.find_one({'book_id': ObjectId(book_id))
        if book not None:
            print(book)
        else:
            print("Book not found.")
        # return some dict, maybe
        # load a book and return its title and which sentence up to
        pass

    def list_books(self):
        books = __library.find()
        count = books.count()
        print("there are %d books" % count)
        print(books)
        # list books available and which sentence up to

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
