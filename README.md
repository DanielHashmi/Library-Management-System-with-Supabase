# 📚 Library Management System

A simple Library Management System built with **Streamlit** and **MongoDB**. It allows users to add, remove, display, search books, and view basic statistics.

## Features
- **Add a Book**: Save book details (title, author, year, genre, and read status).
- **Remove a Book**: Delete a book by its title.
- **Display all Books**: View all books in a table format.
- **Search for a Book**: Search by title, author, genre, or read status.
- **Statistics**: See the total number of books and percentage of read books.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DanielHashmi/-Library-Management-System.git
cd -Library-Management-System
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB connection:
   - Create a `.env` file:
```plaintext
MONGO_DB_CONNECT=your_mongodb_connection_string
```

4. Run the app:
```bash
streamlit run library_manager.py
```

## Author
- **Daniel Hashmi**

