# 📚 Library Management System

A comprehensive Python-based Library Management System with persistent data storage, designed to efficiently manage book collections, track inventory, and handle book issuing/returning operations.

## 🌟 Features

### Core Functionality
- **Add Books**: Register new books with title, author, ISBN, quantity, and shelf location
- **Update Books**: Modify any book attribute (title, author, ISBN, quantity, shelf number)
- **Remove Books**: Delete books from the library collection
- **Display All Books**: View complete library inventory with details
- **Search Books**: Find books by title, author, or ISBN
- **Find Books by Shelf**: Locate all books on a specific shelf

### Book Circulation Management
- **Issue Books**: Track book lending to students with timestamps
- **Return Books**: Process book returns and update inventory
- **View Issued Books History**: Complete log of all book transactions
- **Search Issued Books**: Find all books issued to a specific student by roll number

### Data Persistence
- **Auto-save**: All data saved to JSON format
- **Auto-load**: Previous data restored on program startup
- **Data Integrity**: Comprehensive error handling and validation

## 🏗️ Architecture

### Project Structure
```
project1/
├── main.py              # Entry point - User interface and menu system
├── library.py           # Library class - Core business logic
├── book.py              # Book class - Data model
├── library_data.json    # Persistent storage (auto-generated)
└── README.md            # Project documentation
```

### Class Design

#### **Book Class** (`book.py`)
Represents individual books with attributes:
- `title`: Book title
- `author`: Author name
- `isbn`: International Standard Book Number (unique identifier)
- `quantity`: Available copies
- `shelfNumber`: Physical location in library

Methods:
- `to_dict()`: Serializes book data for JSON storage
- `__str__()`: Formatted string representation for display

#### **Library Class** (`library.py`)
Manages the entire library system with two main collections:
- `_books`: List of all Book objects
- `_issuedBooks`: List of issue records (dictionaries with timestamp, user, rollNo, ISBN)

**Core Methods:**
- `add_books()`: Add new books with validation
- `update_book()`: Modify book attributes
- `remove_books()`: Delete books from inventory
- `display_books()`: Show all books
- `search_books()`: Search by multiple criteria
- `find_shelf_books()`: Locate books by shelf number

**Circulation Methods:**
- `issue_book()`: Issue books to students with timestamp tracking
- `return_book()`: Process returns and update quantities
- `check_issue_books()`: View complete issue history
- `check_issue_books_finder()`: Search issues by roll number

**Data Persistence Methods:**
- `save_data()`: Save library state to JSON file
- `load_data()`: Restore library state from JSON file

### Data Flow

```
User Input (main.py)
    ↓
Menu Selection
    ↓
Library Methods (library.py)
    ↓
Book Objects (book.py)
    ↓
JSON Storage (library_data.json)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses standard library only)

### Installation

1. Clone or download the project files
2. Ensure all three Python files are in the same directory:
   - `main.py`
   - `library.py`
   - `book.py`

### Running the Program

```bash
python main.py
```

## 📖 Usage Guide

### Main Menu Options

```
1.  Add Books
2.  Display All Books
3.  Search Books
4.  Update Book
5.  Remove Books
6.  Find Books by Shelf Number
7.  Issue Book
8.  Return Book
9.  Display All Issued Books
10. Search Issued Books by Roll Number
11. Exit
```

### Example Workflows

#### Adding a New Book
1. Select option `1`
2. Enter book title
3. Enter author name
4. Enter ISBN (numbers only)
5. Enter quantity
6. Enter shelf number

#### Issuing a Book
1. Select option `7`
2. Enter student name
3. Enter roll number
4. Enter book ISBN
5. System automatically decrements quantity and logs transaction

#### Searching Books
1. Select option `3`
2. Enter search term (can be title, author, or ISBN)
3. System displays all matching books

## 🔒 Data Validation

The system includes comprehensive input validation:
- ✅ Duplicate ISBN prevention
- ✅ Negative quantity/shelf number checks
- ✅ Book availability verification before issuing
- ✅ ISBN and quantity type validation
- ✅ Roll number verification for returns

## 💾 Data Storage

All data is stored in `library_data.json` with the following structure:

```json
{
    "Books": [
        {
            "title": "Book Title",
            "author": "Author Name",
            "isbn": 123456,
            "quantity": 5,
            "shelfNumber": 101
        }
    ],
    "issuedBooks": [
        {
            "timeStamp": "2026-01-22 14:30:00",
            "user": "Student Name",
            "rollNo": "2024-CS-001",
            "title": "Book Title",
            "isbn": 123456
        }
    ]
}
```

## 🎯 Key Features Highlights

- **Object-Oriented Design**: Clean separation of concerns with Book and Library classes
- **Data Persistence**: Automatic save/load functionality
- **User-Friendly Interface**: Clear menu system with emoji indicators
- **Error Handling**: Comprehensive validation and error messages
- **Transaction Tracking**: Complete audit trail of book issues/returns with timestamps
- **Flexible Search**: Search books by multiple criteria simultaneously

## 🛠️ Technical Implementation

- **Language**: Python 3
- **Data Storage**: JSON
- **Design Pattern**: Object-Oriented Programming (OOP)
- **Time Handling**: datetime module for timestamp generation
- **Data Structure**: Lists and dictionaries for efficient data management

## 🔮 Future Enhancements

Potential improvements for future versions:
- Database integration (SQLite/PostgreSQL)
- Fine calculation for overdue books
- Book reservation system
- Multiple library branches support
- Web-based interface
- Email notifications
- Barcode scanning support
- Advanced reporting and analytics

---

## 👨‍💻 Developer

**Hassan Waheed Ali**

GitHub: [github.com/hassanwaheedali](https://github.com/hassanwaheedali/)

---

*Built with ❤️ using Python*
