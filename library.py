from datetime import datetime

from database import get_db_connection
from models import Admin, Book, Librarian, Student, User


class Library:
    conn = get_db_connection()
    cursor = conn.cursor()

    def __init__(self):
        self._ensure_default_admin()

    def _ensure_default_admin(self):
        try:
            query = "SELECT COUNT(*) AS total FROM users"
            self.cursor.execute(query)
            total_users = self.cursor.fetchone()["total"]
            if total_users == 0:
                created = self.add_admin("Admin", "admin", "admin")
                if created:
                    print("⚠️ No users found. A default admin user has been created.")
        except Exception as e:
            print(f"❌ Error: Could not ensure default admin! {e}")
            return

    # User Management Methods
    def login(self, username, password):
        try:
            query = "SELECT * FROM vw_user_profiles WHERE username = %s"
            self.cursor.execute(query, (username,))
            user_data = self.cursor.fetchone()
            if user_data:
                base_data = {
                    "id": user_data["id"],
                    "username": user_data["username"],
                    "password": user_data["password"],
                    "name": user_data["name"],
                    "created_at": user_data.get("created_at"),
                    "updated_at": user_data.get("updated_at"),
                }
                if not User(**base_data).check_password(password):
                    print("❌ Invalid Username or Password")
                    return None
                if user_data.get("admin_id") is not None:
                    user = Admin(**{**base_data, "admin_id": user_data["admin_id"]})
                elif user_data.get("employee_id") is not None:
                    user = Librarian(
                        **{**base_data, "employee_id": user_data["employee_id"]}
                    )
                elif user_data.get("rollnumber") is not None:
                    user = Student(
                        **{**base_data, "rollnumber": user_data["rollnumber"]}
                    )
                else:
                    user = User(**base_data)
                print(f"✅ Login Successful! Welcome, {user.name} ({user.role})")
                return user
            print("❌ Invalid Username or Password")
            return None
        except Exception:
            print("❌ Error: Could not login!")
            return None

    def change_password(self, username, old_password, new_password):
        try:
            query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            user_data = self.cursor.fetchone()
            if user_data:
                user = User(**user_data)
                if user.check_password(old_password):
                    query = "UPDATE users SET password = %s WHERE username = %s"
                    self.cursor.execute(
                        query, (user.hash_password(new_password), username)
                    )
                    self.conn.commit()
                    print("✅ Password changed successfully!")
                    return True
                print("❌ Invalid Username or Password")
                return False
            print("❌ Invalid Username or Password")
            return False
        except Exception:
            self.conn.rollback()
            print("❌ Error: Could not change password!")
            return False

    def change_username(self, old_username, new_username):
        try:
            query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(query, (old_username,))
            user_data = self.cursor.fetchone()
            if user_data:
                query = "UPDATE users SET username = %s WHERE username = %s"
                self.cursor.execute(query, (new_username, old_username))
                self.conn.commit()
                print("✅ Username changed successfully!")
                return True
            print("❌ Invalid Username")
            return False
        except Exception:
            self.conn.rollback()
            print("❌ Error: Could not change username!")
            return False

    def add_admin(self, name, username, password):
        try:
            # 1. Check if user already exists
            query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            if self.cursor.fetchone():
                print("❌ Error: Admin with this username already exists!")
                return False

            # 2. Insert into Parent table (users) and grab the new ID!
            query_user = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s) RETURNING id"
            self.cursor.execute(
                query_user, (name, username, User.hash_password(password))
            )

            new_user_id = self.cursor.fetchone()["id"]

            # 3. Insert into Child table (admins) using that ID
            query_admin = "INSERT INTO admins (user_id) VALUES (%s)"
            self.cursor.execute(query_admin, (new_user_id,))

            self.conn.commit()
            print(f"✅ Admin {name} Added Successfully!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not add admin! {e}")
            return False

    def add_librarian(self, name, username, password, employee_id):
        try:
            query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            if self.cursor.fetchone():
                print("❌ Error: Librarian with this username already exists!")
                return False

            query_user = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s) RETURNING id"
            self.cursor.execute(
                query_user, (name, username, User.hash_password(password))
            )
            new_user_id = self.cursor.fetchone()["id"]

            query_librarian = (
                "INSERT INTO librarians (user_id, employee_id) VALUES (%s, %s)"
            )
            self.cursor.execute(query_librarian, (new_user_id, employee_id))

            self.conn.commit()
            print(f"✅ Librarian {name} Added Successfully!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not add librarian! {e}")
            return False

    def add_student(self, name, username, password, rollnumber):
        try:
            query = "SELECT * FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            if self.cursor.fetchone():
                print("❌ Error: Student with this username already exists!")
                return False

            query_user = "INSERT INTO users (name, username, password) VALUES (%s, %s, %s) RETURNING id"
            self.cursor.execute(
                query_user, (name, username, User.hash_password(password))
            )

            new_student_id = self.cursor.fetchone()["id"]
            query_student = "INSERT INTO students (user_id, rollnumber) VALUES (%s, %s)"
            self.cursor.execute(query_student, (new_student_id, rollnumber))

            self.conn.commit()
            print(f"✅ Student {name} Added Successfully!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not add student! {e}")
            return False

    def view_all_users(self):
        try:
            print("\n" + "=" * 60)
            print("👥 ALL USERS IN THE SYSTEM")
            print("=" * 60)
            admins_query = (
                "SELECT * FROM users u INNER JOIN admins a ON a.user_id = u.id;"
            )
            self.cursor.execute(admins_query)
            admins_data = self.cursor.fetchall()
            admins = [Admin(**admin) for admin in admins_data]

            librarians_query = (
                "SELECT * FROM users u INNER JOIN librarians l ON l.user_id = u.id;"
            )
            self.cursor.execute(librarians_query)
            librarians_data = self.cursor.fetchall()
            librarians = [Librarian(**librarian) for librarian in librarians_data]

            students_query = (
                "SELECT * FROM users u INNER JOIN students s ON s.user_id = u.id;"
            )
            self.cursor.execute(students_query)
            students_data = self.cursor.fetchall()
            students = [Student(**student) for student in students_data]

            if not admins and not librarians and not students:
                print("📭 No users found in the system.")
                return

            print("=" * 60)
            print(
                f"Total Users: {len(admins) + len(librarians) + len(students)} (Admins: {len(admins)}, Librarians: {len(librarians)}, Students: {len(students)})"
            )
            print("=" * 60)
            for admin in admins:
                print(admin)
            for librarian in librarians:
                print(librarian)
            for student in students:
                print(student)
            print("=" * 60)
            return
        except Exception as e:
            print(f"❌ Error: Could not view users! {e}")
            return
        finally:
            print("=" * 60)

    def view_all_students(self):
        try:
            query = "SELECT * FROM users u INNER JOIN students s ON s.user_id = u.id;"
            self.cursor.execute(query)
            students_data = self.cursor.fetchall()
            students = [Student(**student) for student in students_data]
            if not students:
                print("📭 No students found in the system.")
                return
            print("\n" + "=" * 60)
            print("🎓 ALL STUDENTS IN THE SYSTEM")
            print("=" * 60)
            for student in students:
                print(student)
            print("=" * 60)
            return
        except Exception as e:
            print(f"❌ Error: Could not view students! {e}")
            return

    # Book Management Methods

    def add_books(self, title, author, isbn, quantity, shelfNumber):
        try:
            if quantity < 0:
                print("❌ Error: Quantity cannot be negative!")
                return False

            if shelfNumber < 0:
                print("❌ Error: Shelf Number cannot be negative!")
                return False

            isbn_query = "SELECT 1 FROM books WHERE isbn = %s"
            self.cursor.execute(isbn_query, (isbn,))
            if self.cursor.fetchone():
                print("❌ Error: A book with this ISBN already exists!")
                return False

            title_query = "SELECT 1 FROM books WHERE LOWER(title) = LOWER(%s)"
            self.cursor.execute(title_query, (title,))
            if self.cursor.fetchone():
                print("❌ Error: A book with this title already exists!")
                return False

            insert_query = (
                "INSERT INTO books (title, author, isbn, quantity, shelf_number) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            self.cursor.execute(
                insert_query, (title, author, isbn, quantity, shelfNumber)
            )
            self.conn.commit()
            print("✅ Book added successfully!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not add book! {e}")
            return False

    def update_book(self, isbn, choice):
        try:
            query = "SELECT * FROM books WHERE isbn = %s"
            self.cursor.execute(query, (isbn,))
            book_data = self.cursor.fetchone()
            if not book_data:
                print(f"❌ Error: Book with ISBN {isbn} not found!")
                return False
            book = Book(**book_data)
            user_choice = choice.lower()
            if user_choice == "title":
                new_title = input("Please Write Title: ")
                book.title = new_title
                query = "UPDATE books SET title = %s WHERE isbn = %s"
                self.cursor.execute(query, (new_title, isbn))
                self.conn.commit()
                print("✅ Book title updated successfully!")
            elif user_choice == "author":
                new_author = input("Please Write Author: ")
                book.author = new_author
                query = "UPDATE books SET author = %s WHERE isbn = %s"
                self.cursor.execute(query, (new_author, isbn))
                self.conn.commit()
                print("✅ Book author updated successfully!")
            elif user_choice == "isbn":
                new_isbn = int(input("Please Write ISBN Number: "))
                old_isbn = book.isbn
                book.isbn = new_isbn
                query = "UPDATE books SET isbn = %s WHERE isbn = %s"
                self.cursor.execute(query, (new_isbn, old_isbn))
                self.conn.commit()
                print("✅ Book ISBN updated successfully!")
            elif user_choice == "quantity":
                new_quantity = int(input("Please Write Quantity: "))
                book.quantity = new_quantity
                query = "UPDATE books SET quantity = %s WHERE isbn = %s"
                self.cursor.execute(query, (new_quantity, isbn))
                self.conn.commit()
                print("✅ Book quantity updated successfully!")
            elif user_choice in ("shelf_number", "shelfnumber"):
                new_shelf_number = int(input("Please Write Shelf Number: "))
                book.shelf_number = new_shelf_number
                query = "UPDATE books SET shelf_number = %s WHERE isbn = %s"
                self.cursor.execute(query, (new_shelf_number, isbn))
                self.conn.commit()
                print("✅ Book shelf number updated successfully!")
            else:
                print("❌ Error: Invalid choice!")
                return False
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not update book! {e}")
            return False

    def remove_books(self, isbn):
        try:
            book_query = "SELECT * FROM books WHERE isbn = %s"
            self.cursor.execute(book_query, (isbn,))
            book = self.cursor.fetchone()
            if not book:
                print("❌ No Book Found Matched To ISBN Number")
                return False

            check_issued_book = "SELECT * FROM issued_books WHERE book_isbn = %s"
            self.cursor.execute(check_issued_book, (isbn,))
            issued_book = self.cursor.fetchone()
            if issued_book:
                print(
                    "❌ Error: Cannot remove book that is currently issued to students!"
                )
                print("Please wait for all copies to be returned first.")
                return False

            delete_query = "DELETE FROM books WHERE isbn = %s"
            self.cursor.execute(delete_query, (isbn,))
            self.conn.commit()
            print("✅ Book removed successfully!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not remove book! {e}")
            return False

    def display_books(self):
        try:
            query = "SELECT * FROM books"
            self.cursor.execute(query)
            books = self.cursor.fetchall()
            if not books:
                print("📭 The library is empty.")
                return
            print("\n--- Current Library Collection ---")
            for book_data in books:
                # Convert the raw dictionary into your Pydantic Book model!
                book = Book(**book_data)
                print(book)
        except Exception as e:
            print(f"❌ Error: Could not display books! {e}")
            return

    def search_books(self, value):
        print("Searching....")
        try:
            search_query = "SELECT * FROM books WHERE LOWER(title) LIKE %s OR LOWER(author) LIKE %s OR isbn::text = %s"
            self.cursor.execute(
                search_query, (f"%{value.lower()}%", f"%{value.lower()}%", value)
            )
            books = self.cursor.fetchall()
            if not books:
                print("📭 No Books Found Matched To Search Value")
                return
            for book_data in books:
                book = Book(**book_data)
                print(book)
        except Exception as e:
            print(f"❌ Error: Could not search books! {e}")
            return

    def find_shelf_books(self, shelfNumber):
        try:
            query = "SELECT * FROM books WHERE shelf_number = %s"
            self.cursor.execute(query, (shelfNumber,))
            books = self.cursor.fetchall()
            if not books:
                print("📭 No Books Found Matched To Shelf Number")
                return
            print(f"\n--- Books on Shelf Number: {shelfNumber} ---")
            for book_data in books:
                book = Book(**book_data)
                print(book)
        except Exception as e:
            print(f"❌ Error: Could not find books on shelf! {e}")
            return

    def issue_book(self, rollNo, isbn):
        try:
            query_student = "SELECT * FROM users u INNER JOIN students s ON s.user_id = u.id WHERE s.rollnumber = %s"
            self.cursor.execute(query_student, (rollNo,))
            student_data = self.cursor.fetchone()
            if not student_data:
                print(f"❌ Error: Student with Roll Number {rollNo} does not exist!")
                print("Please add the student first before issuing a book.")
                return False
            student = Student(**student_data)
            query_book = "SELECT * FROM books WHERE isbn = %s"
            self.cursor.execute(query_book, (isbn,))
            book_data = self.cursor.fetchone()
            if not book_data:
                print("❌ No Book Found Matched To ISBN Number")
                return False
            book = Book(**book_data)
            if book.quantity <= 0:
                print("🚫 Sorry, this book is currently out of stock!")
                return False
            insert_issue_query = (
                "INSERT INTO issued_books (student_id, book_isbn, issued_at) "
                "VALUES (%s, %s, %s)"
            )
            self.cursor.execute(insert_issue_query, (student.id, isbn, datetime.now()))
            update_book_query = (
                "UPDATE books SET quantity = quantity - 1 WHERE isbn = %s"
            )
            self.cursor.execute(update_book_query, (isbn,))
            self.conn.commit()
            print(f"✅ Book Issued to {student.name} ({rollNo}) Successfully!")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not issue book! {e}")
            return False

    def check_issue_books(self):
        try:
            query = """
            SELECT * FROM 
            vw_issued_books_details
            ORDER BY issued_at DESC
            """
            self.cursor.execute(query)
            issued_books_data = self.cursor.fetchall()

            if not issued_books_data:
                print("📭 No books have been issued yet.")
                return

            print("\n" + "=" * 80)
            print("📚 ISSUED BOOKS HISTORY")
            print("=" * 80)
            for entry in issued_books_data:
                print(
                    f"📖 Book: {entry['book_title']} (ISBN: {entry['book_isbn']}) | "
                    f"Student: {entry['student_name']} (Roll: {entry['rollnumber']}) | "
                    f"Issued: {entry['issued_at']} | "
                    f"Returned: {entry['returned_at']}"
                )
            print("=" * 80)
        except Exception as e:
            print(f"❌ Error: Could not retrieve issued books! {e}")
            return

    def check_issue_books_finder(self, rollnumber):
        try:
            query = """
            SELECT * FROM vw_issued_books_details WHERE rollnumber = %s
            ORDER BY issued_at DESC
            """
            self.cursor.execute(query, (rollnumber,))
            issued_books_data = self.cursor.fetchall()

            if not issued_books_data:
                print(f"📭 No records found for Roll Number: {rollnumber}")
                return

            print(f"\n--- Search Results for Roll Number: {rollnumber} ---")
            for entry in issued_books_data:
                print(
                    f"📖 Book: {entry['book_title']} (ISBN: {entry['book_isbn']}) | "
                    f"Student: {entry['student_name']} (Roll: {entry['rollnumber']}) | "
                    f"Issued: {entry['issued_at']}"
                    f" | Returned: {entry['returned_at']}"
                )
        except Exception as e:
            print(f"❌ Error: Could not search issued books! {e}")
            return

    def return_book(self, rollNo, isbn):
        try:
            # Instead of DELETE, we UPDATE the returned_at timestamp!
            update_issue_query = """
                UPDATE issued_books i
                SET returned_at = NOW()
                FROM students s
                WHERE s.user_id = i.student_id
                AND s.rollnumber = %s
                AND i.book_isbn = %s
                AND i.returned_at IS NULL;
            """
            self.cursor.execute(update_issue_query, (rollNo, isbn))
            if self.cursor.rowcount == 0:
                print(
                    f"❌ No active issued record found for Roll Number {rollNo} with ISBN {isbn}"
                )
                return False

            # Restore the book quantity
            update_book_query = (
                "UPDATE books SET quantity = quantity + 1 WHERE isbn = %s"
            )
            self.cursor.execute(update_book_query, (isbn,))
            self.conn.commit()
            print(
                f"✅ Book with ISBN {isbn} returned successfully by Roll Number {rollNo}."
            )
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"❌ Error: Could not return book! {e}")
            return False

    # Student Specific Methods

    def view_borrowed_books(self, rollnumber):
        print("\n--- Borrowed Books ---")
        try:
            query = """
            SELECT
                b.title AS book_title,
                b.isbn,
                i.issued_at,
                s.rollnumber,
                u.name AS student_name
            FROM issued_books i
            INNER JOIN students s ON i.student_id = s.user_id
            INNER JOIN books b ON i.book_isbn = b.isbn
            INNER JOIN users u ON s.user_id = u.id
            WHERE s.rollnumber = %s
            ORDER BY i.issued_at DESC
        """
            self.cursor.execute(query, (rollnumber,))
            borrowed_books = self.cursor.fetchall()

            print("\n--- Borrowed Books ---")
            if not borrowed_books:
                print("📭 No borrowed books found for this student.")
                return

            for entry in borrowed_books:
                print(
                    f"📖 Book Title: {entry['book_title']} | "
                    f"ISBN: {entry['isbn']} | "
                    f"Issued to: {entry['student_name']} ({entry['rollnumber']}) | "
                    f"Issued On: {entry['issued_at']}"
                )
        except Exception as e:
            print(f"❌ Error: Could not retrieve borrowed books! {e}")
            return
