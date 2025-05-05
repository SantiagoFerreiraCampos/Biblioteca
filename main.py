import streamlit as st
import santi as santi
import nini as nini

# Load user credentials from secrets
USER_CREDENTIALS = st.secrets["users"]

# Initialize session state for authentication
if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None

# Authentication Function
def authenticate_user(selected_option, password):
    """
    Authenticate the user based on the selected option and password.
    """
    return USER_CREDENTIALS.get(selected_option.lower()) == password

# Main App
st.title("Biblioteca Virtual")

# If no authenticated user, show library selection
if st.session_state["authenticated_user"] is None:
    
    option = st.selectbox("Selecciona tu biblioteca:", ["Biblioteca de Nini", "Biblioteca de Santi"])

    # Extract user from selection
    selected_user = option.split()[-1].lower()  # 'Santi' or 'Nini'

    # Prompt for password
    password = st.text_input(f"Introduce la contraseña para {option}:", type="password")
    if st.button("Ingresar"):
        if authenticate_user(selected_user, password):
            st.session_state["authenticated_user"] = selected_user
            st.success(f"¡Bienvenida a la {option}!")
            st.session_state["authenticated_library"] = option 
            st.rerun() 
        else:
            st.error("¡Contraseña incorrecta! Inténtalo de nuevo.")

# Authenticated User Section
if st.session_state["authenticated_user"] is not None:
    authenticated_user = st.session_state["authenticated_user"]
    library_name = st.session_state.get("authenticated_library", f"Biblioteca de {authenticated_user.capitalize()}")

    st.sidebar.title(library_name)
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["authenticated_user"] = None  # Clear session state to log out
        st.session_state["authenticated_library"] = None

    # Load the respective module based on the user
    if authenticated_user == "santi":
        santi.show()
    elif authenticated_user == "nini":
        nini.show()