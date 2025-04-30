import streamlit as st
from utils.common import load_books, save_books, search_books

# Define file path for Santiago's books
FILENAME = "data/santi_books.xlsx"

def show():
    st.header("Biblioteca de Santi")
    df = load_books(FILENAME)

    if df is None:
        st.warning("No se pudo cargar el archivo de libros.")
        return

    # Search functionality
    search_term = st.text_input("Buscar libros por Título, Autor o Editorial:")
    filtered_df = search_books(df, search_term)
    st.write("Resultados de la búsqueda:")
    st.dataframe(filtered_df)

    # Add a new book
    with st.form("add_book_form"):
        st.subheader("Añadir un libro nuevo")
        titulo = st.text_input("Título")
        autor = st.text_input("Autor")
        editorial = st.text_input("Editorial")
        submit = st.form_submit_button("Añadir libro")
        
        if submit:
            if titulo and autor and editorial:
                new_row = {"Titulo": titulo, "Autor": autor, "Editorial": editorial}
                df = df.append(new_row, ignore_index=True)
                save_books(df, FILENAME)
                st.success("Libro añadido exitosamente!")
            else:
                st.error("Por favor, completa todos los campos.")

    # Display all books
    st.write("Tu biblioteca completa:")
    st.dataframe(df)