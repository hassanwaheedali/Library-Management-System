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
    print("5. Add Student")
    print("6. Add Librarian")
    print("7. View All Users")
    print("=" * 50)
    print("Account Settings:")
    print("8. Change Password")
    print("9. Change Username")
    print("=" * 50)
    print("10. Logout")
    print("=" * 50)
    print("-" * 50)

    while True:
        choice = input("Enter your choice (1-10): ")

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
            print("Book Removed Successfully!")

        elif choice == "3":
            library.display_books()

        elif choice == "4":
            searchValue = input("Please Enter Title, Author or ISBN to Search: ")
            library.search_books(searchValue)

        elif choice == "5":
            name = input("Enter Student Name: ")
            username = input("Enter Student Username: ")
            while True:
                password = input("Enter Student Password: ")
                confirm_password = input("Confirm Student Password: ")
                if password == confirm_password:
                    break
                print("❌ Error: Passwords do not match! Please type them again.")
            rollNo = input("Enter Student Roll Number: ")
            library.add_student(name, username, password, rollNo)

        elif choice == "6":
            name = input("Enter Librarian Name: ")
            username = input("Enter Librarian Username: ")
            while True:
                password = input("Enter Librarian Password: ")
                confirm_password = input("Confirm Librarian Password: ")
                if password == confirm_password:
                    break
                print("❌ Error: Passwords do not match! Please type them again.")
            employee_id = input("Enter Librarian Employee ID: ")
            library.add_librarian(name, username, password, employee_id)

        elif choice == "7":
            library.view_all_users()

        elif choice == "8":
            username = input("Enter Username: ")
            old_password = input("Enter Old Password: ")
            new_password = input("Enter New Password: ")
            library.change_password(username, old_password, new_password)

        elif choice == "9":
            old_username = input("Enter Current Username: ")
            new_username = input("Enter New Username: ")
            library.change_username(old_username, new_username)

        elif choice == "10":
            print("Logging out from Admin Panel.")
            return

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
                "Please Write What To Update (title, author, isbn, quantity, shelf_number): "
            )
            library.update_book(isbn, choice)

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

                    # Try issuing the book again
                    print("\nNow issuing the book...")
                    library.issue_book(rollNo, isbn)
                else:
                    print("❌ Book issue cancelled.")
            else:
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
            rollNo = input("Please Enter Student Roll Number: ")
            library.return_book(rollNo, isbn)

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
            confirm_password = input("Confirm Student Password: ")
            if password != confirm_password:
                print("❌ Error: Passwords do not match!")
                continue
            rollNo = input("Enter Student Roll Number: ")
            library.add_student(name, username, password, rollNo)
            print("✅ Student Added Successfully!")

        elif userChoice == "12":
            library.view_all_students()

        elif userChoice == "13":
            username = input("Enter Username: ")
            old_password = input("Enter Old Password: ")
            new_password = input("Enter New Password: ")
            library.change_password(username, old_password, new_password)

        elif userChoice == "14":
            old_username = input("Enter Current Username: ")
            new_username = input("Enter New Username: ")
            library.change_username(old_username, new_username)

        elif userChoice == "15":
            print("👋 Goodbye, Logging out from Librarian Panel.")
            return

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
    print("Account Settings: ")
    print("6. Change Password")
    print("7. Change Username")
    print("=" * 50)
    print("8. Logout")
    print("=" * 50)

    while True:
        userChoice = input("\nPlease Enter Choice (1-8): ")
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

        elif userChoice == "5":
            library.view_borrowed_books(student_user.rollnumber)

        elif userChoice == "6":
            old_password = input("Enter Old Password: ")
            new_password = input("Enter New Password: ")
            library.change_password(student_user.username, old_password, new_password)

        elif userChoice == "7":
            new_username = input("Enter New Username: ")
            library.change_username(student_user.username, new_username)

        elif userChoice == "8":
            print("👋 Goodbye, Logging out from Student Panel.")
            return

        else:
            print("⚠️  Invalid choice, please try again.")


def main():
    library = Library()
    print("=" * 50)
    print("--- Welcome to the Library Management System! ---")
    print("=" * 50)

    while True:
        print("\n" + "=" * 50)
        print("🔐 LOGIN")
        print("=" * 50)

        username = input("Enter your username: ")
        password = input("Enter your password: ")

        user = library.login(username, password)

        if user is None:
            continue_login = input("Would you like to try again? (yes/no): ").lower()
            if continue_login == "yes" or continue_login == "y":
                continue
            else:
                print("👋 Goodbye!")
                break
        else:
            # Execute appropriate panel
            if user.role == "Admin":
                admin_panel(library, user)
            elif user.role == "Librarian":
                librarian_panel(library, user)
            elif user.role == "Student":
                student_panel(library, user)
            else:
                print("❌ Unknown role. Contact the administrator.")

            # After logout, ask if user wants to login again
            continue_login = input(
                "\nWould you like to login again? (yes/no): "
            ).lower()
            if continue_login != "yes" and continue_login != "y":
                print("👋 Goodbye!")
                break


if __name__ == "__main__":
    main()
