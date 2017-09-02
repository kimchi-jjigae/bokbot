# -*- coding: utf-8 -*-i
from pymongo import MongoClient
from bokadder import BokAdder
from bson.objectid import ObjectId

class BokReader:
    """Class which reads boks from a MongoDB database."""
    def __init__(self, db_name="book_db", collection_name="library"):
        self.__sentence = 0
        self.__sentence_total = 0
        self.__books = []
        self.__current_book = {}
        _client = MongoClient()
        _db = _client[db_name] # the database to be written to and read from
        self.__library = _db[collection_name] # the collection within the database
        self.__bok_adder = BokAdder()
        print("Connecting to database %s and reading from %s" % (_db, collection_name))

    def load_book(self, book_id):
        book_strings = []
        try:
            id_ = ObjectId(book_id)
        except TypeError:
            book_strings.append("Book not found.")

        book = self.__library.find_one({'_id': id_})
        if book is not None:
            # load a book and return its title and which sentence up to
            self.__current_book = book
            book_strings.append("Now loaded book: ")
            book_strings.append("[%s] \"%s\" by %s" % (book['_id'], book['title'], book['author']))
            book_strings.append("You are on sentence %d of %d." % (
                self.__sentence, self.__sentence_total
            ))
        else:
            book_strings.append("Book not found.")

        return book_strings

    def list_books(self):
        books = self.__library.find()
        count = books.count()
        book_strings = []
        if count == 0:
            book_strings.append("There are no books in the library." % count)
        else:
            if count == 1:
                book_strings.append("There is 1 book:")
            else:
                book_strings.append("There are %d books:" % count)

            for book in books:
                book_strings.append("[%s] \"%s\" by %s" % (book['_id'], book['title'], book['author']))

        return book_strings

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
        return ["You are on sentence %d of %d." % (
        #return "You are on sentence %d of %d of %s." % (
            self.__sentence, self.__sentence_total
            #self.__sentence, self.__sentence_total, self.__current_book['title']
        )]

    def add_book_url(self, url, title="Unknown", author="Unknown"):
        #.add this.url/book.txt adds a book to its database
        #self.__bok_adder.add_book_url(url, title, author)
        pass
