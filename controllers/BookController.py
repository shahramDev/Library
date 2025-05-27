from models.Book import Book

from core.ErrorHandling import (
    BookNotFoundError,
    BookAlreadyExistsError
)

class BookController:

    def __init__(self, book: Book):
        self.book = book

    @classmethod
    def getBook(cls, bookId):
        book = Book.getBook(bookId)
        if book.book is None:
            raise BookNotFoundError("📕 Book not found.")
        return cls(book)

    @classmethod
    def addBook(cls, bookId, bookInfo):
        book = Book.addBook(bookId, bookInfo)
        if book is None:
            raise BookAlreadyExistsError("📕 Book with this ID already exists.")
        return cls(book)

    def updateTitle(self, title):
        self.book.title = title
        self.book.updateBook()

    def updateAuthor(self, author):
        self.book.author = author
        self.book.updateBook()

    def updatePublisher(self, publisher):
        self.book.publisher = publisher
        self.book.updateBook()

    def updatePublishYear(self, year):
        self.book.publishYear = year
        self.book.updateBook()

    def updateAbstract(self, abstract):
        self.book.abstract = abstract
        self.book.updateBook()

    def updatePages(self, pages):
        self.book.pages = pages
        self.book.updateBook()

    def updateLanguage(self, language):
        self.book.language = language
        self.book.updateBook()

    def updateContentType(self, contentType):
        self.book.contentType = contentType
        self.book.updateBook()

    def updateUsageType(self, usageType):
        self.book.usageType = usageType
        self.book.updateBook()

    def updateGenres(self, genres):
        self.book.genres = genres
        self.book.updateBook()

    def updateAvailableCopies(self, count):
        self.book.availableCopies = count
        self.book.updateBook()

    def updateTotalCopies(self, count):
        self.book.totalCopies = count
        self.book.updateBook()


    def getDetails(self):
        return {
            "bookId": self.book.bookId,
            "title": self.book.title,
            "author": self.book.author,
            "publisher": self.book.publisher,
            "publishYear": self.book.publishYear,
            "abstract": self.book.abstract,
            "pages": self.book.pages,
            "language": self.book.language,
            "contentType": self.book.contentType,
            "usageType": self.book.usageType,
            "genres": self.book.genres,
            "availableCopies": self.book.availableCopies,
            "totalCopies": self.book.totalCopies
        }

    @classmethod
    def deleteBook(cls, bookId):
        success = Book.deleteBook(bookId)
        if not success:
            raise BookNotFoundError("❌ Could not delete book. Book ID not found.")
