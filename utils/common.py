import pandas

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

def save_books(df, filename):
    """
    Save books to an Excel file.
    
    Args:
        df (pandas.DataFrame): The DataFrame containing the book data.
        filename (str): The path to the Excel file.
    """
    try:
        df.to_excel(filename, index=False)
    except Exception as e:
        print(f"Error saving file: {e}")

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