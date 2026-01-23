class Book:
    def __init__(self, title, author, isbn, quantity, shelfNumber):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.shelfNumber = shelfNumber

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.isbn}, Quantity: {self.quantity}, Shelf Number: {self.shelfNumber}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "quantity": self.quantity,
            "shelfNumber": self.shelfNumber,
        }
