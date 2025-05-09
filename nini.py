import streamlit as st
import pandas as pd
from utils.common import load_books, save_books, search_books, edit_book, remove_book, wishlist_to_library

# Define file paths
FILENAME = "data/nini/Biblioteca.xlsx"
WISHLIST_FILENAME = "data/nini/Wishlist.xlsx"
USER = "Nini"
 

def biblioteca():
    st.subheader("Biblioteca de Nini")
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
            if titulo:
                new_row = pd.DataFrame([{
                    "Titulo": titulo,
                    "Autor": autor,
                    "Editorial": editorial
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                save_books(df, FILENAME, commit_message)
                st.success("Libro añadido exitosamente!")
            else:
                st.error("Por favor, completa el campo del título.")
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
def wishlist():
    st.header("Lista de deseos")
    
    # Wishlist functionality
    
    wishlist_df = load_books(WISHLIST_FILENAME)
    if wishlist_df is None or wishlist_df.empty:
        wishlist_df = pd.DataFrame(columns=["Titulo", "Autor", "Editorial"])
    # Display wishlist
    if not wishlist_df.empty:
        st.write("Tu lista de deseos:")
        st.dataframe(wishlist_df)
    else:
        st.info("Tu lista de deseos está vacía.")
    with st.form("wishlist_form"):
        st.write("Añade libros a tu lista de deseos:")
        wishlist_titulo = st.text_input("Título del libro", key="wishlist_title")
        wishlist_autor = st.text_input("Autor del libro", key="wishlist_author")
        wishlist_editorial = st.text_input("Editorial del libro", key="wishlist_editorial")
        add_to_wishlist = st.form_submit_button("Añadir a la lista de deseos")
        if add_to_wishlist:
            if wishlist_titulo:
                new_wishlist_entry = pd.DataFrame([{
                    "Titulo": wishlist_titulo,
                    "Autor": wishlist_autor,
                    "Editorial": wishlist_editorial
                }])
                wishlist_df = pd.concat([wishlist_df, new_wishlist_entry], ignore_index=True)
                commit_message: f"Added book to wishlist: {wishlist_titulo} in {USER}'s wishlist"
                save_books(wishlist_df, WISHLIST_FILENAME, "Added book to wishlist")
                st.success(f"'{wishlist_titulo}' añadido a la lista de deseos!")
            else:
                st.error("El título del libro es obligatorio para añadirlo a la lista de deseos.")
    # Edit and Remove from Wishlist
    st.subheader("Editar o eliminar de la lista de deseos")
    if not wishlist_df.empty:
        wishlist_titles = wishlist_df["Titulo"].tolist()
        selected_wishlist_book = st.selectbox("Selecciona un libro de la lista de deseos para editar o eliminar", [""] + wishlist_titles)
        
        if selected_wishlist_book:
            wishlist_index = wishlist_df[wishlist_df["Titulo"] == selected_wishlist_book].index[0]
            
            # Edit book details
            with st.form(f"edit_wishlist_form_{wishlist_index}"):
                st.write("Edita los detalles del libro:")
                new_wishlist_titulo = st.text_input("Título", value=wishlist_df.loc[wishlist_index, "Titulo"])
                new_wishlist_autor = st.text_input("Autor", value=wishlist_df.loc[wishlist_index, "Autor"])
                new_wishlist_editorial = st.text_input("Editorial", value=wishlist_df.loc[wishlist_index, "Editorial"])
                update_wishlist = st.form_submit_button("Actualizar libro")
                
                if update_wishlist:
                    wishlist_df = edit_book(wishlist_df, wishlist_index, new_wishlist_titulo, new_wishlist_autor, new_wishlist_editorial, WISHLIST_FILENAME, "Updated book in wishlist")
                    st.success("Libro en la lista de deseos actualizado exitosamente!")
                    
            # Initialize session state for deletion
            if "delete_confirmation" not in st.session_state:
                st.session_state["delete_confirmation"] = {}

            # Remove book from wishlist
            if st.button("Eliminar de la lista de deseos", key=f"delete_wishlist_{wishlist_index}"):
                st.session_state["delete_confirmation"][wishlist_index] = True

            if st.session_state["delete_confirmation"].get(wishlist_index):
                st.warning(
                    f"Estás segura que quieres eliminar el libro '{wishlist_df.loc[wishlist_index, 'Titulo']}' "
                    f"del autor '{wishlist_df.loc[wishlist_index, 'Autor']}' de la editorial '{wishlist_df.loc[wishlist_index, 'Editorial']}'?"
                )
                if st.button("Confirmar eliminación", key=f"confirm_delete_wishlist_{wishlist_index}"):
                    commit_message = f"Deleted book: {wishlist_df.loc[wishlist_index, 'Titulo']} from {USER}'s wishlist"
                    wishlist_df, book_title = remove_book(wishlist_df, wishlist_index, WISHLIST_FILENAME, commit_message)
                    st.success(f"Libro '{book_title}' eliminado de la lista de deseos exitosamente!")
                    del st.session_state["delete_confirmation"][wishlist_index]  # Reset the confirmation state
    else:
        st.info("No hay libros en la lista de deseos.")
    #add book from wishlist to library using the wishlist_to_library function
    st.subheader("Añadir libro de la lista de deseos a la biblioteca")
    
    if not wishlist_df.empty:
        selected_book_to_library = st.selectbox("Selecciona un libro para mover a la biblioteca", [""] + wishlist_titles)
        if selected_book_to_library:
            library_action = st.button("Mover a la biblioteca")
            if library_action:
                wishlist_index = wishlist_df[wishlist_df["Titulo"] == selected_book_to_library].index[0]
                commit_message = f"Moved book '{selected_book_to_library}' from wishlist to biblioteca"
                wishlist_to_library(USER.lower(), wishlist_index, commit_message)
                st.success(f"'{selected_book_to_library}' se ha movido a la biblioteca exitosamente!")

    
    
           

def estadisticas():
    st.header("Estadísticas de la biblioteca")
    df = load_books(FILENAME)

    if df is None or df.empty:
        st.warning("No hay libros en la biblioteca.")
        return

    # Display total number of books
    total_books = len(df)
    st.write(f"Total de libros en la biblioteca: {total_books}")

    # Display top authors
    top_authors = df["Autor"].value_counts().head(10)
    st.subheader("Top 10 Autores")
    st.bar_chart(top_authors)

    # Display top editorials
    top_editorials = df["Editorial"].value_counts().head(10)
    st.subheader("Top 10 Editoriales")
    st.bar_chart(top_editorials)
    