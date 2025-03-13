import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Page configuration
st.set_page_config(page_title="Library Management System",
                   page_icon="📚", layout="wide")

# MongoDB connection
load_dotenv()
@st.cache_resource
def get_database():
    CONNECTION_STRING = os.getenv('MONGO_DB_CONNECT')
    client = MongoClient(CONNECTION_STRING)
    return client['LibraryDB']
db = get_database()
books_collection = db['books']


# Add a book
def add_a_book():
    st.header('💾 Add a Book')

    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input('Title')
        author = st.text_input('Author')
        publication_year = st.text_input('Publication Year')
    with col2:
        genre = st.text_input('Genre')
        read_status = st.selectbox('Read Status', ['True', 'False'])

    if st.button('Save Book'):
        new_book = {
            "Title": title,
            "Author": author,
            "Publication Year": publication_year,
            "Genre": genre,
            "Read Status": read_status
        }
        books_collection.insert_one(new_book)
        st.success(f"Book: '{title}' successfully added")

# Remove a book
def remove_a_book():
    st.header('🗑️ Remove a Book')
    title = st.text_input('Title to remove')
    if st.button('Remove Book'):
        result = books_collection.delete_one({"Title": title})
        if result.deleted_count > 0:
            st.success(f"Book: '{title}' successfully deleted")
        else:
            st.warning(f"Book: '{title}' not found")

# Display all books
def display_all_books():
    st.header('📕 All Books')
    books = list(books_collection.find())
    if books:
        st.dataframe(books, use_container_width=True)
    else:
        st.info("No books available.")

# Search for a book
def search_for_a_book():
    st.header('📖 Search for a Book')
    search_by = st.selectbox(
        'Search by', ['Title', 'Author', 'Genre', 'Read Status'])
    search_term = st.text_input('Enter a search term')

    if search_term:
        query = {search_by: {'$regex': search_term, '$options': 'i'}}
        search_results = list(books_collection.find(query))
        if search_results:
            st.dataframe(search_results, use_container_width=True)
        else:
            st.info("No matching books found.")

# Display statistics
def display_statistics():
    st.header('📊 Library Statistics')
    total_books = books_collection.count_documents({})
    read_books = books_collection.count_documents({"Read Status": "True"})
    read_percentage = (read_books / total_books *
                       100) if total_books > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Read Books Percentage", f"{read_percentage:.1f}%")


# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Select an option:", [
    "Add a Book", "Remove a Book", "Display all Books", "Search for a Book", "Display Statistics"
])

# Display selected page
if choice == "Add a Book":
    add_a_book()
elif choice == "Remove a Book":
    remove_a_book()
elif choice == "Display all Books":
    display_all_books()
elif choice == "Search for a Book":
    search_for_a_book()
else:
    display_statistics()
