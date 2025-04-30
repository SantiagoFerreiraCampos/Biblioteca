
import streamlit as st
import pandas as pd

df = pd.read_excel("Biblioteca_cleaned.xlsx")
# Title
st.title("My Personal Library")

# Search bar
search = st.text_input("Search for a book, author, or publisher")

# Filter results
if search:
    filtered_df = df[
        df["Titulo"].str.contains(search, case=False, na=False) |
        df["Autor"].str.contains(search, case=False, na=False) |
        df["Editorial"].str.contains(search, case=False, na=False)
    ]
    st.write(filtered_df)
else:
    st.write(df)