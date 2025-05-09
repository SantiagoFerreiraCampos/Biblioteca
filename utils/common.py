import pandas
import streamlit as st
import pandas as pd
from github import Github

def load_books(filename):
    """
    Load books from an Excel file.
    
    Args:
        filename (str): The path to the Excel file.
        
    Returns:
        pandas.DataFrame: A DataFrame containing the book data.
    """
    try:
        df = pandas.read_excel(filename)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def search_books(df, search_term):
    """
    Search for books in the DataFrame.
    
    Args:
        df (pandas.DataFrame): The DataFrame containing the book data.
        search_term (str): The term to search for.
        
    Returns:
        pandas.DataFrame: A DataFrame containing the filtered book data.
    """
    if search_term:
        filtered_df = df[
            df["Titulo"].str.contains(search_term, case=False, na=False) |
            df["Autor"].str.contains(search_term, case=False, na=False) |
            df["Editorial"].str.contains(search_term, case=False, na=False)
        ]
        return filtered_df
    return df


def push_to_github(filename,commit_message):
    """
    Push the updated file to GitHub.

    Args:
        filename (str): The path to the file to be pushed.

    """
    # Retrieve secrets
    GITHUB_TOKEN = st.secrets["token"]
    REPO_NAME = "SantiagoFerreiraCampos/Biblioteca"
    FILE_PATH = filename
    COMMIT_MESSAGE = commit_message

    # Authenticate with GitHub
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Read the updated file
    with open(filename, "rb") as file:
        content = file.read()

    # Check if the file already exists on GitHub
    try:
        file_on_github = repo.get_contents(FILE_PATH)
        # Update existing file
        repo.update_file(FILE_PATH, COMMIT_MESSAGE, content, file_on_github.sha)
    except Exception as e:
        # If file doesn't exist, create a new one
        repo.create_file(FILE_PATH, COMMIT_MESSAGE, content)

def save_books(df, filename, commit_message):
    """
    Save books to an Excel file.
    
    Args:
        df (pandas.DataFrame): The DataFrame containing the book data.
        filename (str): The path to the Excel file.
    """
    try:
        # Save locally
        df.to_excel(filename, index=False)

        # Push to GitHub
        push_to_github(filename,commit_message)
    except Exception as e:
        print(f"Error saving file: {e}")

def edit_book(df, book_index, new_title, new_author, new_editorial, filename, commit_message):
    """
    Edit the details of a book in the DataFrame and save changes.

    Args:
        df (pd.DataFrame): DataFrame containing books.
        book_index (int): Index of the book to edit.
        new_title (str): New title of the book.
        new_author (str): New author of the book.
        new_editorial (str): New editorial of the book.
        filename (str): Path to the Excel file.
        commit_message (str): Commit message for the update.
    """
    df.loc[book_index, "Titulo"] = new_title
    df.loc[book_index, "Autor"] = new_author
    df.loc[book_index, "Editorial"] = new_editorial
    save_books(df, filename, commit_message)
    return df

def remove_book(df, book_index, filename, commit_message):
    """
    Remove a book from the DataFrame and save changes.

    Args:
        df (pd.DataFrame): DataFrame containing books.
        book_index (int): Index of the book to remove.
        filename (str): Path to the Excel file.
        commit_message (str): Commit message for the removal.
    """
    book_title = df.loc[book_index, "Titulo"]
    df = df.drop(index=book_index).reset_index(drop=True)
    save_books(df, filename, commit_message)
    return df, book_title

def wishlist_to_library(user, book_index, commit_message):
    """
    Move a book from the wishlist to the biblioteca for a specific user.
    
    Args:
        user (str): The username or directory identifier for the user's data.
        book_index (int): Index of the book to move from the wishlist.
        commit_message (str): Commit message for the update.
        
    """
    try:
        # Load the user's wishlist and biblioteca
        wishlist_filename = f"data/{user}/Wishlist.xlsx"
        biblioteca_filename = f"data/{user}/Biblioteca.xlsx"
        wishlist_df = load_books(wishlist_filename)
        biblioteca_df = load_books(biblioteca_filename)
        
        if wishlist_df is None or biblioteca_df is None:
            print("Error: Failed to load data.")
            

        # Get the book details from the wishlist
        book_to_move = wishlist_df.iloc[book_index]
    
        # Add the book to biblioteca
        new_entry = pd.DataFrame([book_to_move])
        biblioteca_df = pd.concat([biblioteca_df, new_entry], ignore_index=True)
        
        # Remove the book from wishlist
        wishlist_df = wishlist_df.drop(book_index).reset_index(drop=True)
        
        # Save both DataFrames
        save_books(biblioteca_df, f"data/{user}/Biblioteca.xlsx", commit_message)
        save_books(wishlist_df, f"data/{user}/Wishlist.xlsx", commit_message)
        
        
    except Exception as e:
        print(f"Error transferring book from wishlist to biblioteca: {e}")
        return None, None
    


    
