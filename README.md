# bokbot
Very simple IRC bot which acts as a text-only e-book reader.

Planned feature list:

CORE
+ divides a book (text-only format?) into manageable pieces, sentences, and split them to not exceed the IRC message character limit.
+ points to a particular sentence.
+ ` `
    next sentence
+ `5`
    next 5 sentences
+ `.back 10`
    goes back 10 sentences
+ `.define word`
    defines a word
+ `.sentence`
    reports which sentence it is up to and the total amount of sentences in the book

EXTRA
+ only responds to kim.
+ `.add this.url/book.txt`
    adds a book to its database
+ `.list`
    lists books available
+ `.load book`
    loads a particular book
+ `.skipto 408`
    skips to a particular sentence number
