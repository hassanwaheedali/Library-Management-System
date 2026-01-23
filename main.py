from library import Library

# Title: The Alchemist
# Author: Paulo Coelho
# ISBN: 9783161484100
# Quantity: 37


def admin_panel(library, admin):
    print("\n--- Admin Panel ---")
    print(f"👑 ADMIN PANEL - Welcome {admin.name}")
    print("=" * 50)
    print("Book Management:")
    print("1. Add Book")
    print("2. Remove Book")
    print("3. Display Books")
    print("4. Search Books")
    print("=" * 50)
    print("User Management:")
    print("4. Add Student")
    print("5. Add Librarian")
    print("6. View All Users")
    print("7. Logout")
    print("=" * 50)
    print("-" * 50)

    while True:
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            title = input("Please Write Title: ")
            author = input("Please Write Author: ")
            try:
                isbn = int(input("Please Write ISBN Number without Dashes: "))
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue
            try:
                quantity = int(input("Please Write Quantity: "))
            except ValueError:
                print("❌ Error: Quantity must be a number!")
                continue
            try:
                shelfNumber = int(input("Please Write Shelf Number: "))
            except ValueError:
                print("❌ Error: Shelf Number must be a number!")
                continue
            library.add_books(title, author, isbn, quantity, shelfNumber)
            library.save_data()
            print("Book Added Successfully!")

        elif choice == "2":
            try:
                isbn = int(
                    input(
                        "Please Enter ISBN Number without Dashes of the Book to Remove: "
                    )
                )
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue

            library.remove_books(isbn)
            library.save_data()
            print("Book Removed Successfully!")

        elif choice == "3":
            library.display_books()

        elif choice == "4":
            searchValue = input("Please Enter Title, Author or ISBN to Search: ")
            library.search_books(searchValue)

        elif choice == "5":
            name = input("Enter Student Name: ")
            username = input("Enter Student Username: ")
            password = input("Enter Student Password: ")
            rollNo = input("Enter Student Roll Number: ")
            library.add_student(name, username, password, rollNo)

        elif choice == "6":
            name = input("Enter Librarian Name: ")
            username = input("Enter Librarian Username: ")
            password = input("Enter Librarian Password: ")
            employee_id = input("Enter Librarian Employee ID: ")
            library.add_librarian(name, username, password, employee_id)

        elif choice == "7":
            library.view_all_users()

        elif choice == "7":
            print("Logging out from Admin Panel.")
            main()
            break

        else:
            print("Invalid choice. Please try again.")


def librarian_panel(library, librarian_user):
    print("\n" + "=" * 50)
    print(f"👨‍💼 LIBRARIAN PANEL - Welcome {librarian_user.name}")
    print("=" * 50)
    print("Book Management:")
    print("1. Add Book")
    print("2. Update Book")
    print("3. Display Books")
    print("4. Search Books")
    print("5. Remove Book")
    print("-" * 20)
    print("Book Transactions:")
    print("6. Issue Book")
    print("7. Return Book")
    print("8. Check Issued Books History")
    print("9. Find Issued Books by Roll Number")
    print("10. Find Books in Shelf Number")
    print("-" * 20)
    print("User Management:")
    print("11. Add Student")
    print("12. View All Students")
    print("-" * 20)
    print("Account Settings:")
    print("13. Change Password")
    print("14. Change Username")
    print("-" * 20)
    print("15. Logout")
    print("=" * 50)

    while True:
        userChoice = input("\nPlease Enter Choice (1-15): ")

        if userChoice == "1":
            title = input("Please Write Title: ")
            author = input("Please Write Author: ")
            try:
                isbn = int(input("Please Write ISBN Number without Dashes: "))
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue

            try:
                quantity = int(input("Please Write Quantity: "))
            except ValueError:
                print("❌ Error: Quantity must be a number!")
                continue
            try:
                shelfNumber = int(input("Please Write Shelf Number: "))
            except ValueError:
                print("❌ Error: Shelf Number must be a number!")
                continue

            library.add_books(title, author, isbn, quantity, shelfNumber)
            library.save_data()

        elif userChoice == "2":
            try:
                isbn = int(
                    input(
                        "Please Enter ISBN Number without Dashes of the Book to Update: "
                    )
                )
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue
            choice = input(
                "Please Write What To Update (title, author, isbn, quantity, shelfnumber): "
            )
            library.update_book(isbn, choice)
            library.save_data()

        elif userChoice == "3":
            library.display_books()

        elif userChoice == "4":
            searchValue = input("Please Enter Title, Author or ISBN to Search: ")
            library.search_books(searchValue)

        elif userChoice == "5":
            try:
                isbn = int(
                    input(
                        "Please Enter ISBN Number without Dashes of the Book to Remove: "
                    )
                )
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue

            library.remove_books(isbn)
            library.save_data()

        elif userChoice == "6":
            try:
                rollNo = input("Please Enter Student Roll Number: ")
                isbn = int(
                    input(
                        "Please Enter ISBN Number of the Book without Dashes to Issue: "
                    )
                )
            except ValueError:
                print("❌ Error: Invalid input!")
                continue

            # Try to issue book
            success = library.issue_book(rollNo, isbn)

            # If student doesn't exist, offer to create them
            if not success:
                print("❌ Student not found.")
                create_student = input(
                    "\nWould you like to add this student now? (yes/no): "
                ).lower()
                if create_student == "yes":
                    name = input("Enter Student Name: ")
                    username = input("Enter Student Username: ")
                    password = input("Enter Student Password: ")
                    rollNo = input("Enter Student Roll Number: ")
                    library.add_student(name, username, password, rollNo)
                    library.save_users_data()

                    # Try issuing the book again
                    print("\nNow issuing the book...")
                    library.issue_book(rollNo, isbn)
                    library.save_data()
                else:
                    print("❌ Book issue cancelled.")
            else:
                library.save_data()
                print(f"✅ Book issued successfully to student with Roll No: {rollNo}")

        elif userChoice == "7":
            try:
                isbn = int(
                    input(
                        "Please Enter ISBN Number of the Book without Dashes to Return: "
                    )
                )
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue
            rollNo = input("Please Enter Your Roll Number: ")
            library.return_book(rollNo, isbn)
            library.save_data()

        elif userChoice == "8":
            library.check_issue_books()

        elif userChoice == "9":
            rollnumber = input(
                "Please Enter Student Roll Number to Search Issued Books: "
            )
            library.check_issue_books_finder(rollnumber)

        elif userChoice == "10":
            try:
                shelfNumber = int(input("Please Enter Shelf Number to Find Books: "))
            except ValueError:
                print("❌ Error: Shelf Number must be a number!")
                continue
            library.find_shelf_books(shelfNumber)

        elif userChoice == "11":
            name = input("Enter Student Name: ")
            username = input("Enter Student Username: ")
            password = input("Enter Student Password: ")
            rollNo = input("Enter Student Roll Number: ")
            library.add_student(name, username, password, rollNo)
            library.save_users_data()
            print("✅ Student Added Successfully!")

        elif userChoice == "12":
            library.view_all_users()

        elif userChoice == "13":
            user_id = input("Enter User ID: ")
            old_password = input("Enter Old Password: ")
            new_password = input("Enter New Password: ")
            library.change_password(user_id, old_password, new_password)

        elif userChoice == "14":
            user_id = input("Enter User ID: ")
            new_name = input("Enter New Username: ")
            library.change_username(user_id, new_name)

        elif userChoice == "15":
            print("👋 Goodbye, Logging out from Librarian Panel.")
            main()
            break

        else:
            print("⚠️  Invalid choice, please try again.")


def student_panel(library, student_user):
    print("\n--- Student Panel ---")
    print(f"🎓 STUDENT PANEL - Welcome {student_user.name}")
    print("=" * 50)
    print("1. View Available Books")
    print("2. Search Books")
    print("=" * 50)
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. View Borrowed Books")
    print("=" * 50)
    print("6. Logout")
    print("=" * 50)

    while True:
        userChoice = input("\nPlease Enter Choice (1-6): ")
        if userChoice == "1":
            library.display_books()

        elif userChoice == "2":
            searchValue = input("Please Enter Title, Author or ISBN to Search: ")
            library.search_books(searchValue)

        elif userChoice == "3":
            try:
                isbn = int(
                    input(
                        "Please Enter ISBN Number of the Book without Dashes to Borrow: "
                    )
                )
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue

            library.issue_book(student_user.rollnumber, isbn)
            library.save_data()

        elif userChoice == "4":
            try:
                isbn = int(
                    input(
                        "Please Enter ISBN Number of the Book without Dashes to Return: "
                    )
                )
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue
            library.return_book(student_user.rollnumber, isbn)
            library.save_data()

        elif userChoice == "5":
            library.view_borrowed_books(student_user.rollnumber)

        elif userChoice == "6":
            print("👋 Goodbye, Logging out from Student Panel.")
            main()
            break

        else:
            print("⚠️  Invalid choice, please try again.")


def main():
    library = Library()
    library.load_data()
    library.load_users_data()
    print("=" * 50)
    print("--- Welcome to the Library Management System! ---")
    print("=" * 50)

    print("=" * 50)
    print("🔐 LOGIN")
    print("=" * 50)

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user = library.login(username, password)
    login = False
    if user is None:
        continue_login = input("Would you like to try again? (yes/no): ").lower()
        if continue_login == "yes" or continue_login == "y":
            main()  # Restart the login process
        else:
            print("👋 Goodbye!")
            return
    else:
        login = True

    if login and user.get_role() == "Admin":
        admin_panel(library, user)

    elif login and user.get_role() == "Librarian":
        librarian_panel(library, user)

    elif login and user.get_role() == "Student":
        student_panel(library, user)


if __name__ == "__main__":
    main()
