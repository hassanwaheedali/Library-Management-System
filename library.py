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
        if quantity < 0:
            print("❌ Error: Quantity cannot be negative!")
            return
        if shelfNumber < 0:
            print("❌ Error: Shelf Number cannot be negative!")
            return
        if any(book.isbn == isbn for book in self.books):
            print("❌ Error: A book with this ISBN already exists!")
            return
        new_books = Book(title, author, isbn, quantity, shelfNumber)
        self._books.append(new_books)
        print("Book Added Successfully!")

    def update_book(self, isbn, choice):
        for book in self.books:
            if isbn == book.isbn:
                user_choice = choice.lower()
                if user_choice == "title":
                    new_title = input("Please Write Title: ")
                    book.title = new_title
                elif user_choice == "author":
                    new_author = input("Please Write Author: ")
                    book.author = new_author
                elif user_choice == "isbn":
                    try:
                        new_isbn = int(input("Please Write ISBN Number: "))
                        if any(b.isbn == new_isbn and b != book for b in self.books):
                            print("❌ Error: A book with this ISBN already exists!")
                            return
                        book.isbn = new_isbn
                    except ValueError:
                        print("❌ Error: ISBN must be a number!")
                        return
                elif user_choice == "quantity":
                    try:
                        new_quantity = int(input("Please Write Quantity: "))
                        if new_quantity < 0:
                            print("❌ Error: Quantity cannot be negative!")
                            return
                        book.quantity = new_quantity
                    except ValueError:
                        print("❌ Error: Quantity must be a number!")
                        return
                elif user_choice == "shelfnumber":
                    try:
                        new_shelfNumber = int(
                            input("Please Write Shelf Number without Dashes: ")
                        )
                        if new_shelfNumber < 0:
                            print("❌ Error: Shelf Number cannot be negative!")
                            return
                        book.shelfNumber = new_shelfNumber
                    except ValueError:
                        print("❌ Error: Shelf Number must be a number!")
                        return
                else:
                    print("❌ Invalid Update Choice!")
                    return
                print("Book Updated Successfully!")
                return
        print("❌ No Book Found Matched To ISBN Number")

    def remove_books(self, isbn):
        for book in self.books:
            if isbn == book.isbn:
                self._books.remove(book)
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

    def search_books(self, value):
        print("Searching....")
        found = False
        isbn_value = None
        try:
            isbn_value = int(value)
        except ValueError:
            pass 
        
        for book in self.books:
            if (
                value.lower() in book.title.lower()
                or value.lower() in book.author.lower()
                or (isbn_value is not None and isbn_value == book.isbn)
            ):
                print(book)
                found = True
        if not found:
            print("❌ No Books Found Matched To Search Value")

    def find_shelf_books(self, shelfNumber):
        found = False
        print("Searching....")
        # Convert shelfNumber to int if it's a string
        try:
            shelf_num = int(shelfNumber)
        except (ValueError, TypeError):
            print("❌ Error: Shelf Number must be a valid number!")
            return
            
        print(f"\n--- Books in Shelf Number: {shelf_num} ---")
        for book in self.books:
            if shelf_num == book.shelfNumber:
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
                    self._issuedBooks.append(issue_entry)
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
                for issueBook in self._issuedBooks:
                    if issueBook["rollNo"] == rollNo and issueBook["isbn"] == isbn:
                        self._issuedBooks.remove(issueBook)
                        book.quantity += 1
                        print(
                            f"✅ Book with ISBN {isbn} returned successfully by {rollNo}."
                        )
                        return
                print(
                    f"❌ No issued record found for Roll Number {rollNo} with ISBN {isbn}"
                )
                return
        print("❌ No Book Found Matched To ISBN Number")
        return

    def save_data(self, filename="library_data.json"):
        data = {
            "Books": [book.to_dict() for book in self.books],
            "issuedBooks": self.issuedBooks,
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"💾 Data saved successfully to {filename}")

    def load_data(self, filename="library_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self._books = []
                for b in data.get("Books", []):
                    book = Book(
                        b["title"],
                        b["author"],
                        int(b["isbn"]),
                        b["quantity"],
                        b["shelfNumber"],
                    )
                    self._books.append(book)

                issued_books_data = data.get("issuedBooks", [])
                self._issuedBooks = []
                for entry in issued_books_data:
                    entry_copy = entry.copy()
                    entry_copy["isbn"] = int(entry_copy["isbn"])
                    self._issuedBooks.append(entry_copy)

                print(f"📂 Data loaded successfully from {filename}.")
        except FileNotFoundError:
            print("📝 No previous data found. Starting with an empty library.")
        except Exception as e:
            print("Unknown Error Occured Please Contact Support", e)
