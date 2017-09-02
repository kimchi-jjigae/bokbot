# -*- coding: utf-8 -*-i
from pymongo import MongoClient
from booksplitter import BookSplitter
from bson.objectid import ObjectId
#import urllib

class BokAdder:
    """Class which takes JSON-books and adds them to a MongoDB database."""
    def __init__(self, db_name="book_db", collection_name="library"):
        _client = MongoClient()
        _db = _client[db_name] # the database to be written to and read from
        self.__library = _db[collection_name] # the collection within the database
        self.__bs = BookSplitter()

    def clear_library(self):
        self.__library.remove({}) # clear all books omg 

    def add_book(self, text_file, title="Unknown", author="Unknown"):
        json_book = self.__bs.split_book(text_file, title, author)
        id_ = self.__library.insert_one(json_book).inserted_id
        print("Added the book with id %s" % id_)

    def add_book_url(self, url):
        #.add this.url/book.txt adds a book to its database
        #txt = urllib.urlopen(target_url).read()
        pass
