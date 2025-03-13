import streamlit as st
import pandas as pd
import os

# File to store library data
LIBRARY_FILE = "library.txt"

# Initialize session state for the library
if 'library' not in st.session_state:
    if os.path.exists(LIBRARY_FILE):
        st.session_state.library = pd.read_csv(LIBRARY_FILE)
    else:
        st.session_state.library = pd.DataFrame(columns=["Title", "Author", "Publication Year", "Genre", "Read Status"])

# Function to save library to file
def save_library():
    st.session_state.library.to_csv(LIBRARY_FILE, index=False)

# Function to add a book
def add_book(title, author, year, genre, read_status):
    new_book = pd.DataFrame([[title, author, year, genre, read_status]],
                            columns=["Title", "Author", "Publication Year", "Genre", "Read Status"])
    st.session_state.library = pd.concat([st.session_state.library, new_book], ignore_index=True)
    save_library()
    st.success("Book added successfully!")

# Function to remove a book
def remove_book(title):
    if title in st.session_state.library["Title"].values:
        st.session_state.library = st.session_state.library[st.session_state.library["Title"] != title]
        save_library()
        st.success(f"Book '{title}' removed successfully!")
    else:
        st.error(f"Book '{title}' not found in the library.")

# Function to search for a book
def search_book(query):
    results = st.session_state.library[
        (st.session_state.library["Title"].str.contains(query, case=False)) |
        (st.session_state.library["Author"].str.contains(query, case=False))
    ]
    return results

# Function to display statistics
def display_statistics():
    total_books = len(st.session_state.library)
    read_books = st.session_state.library["Read Status"].sum()
    percentage_read = (read_books / total_books * 100) if total_books > 0 else 0
    st.write(f"**Total Books:** {total_books}")
    st.write(f"**Percentage Read:** {percentage_read:.2f}%")

# Streamlit App
st.set_page_config(page_title="Personal Library Manager", page_icon="📚", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stTextInput input {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .stSelectbox select {
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📚 Personal Library Manager")

# Menu System
menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"])

if menu == "Add a Book":
    st.header("Add a Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1800, max_value=2100, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Read Status (Checked if read)")
    if st.button("Add Book"):
        if title and author and year and genre:
            add_book(title, author, year, genre, read_status)
        else:
            st.error("Please fill in all fields.")

elif menu == "Remove a Book":
    st.header("Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if title:
            remove_book(title)
        else:
            st.error("Please enter a title.")

elif menu == "Search for a Book":
    st.header("Search for a Book")
    query = st.text_input("Enter title or author to search")
    if query:
        results = search_book(query)
        if not results.empty:
            st.write("Search Results:")
            st.dataframe(results)
        else:
            st.warning("No matching books found.")

elif menu == "Display All Books":
    st.header("All Books in Library")
    if not st.session_state.library.empty:
        st.dataframe(st.session_state.library)
    else:
        st.warning("The library is empty.")

elif menu == "Display Statistics":
    st.header("Library Statistics")
    display_statistics()

elif menu == "Exit":
    st.header("Exiting the Program")
    st.write("Thank you for using the Personal Library Manager!")
    save_library()
    st.stop()