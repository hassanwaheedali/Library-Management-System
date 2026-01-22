from datetime import datetime
import json
from book import Book


class Library:
    def __init__(self):
        self._books = []
        self._issuedBooks = []

    @property
    def books(self):
        return self._books

    @property
    def issuedBooks(self):
        return self._issuedBooks

    def add_books(self, title, author, isbn, quantity, shelfNumber):
        new_books = Book(title, author, isbn, quantity, shelfNumber)
        self._books.append(new_books)
        print("Book Added Successfully!")

    def remove_books(self, isbn):
        for book in self.books:
            if isbn == book.isbn:
                self.books.remove(book)
                print("Book Removed Successfully!")
                return
        print("❌ No Book Found Matched To ISBN Number")

    def display_books(self):
        if not self.books:
            print("📭 The library is empty.")
            return

        print("\n--- Current Library Collection ---")
        for book in self.books:
            print(book)
            print(type(book))

    def search_books(self, value):
        print("Searching....")
        found = False
        for book in self.books:
            if (
                value.lower() in book.title.lower()
                or value.lower() in book.author.lower()
                or value == book.isbn
            ):
                print(book)
                found = True
        if not found:
            print("❌ No Books Found Matched To Search Value")

    def find_shelf_books(self, shelfNumber):
        found = False
        print("Searching....")
        print(f"\n--- Books in Shelf Number: {shelfNumber} ---")
        for book in self.books:
            if shelfNumber == book.shelfNumber:
                print(book)
                found = True
        if not found:
            print("❌ No Books Found in Shelf Number")

    def issue_book(self, user, rollNo, isbn):
        for book in self.books:
            if isbn == book.isbn:
                if book.quantity > 0:
                    book.quantity -= 1
                    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    issue_entry = {
                        "timeStamp": timeStamp,
                        "user": user,
                        "rollNo": rollNo,
                        "title": book.title,
                        "isbn": book.isbn,
                    }
                    self.issuedBooks.append(issue_entry)
                    print(
                        f"📖 Book Issued to {user} {rollNo} Successfully! Remaining: {book.quantity}"
                    )
                    return
                else:
                    print("🚫 Sorry, this book is currently out of stock!")
                    return
        print("❌ No Book Found Matched To ISBN Number")

    def check_issue_books(self):
        if not self._issuedBooks:
            print("📭 No books have been issued yet.")
            return

        print("\n--- All Issued Books History ---")
        for entry in self._issuedBooks:
            print(
                f"{entry['timeStamp']} - {entry['title']} {entry['isbn']} issued to {entry['user']} ({entry['rollNo']})"
            )

    def check_issue_books_finder(self, rollnumber):
        found = False
        for entry in self.issuedBooks:
            if entry["rollNo"] == rollnumber:
                print(f"\n--- Search Results for Roll Number: {rollnumber} ---")
                print(
                    f"🕒 {entry['timeStamp']} | Book: {entry['title']} (ISBN: {entry['isbn']}) | Student: {entry['user']} | ({entry['rollNo']})"
                )
                found = True
        if not found:
            print(f"⚠️ No records found for Roll Number: {rollnumber}")

    def return_book(self, rollNo, isbn):
        for book in self.books:
            if book.isbn == isbn:
                book.quantity += 1
                for issueBook in self.issuedBooks:
                    if issueBook["rollNo"] == rollNo:
                        self.issuedBooks.remove(issueBook)
                        print(
                            f"✅ Book with ISBN {isbn} returned successfully by {rollNo}."
                        )
                        return
        print("❌ No Book Found Matched To ISBN Number")
        return
