import os
import json
from filelock import FileLock

class Book:

    database = 'database/books.json'
    lockFile = database + '.lock'

    def __init__(self, bookId, bookData=None):
        self.bookId = bookId
        self.book = bookData

    @classmethod
    def loadBooks(cls):
        if not os.path.exists(cls.database):
            with open(cls.database, 'w') as database:
                json.dump({}, database, indent=4)
        lock = FileLock(cls.lockFile)
        with lock:
            with open(cls.database, 'r') as database:
                return json.load(database)

    
    def saveBooks(self, books):
        lock = FileLock(self.lockFile)
        with lock:
            with open(self.database, 'w') as database:
                json.dump(books, database, indent=4)

    @classmethod
    def getBook(cls, bookId):
        books = cls.loadBooks()
        book = books.get(bookId)
        return cls(bookId, book)

    @classmethod
    def addBook(cls, bookId, bookInfo):
        books = cls.loadBooks()
        if bookId in books:
            return None
        data = {
            "title":bookInfo[0],
            "author":bookInfo[1],
            "publisher":bookInfo[2],
            "publishYear":bookInfo[3],
            "abstract":bookInfo[4],
            "pages":bookInfo[5],
            "language":bookInfo[6],
            "contentType": bookInfo[7],
            "usageType": bookInfo[8],
            "genres":bookInfo[9],
            "availableCopies":bookInfo[10],
            "totalCopies":bookInfo[11]
        }
        books[bookId] = data
        book = cls(bookId,data)
        book.saveBooks(books)
        return book

    def updateBook(self):
        books = Book.loadBooks()
        books[self.bookId] = self.book
        self.saveBooks(books)

    @classmethod
    def deleteBook(cls, bookId):
        books = cls.loadBooks()
        if bookId in books:
            books[bookId] = {}
            cls.saveBooks(books)
            return True
        return False

    @property
    def title(self):
        return self.book["title"]

    @title.setter
    def title(self, value):
        self.book["title"] = value


    @property
    def author(self):
        return self.book["author"]

    @author.setter
    def author(self, value):
        self.book["author"] = value

    @property
    def publisher(self):
        return self.book["publisher"]

    @publisher.setter
    def publisher(self, value):
        self.book["publisher"] = value

    @property
    def publishYear(self):
        return self.book["publishYear"]

    @publishYear.setter
    def publishYear(self, value):
        self.book["publishYear"] = value

    @property
    def abstract(self):
        return self.book["abstract"]

    @abstract.setter
    def abstract(self, value):
        self.book["abstract"] = value

    @property
    def pages(self):
        return self.book["pages"]

    @pages.setter
    def pages(self, value):
        self.book["pages"] = value

    @property
    def language(self):
        return self.book["language"]

    @language.setter
    def language(self, value):
        self.book["language"] = value

    @property
    def contentType(self):
        return self.book["contentType"]

    @contentType.setter
    def contentType(self, value):
        self.book["contentType"] = value

    @property
    def usageType(self):
        return self.book["usageType"]

    @usageType.setter
    def usageType(self, value):
        self.book["usageType"] = value

    @property
    def genres(self):
        return self.book["genres"]

    @genres.setter
    def genres(self, value):
        self.book["genres"] = value

    @property
    def availableCopies(self):
        return self.book["availableCopies"]

    @availableCopies.setter
    def availableCopies(self, value):
        self.book["availableCopies"] = value

    @property
    def totalCopies(self):
        return self.book["totalCopies"]

    @totalCopies.setter
    def totalCopies(self, value):
        self.book["totalCopies"] = value