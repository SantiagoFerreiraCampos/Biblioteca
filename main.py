import streamlit as st
import santi as santi
import nini as nini

st.title("Biblioteca Virtual")

option = st.selectbox("Selecciona tu biblioteca:", ["Biblioteca de Santi", "Biblioteca de Nini"])

if option == "Biblioteca de Santi":
    santi.show()
elif option == "Biblioteca de Nini":
    nini.show()