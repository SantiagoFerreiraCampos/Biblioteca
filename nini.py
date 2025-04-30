import streamlit as st
import pandas as pd
from utils.common import load_books, save_books, search_books

# Define file path for Santiago's books
FILENAME = "data/Biblioteca_cleaned.xlsx"

def show():
    st.header("Biblioteca de Nini")
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
                new_row = pd.DataFrame([{
                "Titulo": titulo, 
                "Autor": autor, 
                "Editorial": editorial
            }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_books(df, FILENAME)
                st.success("Libro añadido exitosamente!")
            else:
                st.error("Por favor, completa todos los campos.")
                
    # Edit and Remove Books
    st.subheader("Editar o eliminar libros")
    if not df.empty:
        book_titles = df["Titulo"].tolist()
        selected_book = st.selectbox("Selecciona un libro para editar o eliminar", [""] + book_titles)
        
        if selected_book:
            book_index = df[df["Titulo"] == selected_book].index[0]
            
            # Edit book details
            with st.form(f"edit_book_form_{book_index}"):
                st.write("Edita los detalles del libro:")
                new_titulo = st.text_input("Título", value=df.loc[book_index, "Titulo"])
                new_autor = st.text_input("Autor", value=df.loc[book_index, "Autor"])
                new_editorial = st.text_input("Editorial", value=df.loc[book_index, "Editorial"])
                update = st.form_submit_button("Actualizar libro")
                
                if update:
                    df.loc[book_index, "Titulo"] = new_titulo
                    df.loc[book_index, "Autor"] = new_autor
                    df.loc[book_index, "Editorial"] = new_editorial
                    save_books(df, FILENAME)
                    st.success("Libro actualizado exitosamente!")
                    
            
            # Remove book
            if st.button("Eliminar libro", key=f"delete_book_{book_index}"):
                df = df.drop(index=book_index).reset_index(drop=True)
                save_books(df, FILENAME)
                st.success("Libro eliminado exitosamente!")
                
    else:
        st.info("No hay libros en la biblioteca.")

