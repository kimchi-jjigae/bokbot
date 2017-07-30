# -*- coding: utf-8 -*-i
import re

class BookSplitter:
    """Takes a book in the form of a .txt file and splits it up into a more
    easily parsable JSON format (bok), which may be inserted into a MongoDB
    bok database.
    """
    def __init__(self): 
        pass

    def split_book(self, text_file, title="Unknown", author="Unknown"):
        # possibly do some kind of preprocessing on the book first
        # (remove empty lines? they might be nice as paragraph breaks)
        counter = 0
        extra = []
        book_content = {}
        with open(text_file) as tf:
            sentence_list = []
            for text_line in tf:
                # split line roughly into sentences, keep delimiter
                rough = re.split('([\.\?\!])', text_line)
                # remove all blank "sentences"
                rough = list(filter(lambda s: s != '', sentences))
                sentences = []
                # look at every sentence
                for i in range(0, len(rough), 2):
                    # and re-add the delimiter to it
                    if i == len(rough) - 1:
                        # if odd list and last element, then no delimiter
                        new_sentence = rough[i]
                    else:
                        new_sentence = rough[i] + rough[i+1]
                    sentences.append(new_sentence)

                # done with that line, so add to the sentences to the
                # sentence list
                sentence_list += sentences
                # if the sentence list is full, then add it to the book
                # content
                if len(sentence_list) >= 1000:
                    diff = len(sentence_list) - 1000
                    extra = sentence_list[-diff]
                    key = str(counter).zfill(5)
                    book_content[key] = sentence_list[:]
                    sentence_list = extra
                    extra = []
                    counter += 1

            # add the remaining sentences to the book if the sentence
            # list is not empty
            if len(sentence_list) > 0:
                key = str(counter).zfill(5)
                book_content[key] = sentence_list[:]

        metadata = "Created in pre-alpha phase %s" % datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

        return {
            'title': title,
            'author': author,
            'content': book_content,
            'metadata': metadata,
        }

#result = posts.insert_one(post_data)
#print('One post: {0}'.format(result.inserted_id))
