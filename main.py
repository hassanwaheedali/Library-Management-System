from library import Library

# Title: The Alchemist
# Author: Paulo Coelho
# ISBN: 9783161484100
# Quantity: 37


def main():
    library = Library()

    print("=" * 50)
    print("--- Welcome to the Library Management System! ---")
    print("=" * 50)

    print("\nMenu:")
    print("-" * 20)

    print("1: Press 1 to Add Books")
    print("2: Press 2 to Display Books")
    print("3: Press 3 to Search Books")

    print("-" * 20)

    print("4: Press 4 to Issue Book")
    print("5: Press 5 to Check Issued Books History")
    print("6: Press 6 to Find Issued Books by Roll Number")
    print("7: Press 7 to Find Books in Shelf Number")

    print("-" * 20)
    print("8: Press 8 to Return The Book")

    print("-" * 20)
    print("9: Press 9 to Stop Program")
    print("-" * 20)

    while True:

        userChoice = input("\nPlease Enter Choice (1,9): ")

        if userChoice == "1":
            title = input("Please Write Title: ")
            author = input("Please Write Author: ")
            isbn = input("Please Write ISBN Number: ")

            try:
                quantity = int(input("Please Write Quantity: "))
            except ValueError:
                print("❌ Error: Quantity must be a number!")

            try:
                shelfNumber = int(input("Please Write Shelf Number: "))
            except ValueError:
                print("❌ Error: Shelf Number must be a number!")

            library.add_books(title, author, isbn, quantity)

        elif userChoice == "2":
            library.display_books()

        elif userChoice == "3":
            searchValue = input("Please Enter Title, Author or ISBN to Search: ")
            library.search_books(searchValue)

        elif userChoice == "4":
            try:
                user = input("Please Enter Your Name: ")
                rollNo = input("Please Enter Your Roll Number: ")
                isbn = input("Please Enter ISBN Number of the Book to Issue: ")
            except ValueError:
                print("❌ Error: Invalid input!")

            library.issue_book(user, rollNo, isbn)

        elif userChoice == "5":
            library.check_issue_books()

        elif userChoice == "6":
            rollnumber = input("Please Enter Roll Number to Search Issued Books: ")
            library.check_issue_books_finder(rollnumber)

        elif userChoice == "7":
            shelfNumber = input("Please Enter Shelf Number to Find Books: ")
            library.find_shelf_books(shelfNumber)

        elif userChoice == "8":
            isbn = input("Please Enter ISBN Number of the Book to Return: ")
            rollNo = input("Please Enter Your Roll Number: ")
            library.return_book(rollNo, isbn)

        elif userChoice == "9":
            print("👋 Goodbye, Closing the library System.")
            break

        else:
            print("⚠️  Invalid choice, please try again.")


if __name__ == "__main__":
    main()
