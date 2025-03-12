import streamlit as st
import pandas as pd

# Page configuration and styling
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton button {
        width: 100%;
        margin: 0.5rem 0;
        border-radius: 5px;
        background-color: #4CAF50;
        color: white;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    h1 {
        color: #2C3E50;
        padding-bottom: 2rem;
    }
    h2 {
        color: #34495E;
        padding: 1rem 0;
    }
    .stDataFrame {
        padding: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Load the books dataset
books = pd.read_csv('library.csv')

# Functions
def display_statistics():
    col1, col2 = st.columns(2)
    books_count = len(books)
    read_books_count = len(books[books['Read Status'].astype(str) == 'True'])
    read_percentage = (read_books_count / len(books)) * 100
    
    with col1:
        st.metric("Total Books", books_count)
    with col2:
        st.metric("Read Books Percentage", f"{read_percentage:.1f}%")

def search_for_a_book():
    st.header('📖 Search for a Book')
    col1, col2 = st.columns([1, 2])
    with col1:
        search_by = st.selectbox('Search by', ['Title', 'Author', 'Genre', 'Read Status'], key='search_by')
    with col2:
        search_term = st.text_input('Enter a search term', key='search_term')
    
    if search_term:
        search_results = books[books[search_by].fillna('').str.contains(search_term, case=False, na=False)]
        st.dataframe(search_results, use_container_width=True)

def display_all_books():
    st.header('📕 All Books')
    st.dataframe(books, use_container_width=True)

def remove_a_book():
    st.header('🗑️ Remove a Book')
    title = st.text_input('Title to remove', key='remove_title')
    if title and st.button('Remove Book', type='primary'):
        global books
        filtered_books = books[books['Title'] != title]
        if books.equals(filtered_books):
            st.warning(f"Book: '{title}' not found")
            return
        books = filtered_books
        books.to_csv('library.csv', index=False)
        st.success(f"Book: '{title}' successfully deleted")

def add_a_book():
    st.header('💾 Add a Book')
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input('Title', key='add_title')
        author = st.text_input('Author', key='add_author')
        publication_year = st.text_input('Publication Year', key='add_year')
    with col2:
        genre = st.text_input('Genre', key='add_genre')
        read_status = st.selectbox('Read Status', ['True', 'False'], key='add_status')

    if st.button('Save Book', type='primary'):
        global books
        new_book = pd.DataFrame([{
            'Title': title,
            'Author': author,
            'Publication Year': publication_year,
            'Genre': genre,
            'Read Status': read_status
        }])
        books = pd.concat([books, new_book], ignore_index=True)
        books.to_csv('library.csv', index=False)
        st.success(f"Book: '{title}' successfully added")

# Main interface
st.title("📚 Library Management System")

# Create a sidebar for navigation
st.sidebar.title("Navigation")
choice = st.sidebar.radio("Select an option:", 
    ["Add a Book", "Remove a Book", "Display all Books", "Search for a Book", "Display Statistics"])

# Display the selected function
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
