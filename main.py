from library import Library

# Title: The Alchemist
# Author: Paulo Coelho
# ISBN: 9783161484100
# Quantity: 37


def main():
    library = Library()
    library.load_data()
    print("=" * 50)
    print("--- Welcome to the Library Management System! ---")
    print("=" * 50)

    print("\nMenu:")
    print("-" * 20)

    print("1: Press 1 to Add Books")
    print("2: Press 2 to Update Book")
    print("3: Press 3 to Display Books")
    print("4: Press 4 to Search Books")
    print("5: Press 5 to Remove Book")

    print("-" * 20)

    print("6: Press 6 to Issue Book")
    print("7: Press 7 to Check Issued Books History")
    print("8: Press 8 to Find Issued Books by Roll Number")
    print("9: Press 9 to Find Books in Shelf Number")

    print("-" * 20)
    print("10: Press 10 to Return The Book")

    print("-" * 20)
    print("11: Press 11 to Stop Program")
    print("-" * 20)

    while True:

        userChoice = input("\nPlease Enter Choice (1,11): ")

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
                user = input("Please Enter Name: ")
                rollNo = input("Please Enter Roll Number: ")
                isbn = int(input(
                    "Please Enter ISBN Number of the Book without Dashes to Issue: "
                ))
            except ValueError:
                print("❌ Error: Invalid input!")
                continue

            library.issue_book(user, rollNo, isbn)
            library.save_data()

        elif userChoice == "7":
            library.check_issue_books()

        elif userChoice == "8":
            rollnumber = input("Please Enter Roll Number to Search Issued Books: ")
            library.check_issue_books_finder(rollnumber)

        elif userChoice == "9":
            try:
                shelfNumber = int(input("Please Enter Shelf Number to Find Books: "))
            except ValueError:
                print("❌ Error: Shelf Number must be a number!")
                continue
            library.find_shelf_books(shelfNumber)

        elif userChoice == "10":
            try:
                isbn = int(input(
                    "Please Enter ISBN Number of the Book without Dashes to Return: "
                ))
            except ValueError:
                print("❌ Error: ISBN must be a number!")
                continue
            rollNo = input("Please Enter Your Roll Number: ")
            library.return_book(rollNo, isbn)
            library.save_data()

        elif userChoice == "11":
            print("👋 Goodbye, Closing the library System.")
            break

        else:
            print("⚠️  Invalid choice, please try again.")


if __name__ == "__main__":
    main()
