import streamlit as st
import pandas as pd
from utils.common import load_books, save_books, search_books, edit_book, remove_book

# Define file path for Nini's books
FILENAME = "data/Biblioteca_nini.xlsx"
USER = "Nini"

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
        commit_message = f"Added new book: {titulo} by {autor} in {USER}'s library"
        if submit:
            if titulo and autor and editorial:
                new_row = pd.DataFrame([{
                "Titulo": titulo, 
                "Autor": autor, 
                "Editorial": editorial
            }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_books(df, FILENAME, commit_message)
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
                commit_message = f"Updated book: {new_titulo} by {new_autor} in {USER}'s library"
                
                if update:
                    df = edit_book(df, book_index, new_titulo, new_autor, new_editorial, FILENAME, commit_message)
                    st.success("Libro actualizado exitosamente!")
                    
            # Initialize session state for deletion
            if "delete_confirmation" not in st.session_state:
                st.session_state["delete_confirmation"] = {}

            # Remove book
            if st.button("Eliminar libro", key=f"delete_book_{book_index}"):
                st.session_state["delete_confirmation"][book_index] = True

            if st.session_state["delete_confirmation"].get(book_index):
                st.warning(
                    f"Estás segura que quieres eliminar el libro '{df.loc[book_index, 'Titulo']}' "
                    f"del autor '{df.loc[book_index, 'Autor']}' de la editorial '{df.loc[book_index, 'Editorial']}'?"
                )
                if st.button("Confirmar eliminación", key=f"confirm_delete_{book_index}"):
                    commit_message = f"Deleted book: {df.loc[book_index, 'Titulo']} from {USER}'s library"
                    df, book_title = remove_book(df, book_index, FILENAME, commit_message)
                    st.success(f"Libro '{book_title}' eliminado exitosamente!")
                    del st.session_state["delete_confirmation"][book_index]  # Reset the confirmation state

                
    else:
        st.info("No hay libros en la biblioteca.")

