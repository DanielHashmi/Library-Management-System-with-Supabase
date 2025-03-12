# Library Management System Using Pandas & Streamlit

This is a simple Library Management System built using Streamlit and Pandas. It allows you to manage a collection of books, including adding, removing, displaying, and searching for books, as well as displaying statistics about the collection.

## Features

- **Add a Book**: Add a new book to the library.
- **Remove a Book**: Remove an existing book from the library.
- **Display all Books**: Display all books in the library.
- **Search for a Book**: Search for a book by title, author, genre, or read status.
- **Display Statistics**: Display statistics about the library, including the total number of books and the percentage of books that have been read.

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/DanielHashmi/-Library-Management-System.git
    cd -Library-Management-System
    ```

2. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

3. Make sure you have a `library.csv` file in the project directory with the following columns:

    ```csv
    Title,Author,Publication Year,Genre,Read Status
    ```

## Usage

Run the Streamlit app:

```sh
streamlit run library_manager.py
```