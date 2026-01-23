from datetime import datetime
import json
from book import Book
from person import Admin, Librarian, Student


class Library:
    def __init__(self):
        self._books = []
        self._issuedBooks = []
        self._users = []

    @property
    def books(self):
        return self._books

    @property
    def issuedBooks(self):
        return self._issuedBooks

    @property
    def users(self):
        return self._users

    # User Management Methods

    def login(self, user_id, password):
        for user in self._users:
            if user.user_id == user_id and user.password == password:
                print(f"✅ Login Successful! Welcome, {user.name} ({user.get_role()})")
                return user
        print("❌ Invalid User ID or Password")
        return None
    
    def change_password(self, user_id, old_password, new_password):
        for user in self._users:
            if user.user_id == user_id:
                if user.password == old_password:
                    user.password = new_password
                    self.save_users_data()
                    print("✅ Password changed successfully!")
                    return
                else:
                    print("❌ Error: Old password is incorrect!")
                    return
        print("❌ Error: User not found!")
        return
    
    def change_username(self, user_id, new_user_id):
        for user in self._users:
            if user.user_id == user_id:
                user.user_id = new_user_id
                self.save_users_data()
                print("✅ Username changed successfully!")
                return
        print("❌ Error: User not found!")
        return
    
    def add_admin(self, name, user_id, password, admin_id):
        for user in self._users:
            if user.user_id == user_id:
                print("❌ Error: Admin with this User ID already exists!")
                return
        new_admin = Admin(name, user_id, password, admin_id)
        self._users.append(new_admin)
        self.save_users_data()
        print(f"Admin {name} Added Successfully!")

    def add_librarian(self, name, user_id, password, employee_id):
        for user in self._users:
            if user.user_id == user_id:
                print("❌ Error: Librarian with this User ID already exists!")
                return
        new_librarian = Librarian(name, user_id, password, employee_id)
        self._users.append(new_librarian)
        self.save_users_data()
        print(f"Librarian {name} Added Successfully!")

    def add_student(self, name, user_id, password, student_id):
        for user in self._users:
            if user.user_id == user_id:
                print("❌ Error: Student with this User ID already exists!")
                return
        new_student = Student(name, user_id, password, student_id)
        self._users.append(new_student)
        self.save_users_data()
        print(f"Student {name} Added Successfully!")

    def view_all_users(self):
        if not self._users:
            print("📭 No users found in the system.")
            return
        
        print("\n" + "=" * 60)
        print("👥 ALL USERS IN THE SYSTEM")
        print("=" * 60)
        
        admins = [u for u in self._users if u.get_role() == "Admin"]
        librarians = [u for u in self._users if u.get_role() == "Librarian"]
        students = [u for u in self._users if u.get_role() == "Student"]
        
        if admins:
            print("\n👑 ADMINS:")
            print("-" * 60)
            for admin in admins:
                print(f"  Name: {admin.name} | User ID: {admin.user_id} | Admin ID: {admin.admin_id}")
        
        if librarians:
            print("\n👨‍💼 LIBRARIANS:")
            print("-" * 60)
            for lib in librarians:
                print(f"  Name: {lib.name} | User ID: {lib.user_id} | Employee ID: {lib.employee_id}")
        
        if students:
            print("\n📚 STUDENTS:")
            print("-" * 60)
            for student in students:
                print(f"  Name: {student.name} | User ID: {student.user_id} | Roll No: {student.rollnumber}")
        
        print("=" * 60)
        print(f"Total Users: {len(self._users)} (Admins: {len(admins)}, Librarians: {len(librarians)}, Students: {len(students)})")
        print("=" * 60)

    # Book Management Methods

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

    def issue_book(self, rollNo, isbn):
        # Check if student exists
        student = None
        for user in self._users:
            if user.get_role() == "Student" and user.rollnumber == rollNo:
                student = user
                break
        
        if student is None:
            print(f"❌ Error: Student with Roll Number {rollNo} does not exist!")
            print("Please add the student first before issuing a book.")
            return False
        
        # Check if book exists and is available
        for book in self.books:
            if isbn == book.isbn:
                if book.quantity > 0:
                    book.quantity -= 1
                    timeStamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # Store only foreign keys (like database foreign keys)
                    issue_entry = {
                        "timeStamp": timeStamp,
                        "rollNo": rollNo,    # Foreign key to student
                        "isbn": book.isbn,   # Foreign key to book
                    }
                    self._issuedBooks.append(issue_entry)
                    print(
                        f"📖 Book Issued to {student.name} ({rollNo}) Successfully! Remaining: {book.quantity}"
                    )
                    return True
                else:
                    print("🚫 Sorry, this book is currently out of stock!")
                    return False
        print("❌ No Book Found Matched To ISBN Number")
        return False

    def check_issue_books(self):
        if not self._issuedBooks:
            print("📭 No books have been issued yet.")
            return

        print("\n--- All Issued Books History ---")
        for entry in self._issuedBooks:
            # Lookup student and book using foreign keys
            student_name = "Unknown Student"
            for user in self._users:
                if user.get_role() == "Student" and user.rollnumber == entry["rollNo"]:
                    student_name = user.name
                    break
            
            book_title = "Unknown Book"
            for book in self._books:
                if book.isbn == entry["isbn"]:
                    book_title = book.title
                    break
            
            print(
                f"{entry['timeStamp']} - {book_title} (ISBN: {entry['isbn']}) issued to {student_name} (Roll No: {entry['rollNo']})"
            )

    def check_issue_books_finder(self, rollnumber):
        found = False
        for entry in self.issuedBooks:
            if entry["rollNo"] == rollnumber:
                if not found:
                    print(f"\n--- Search Results for Roll Number: {rollnumber} ---")
                    found = True
                
                # Lookup student and book using foreign keys
                student_name = "Unknown Student"
                for user in self._users:
                    if user.get_role() == "Student" and user.rollnumber == rollnumber:
                        student_name = user.name
                        break
                
                book_title = "Unknown Book"
                for book in self._books:
                    if book.isbn == entry["isbn"]:
                        book_title = book.title
                        break
                
                print(
                    f"🕒 {entry['timeStamp']} | Book: {book_title} (ISBN: {entry['isbn']}) | Student: {student_name} (Roll No: {rollnumber})"
                )
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

    # Data Management Methods

    def save_data(self, filename="library_data.json"):
        data = {
            "Books": [book.to_dict() for book in self.books],
            "issuedBooks": self.issuedBooks,
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"💾 Data saved successfully to {filename}")

    def save_users_data(self, filename="users_data.json"):
        data = {
            "Users": [user.to_dict() for user in self.users],
        }
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

        print(f"💾 Users data saved successfully to {filename}")

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

    def load_users_data(self, filename="users_data.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self._users = []
                users_data = data.get("Users", [])
                for user_data in users_data:
                    if user_data["role"] == "Admin":
                        user = Admin(
                            user_data["name"],
                            user_data["user_id"],
                            user_data["password"],
                            user_data["admin_id"],
                        )
                    elif user_data["role"] == "Librarian":
                        user = Librarian(
                            user_data["name"],
                            user_data["user_id"],
                            user_data["password"],
                            user_data["employee_id"],
                        )
                    elif user_data["role"] == "Student":
                        user = Student(
                            user_data["name"],
                            user_data["user_id"],
                            user_data["password"],
                            user_data["rollnumber"],
                        )
                    self._users.append(user)
                print(f"📂 Users data loaded successfully from {filename}.")
        except FileNotFoundError:
            print("📝 No previous users data found. Starting with no users.")
            # by default only 1 admin user
            default_admin = Admin("Default Admin", "admin", "admin123", 1)
            self._users.append(default_admin)
        except Exception as e:
            print("Unknown Error Occured Please Contact Support", e)
