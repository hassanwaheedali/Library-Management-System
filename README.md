# 📚 Library Management System

A comprehensive Python-based Library Management System with role-based access control, user authentication, and persistent data storage. Designed to efficiently manage book collections, user accounts, track inventory, and handle book issuing/returning operations.

## 🌟 Features

### Authentication & Authorization

- **Role-Based Access Control**: Three distinct user roles (Admin, Librarian, Student)
- **Secure Login System**: Username and password authentication
- **Default Admin Account**: Pre-configured admin for initial setup (username: `admin`, password: `admin123`)

### User Management

- **Add Students**: Register new students with username, password, and roll number
- **Add Librarians**: Register librarian accounts with employee IDs
- **View All Users**: Display complete list of all system users by role
- **Change Password**: Update password for any user account (requires old password verification)
- **Change Username**: Update username for any user account
- **User Persistence**: All user data stored in separate JSON file

### Book Management (Admin & Librarian)

- **Add Books**: Register new books with title, author, ISBN, quantity, and shelf location
- **Update Books**: Modify any book attribute (title, author, ISBN, quantity, shelf number)
- **Remove Books**: Delete books from the library collection
- **Display All Books**: View complete library inventory with details
- **Search Books**: Find books by title, author, or ISBN
- **Find Books by Shelf**: Locate all books on a specific shelf

### Book Circulation Management (Librarian & Student)

- **Issue Books**: Issue books to registered students only (validates student existence)
- **On-the-Fly Registration**: Create new student accounts during book issuing if needed (Librarian only)
- **Borrow Books**: Students can directly borrow available books
- **Return Books**: Process book returns and update inventory
- **View Issued Books History**: Complete log of all book transactions with foreign key lookups (Librarian)
- **View Borrowed Books**: Students can see all their currently borrowed books
- **Search Issued Books**: Find all books issued to a specific student by roll number (Librarian)

### Data Persistence

- **Dual JSON Storage**: Separate files for library data and user data
- **Foreign Key Relationships**: Efficient data referencing (stores only IDs, not duplicate data)
- **Auto-save**: All changes immediately persisted to JSON
- **Auto-load**: Previous data restored on program startup
- **Data Integrity**: Comprehensive error handling and validation

## 🏗️ Architecture

### Project Structure

```
project1/
├── main.py              # Entry point - UI and role-based menu systems
├── library.py           # Library class - Core business logic
├── book.py              # Book class - Data model
├── person.py            # Person class hierarchy - User models (Admin, Librarian, Student)
├── library_data.json    # Persistent storage for books and issued books (auto-generated)
├── users_data.json      # Persistent storage for users (auto-generated)
└── README.md            # Project documentation
```

### Class Design

#### **Person Class Hierarchy** (`person.py`)

Abstract base class with three concrete implementations:

**Person (Abstract Base Class)**

- `name`: User's full name
- `user_id`: Login username (unique identifier)
- `password`: User password
- `get_role()`: Abstract method returning user role
- `to_dict()`: Serialization for JSON storage

**Admin Class**

- `admin_id`: Unique admin identifier
- Full access to user management and book operations

**Librarian Class**

- `employee_id`: Unique employee identifier
- Access to book management and circulation operations

**Student Class**

- `rollnumber`: Unique student roll number
- Access to book browsing and personal account management

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

Manages the entire library system with three main collections:

- `_books`: List of all Book objects
- `_issuedBooks`: List of issue records with **foreign keys only** (rollNo, isbn, timestamp)
- `_users`: List of all Person objects (Admin, Librarian, Student)

**User Management Methods:**

- `login()`: Authenticate users by username and password
- `add_admin()`: Register new admin accounts
- `add_librarian()`: Register new librarian accounts
- `add_student()`: Register new student accounts
- `view_all_users()`: Display all users organized by role
- `change_password()`: Update user password with old password verification
- `change_username()`: Update user's username with duplicate validation

**Book Management Methods:**

- `add_books()`: Add new books with validation
- `update_book()`: Modify book attributes
- `remove_books()`: Delete books from inventory
- `display_books()`: Show all books
- `search_books()`: Search by multiple criteria
- `find_shelf_books()`: Locate books by shelf number

**Circulation Methods:**

- `issue_book()`: Issue books to **registered students only** with validation
- `return_book()`: Process returns and update quantities
- `check_issue_books()`: View complete issue history (uses foreign key lookups)
- `check_issue_books_finder()`: Search issues by roll number (uses foreign key lookups)
- `view_borrowed_books()`: Display all books borrowed by a specific student

**Data Persistence Methods:**

- `save_data()`: Save books and issued books to `library_data.json`
- `load_data()`: Restore books and issued books from JSON
- `save_users_data()`: Save users to `users_data.json`
- `load_users_data()`: Restore users from JSON

### Data Flow

```
User Login (main.py)
    ↓
Authentication (library.login())
    ↓
Role Detection (Admin/Librarian/Student)
    ↓
Role-Specific Panel
    ↓
Library Methods (library.py)
    ↓
Book/Person Objects (book.py/person.py)
    ↓
Dual JSON Storage (library_data.json + users_data.json)
```

## 🚀 Getting Started

### Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses standard library only)

### Installation

1. Clone or download the project files
2. Ensure all four Python files are in the same directory:
   - `main.py`
   - `library.py`
   - `book.py`
   - `person.py`

### Running the Program

```bash
python main.py
```

### Default Login Credentials

**Admin Account** (pre-configured):

- Username: `admin`
- Password: `admin123`

_Note: Use admin account to create librarian and student accounts_

## 📖 Usage Guide

### Login Flow

1. Enter username
2. Enter password
3. System detects role and redirects to appropriate panel

### Admin Panel Options

```
Book Management:
1. Add Book
2. Remove Book
3. Display Books
4. Search Books

User Management:
5. Add Student
6. Add Librarian
7. View All Users
8. Change Password
9. Change Username
10. Logout
```

### Librarian Panel Options

```
Book Management:
1. Add Book
2. Update Book
3. Display Books
4. Search Books
5. Remove Book

Book Transactions:
6. Issue Book
7. Return Book
8. Check Issued Books History
9. Find Issued Books by Roll Number
10. Find Books in Shelf Number

User Management:
11. Add Student
12. View All Students

Account Settings:
13. Change Password
14. Change Username

15. Logout
```

### Student Panel Options

```
Book Browsing:
1. View Available Books
2. Search Books

Book Transactions:
3. Borrow Book
4. Return Book
5. View Borrowed Books

Account Settings:
6. Change Password
7. Change Username

8. Logout
```

### Example Workflows

#### First Time Setup (Admin)

1. Login with default admin credentials
2. Add librarian accounts (Option 6)
3. Add initial student accounts (Option 5)
4. Add books to library (Option 1)

#### Issuing a Book (Librarian)

1. Login as librarian
2. Select option `6` (Issue Book)
3. Enter student roll number
4. Enter book ISBN
5. **System validates:**
   - Student exists in database
   - Book exists and is available
6. If student doesn't exist, option to create account on-the-fly
7. System decrements quantity and logs transaction

#### Borrowing a Book (Student)

1. Login as student
2. Select option `3` (Borrow Book)
3. Enter book ISBN
4. **System validates:**
   - Book exists and is available
   - Student account is active
5. System issues book and decrements quantity
6. Transaction logged with timestamp

#### Returning a Book (Student)

1. Login as student
2. Select option `4` (Return Book)
3. Enter book ISBN of borrowed book
4. System validates the issue record
5. Book quantity incremented
6. Issue record removed from system

#### Viewing Borrowed Books (Student)

1. Login as student
2. Select option `5` (View Borrowed Books)
3. System displays all currently borrowed books with:
   - Book title
   - ISBN
   - Issue date and time

#### Viewing Issued Books (Librarian)

1. Login as librarian
2. Select option `8` (Check Issued Books History)
3. System displays all transactions with:
   - Timestamp
   - Student name (looked up via foreign key)
   - Book title (looked up via foreign key)
   - Roll number and ISBN

#### Changing Password (All Users)

1. Select "Change Password" from respective panel
2. Enter old password
3. Enter new password
4. System validates old password and updates
5. Changes saved to users_data.json

#### Changing Username (All Users)

1. Select "Change Username" from respective panel
2. Enter new desired username
3. System checks for duplicate usernames
4. If available, username updated
5. Changes saved to users_data.json

## 🔒 Data Validation

The system includes comprehensive input validation:

- ✅ User authentication (username/password verification)
- ✅ Old password verification for password changes
- ✅ Duplicate username prevention for username changes
- ✅ **Student existence validation** before issuing books
- ✅ Duplicate ISBN prevention
- ✅ Duplicate username/user_id prevention
- ✅ Negative quantity/shelf number checks
- ✅ Book availability verification before issuing
- ✅ ISBN and quantity type validation
- ✅ Roll number verification for returns
- ✅ Issue record validation for returns
- ✅ Role-based access control
- ✅ Type consistency for roll numbers (string) and ISBNs (integer)

## 💾 Data Storage

The system uses **two separate JSON files** for data persistence:

### `library_data.json`

Stores books and issued books with **foreign key relationships**:

```json
{
  "Books": [
    {
      "title": "The Alchemist",
      "author": "Paulo Coelho",
      "isbn": 9783161484100,
      "quantity": 36,
      "shelfNumber": 5
    }
  ],
  "issuedBooks": [
    {
      "timeStamp": "2026-01-23 14:30:15",
      "rollNo": "S12345",
      "isbn": 9783161484100
    }
  ]
}
```

**Note**: Issued books store **only foreign keys** (rollNo, isbn). Student names and book titles are looked up dynamically from their respective sources, ensuring data integrity when updates occur.

### `users_data.json`

Stores all user accounts with username-based identification:

```json
{
  "Users": [
    {
      "name": "Default Admin",
      "username": "admin",
      "password": "admin123",
      "admin_id": 1,
      "role": "Admin"
    },
    {
      "name": "John Smith",
      "username": "lib001",
      "password": "pass123",
      "employee_id": "EMP001",
      "role": "Librarian"
    },
    {
      "name": "Alice Johnson",
      "username": "alice_j",
      "password": "student123",
      "rollnumber": "S12345",
      "role": "Student"
    }
  ]
}
```

**Note**: The system supports backward compatibility with old JSON files that use `user_id` instead of `username`.

## 🎯 Key Features Highlights

- **Complete Student Panel**: Fully functional interface for students to browse, borrow, and manage their book transactions
- **Role-Based Access Control**: Separate interfaces for Admin, Librarian, and Student with appropriate permissions
- **Authentication System**: Secure login with username/password
- **Password & Username Management**: All users can change their passwords and usernames with validation
- **Object-Oriented Design**: Clean separation of concerns with Person hierarchy, Book, and Library classes
- **Foreign Key Relationships**: Efficient data storage mimicking database design principles
- **Dual Data Persistence**: Separate JSON files for library data and user data
- **User-Friendly Interface**: Clear menu systems with emoji indicators for each role
- **Error Handling**: Comprehensive validation and error messages
- **Transaction Tracking**: Complete audit trail of book issues/returns with timestamps
- **Dynamic Data Lookup**: Student names and book titles retrieved via foreign keys to ensure data consistency
- **Flexible Search**: Search books by multiple criteria simultaneously
- **On-Demand Registration**: Create student accounts during book issuing workflow (Librarian feature)
- **No Infinite Recursion**: Proper logout and re-login flow without stack overflow issues
- **Type Consistency**: Roll numbers as strings, ISBNs as integers for reliable comparisons
- **Backward Compatibility**: Supports old JSON files with `user_id` field

## 🛠️ Technical Implementation

- **Language**: Python 3
- **Data Storage**: Dual JSON files (library_data.json, users_data.json)
- **Design Pattern**: Object-Oriented Programming (OOP) with inheritance
- **Architecture**: Role-based access control (RBAC)
- **Data Relationships**: Foreign key pattern for referential integrity
- **Time Handling**: datetime module for timestamp generation
- **Data Structure**: Lists and dictionaries for efficient data management
- **Abstraction**: Abstract base class (ABC) for Person hierarchy

### Student Panel Options

```
Book Browsing:
1. View Available Books
2. Search Books

Book Transactions:
3. Borrow Book
4. Return Book
5. View Borrowed Books

Account Settings:
6. Change Password
7. Change Username

8. Logout
```

Students have full access to browse books, borrow/return books, view their borrowing history, and manage their account settings.

## 🔮 Future Enhancements

### Potential Improvements for Future Versions

- Password hashing for enhanced security (bcrypt, SHA-256)
- Fine calculation for overdue books with configurable rates
- Book reservation system (reserve books that are currently issued)
- Due date system with automatic tracking
- Email/SMS notifications for overdue books and reservations
- Multiple library branches support with inter-branch transfers
- Database integration (SQLite/PostgreSQL) for better scalability
- Web-based interface (Flask/Django/FastAPI)
- RESTful API for mobile app integration
- Barcode/QR code scanning support for quick book identification
- Advanced reporting and analytics dashboard
- Export functionality (CSV, Excel, PDF reports)
- User activity logs and comprehensive audit trails
- Book cover image support with preview
- Book ratings and reviews system
- Popular books and recommendation engine
- Multi-language support (i18n)
- Dark mode UI option
- Backup and restore functionality
- Integration with online book databases (Google Books API, Open Library)
- Prevent duplicate book borrowing (student can't borrow same book twice)
- Book renewal system (extend borrowing period)
- Reading history and statistics for students
- Library announcements and notifications system

## 🔐 Security Notes

**Current Implementation:**

- Passwords are stored in plain text in `users_data.json`
- Default admin credentials should be changed after first login
- User permissions are enforced through role-based menus

**Recommended for Production:**

- Implement password hashing (bcrypt, SHA-256)
- Add session management
- Implement password strength requirements
- Add account lockout after failed login attempts
- Use environment variables for sensitive data

---

## 👨‍💻 Developer

**Hassan Waheed Ali**

GitHub: [github.com/hassanwaheedali](https://github.com/hassanwaheedali/)

---

_Built with ❤️ using Python_
