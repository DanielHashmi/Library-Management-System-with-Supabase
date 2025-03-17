import streamlit as st
from supabase import create_client
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Library Management System", page_icon="📚", layout="wide")
load_dotenv()

@st.cache_resource
def get_supabase_client():
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase_client = get_supabase_client()

def add_a_book():
    st.header('💾 Add a Book')
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input('Title')
        author = st.text_input('Author')
        publication_year = st.text_input('Publication Year')
    with col2:
        genre = st.text_input('Genre')
        read_status = st.selectbox('Read Status', [True, False])
    if st.button('Save Book'):
        new_book = {
            "Title": title,
            "Author": author,
            "Publication_Year": publication_year,
            "Genre": genre,
            "Read_Status": read_status
        }
        response = supabase_client.table("books").insert(new_book).execute()
        if response.data:
            st.success(f"Book: '{title}' successfully added")
        else:
            st.error("Failed to add book.")

def remove_a_book():
    st.header('🗑️ Remove a Book')
    title = st.text_input('Title to remove')
    if st.button('Remove Book'):
        response = supabase_client.table("books").delete().eq("Title", title).execute()
        if response.data:
            st.success(f"Book: '{title}' successfully deleted")
        else:
            st.warning(f"Book: '{title}' not found")

def display_all_books():
    st.header('📕 All Books')
    response = supabase_client.table("books").select("*").execute()
    books = response.data
    if books:
        st.dataframe(books, use_container_width=True)
    else:
        st.info("No books available.")

def search_for_a_book():
    st.header('📖 Search for a Book')
    search_by = st.selectbox('Search by', ['Title', 'Author', 'Genre', 'Read_Status'])
    search_term = st.text_input('Enter a search term')
    if search_term:
        if search_by == "Read_Status":
            search_value = search_term.lower() in ['true', '1', 'yes']
            response = supabase_client.table("books").select("*").eq("Read_Status", search_value).execute()
        else:
            response = supabase_client.table("books").select("*").ilike(search_by, f"%{search_term}%").execute()
        search_results = response.data
        if search_results:
            st.dataframe(search_results, use_container_width=True)
        else:
            st.info("No matching books found.")

def display_statistics():
    st.header('📊 Library Statistics')
    response_all = supabase_client.table("books").select("id", count="exact").execute()
    total_books = response_all.count if response_all.count is not None else len(response_all.data or [])
    response_read = supabase_client.table("books").select("id", count="exact").eq("Read_Status", True).execute()
    read_books = response_read.count if response_read.count is not None else len(response_read.data or [])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Read Books Percentage", f"{read_percentage:.1f}%")

st.sidebar.title("Navigation")
pages = {
    "Add a Book": add_a_book,
    "Remove a Book": remove_a_book,
    "Display all Books": display_all_books,
    "Search for a Book": search_for_a_book,
    "Display Statistics": display_statistics
}

choice = st.sidebar.radio("Select an option:", list(pages.keys()))
pages[choice]()
