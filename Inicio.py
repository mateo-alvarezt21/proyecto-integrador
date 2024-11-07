import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Mapping Demo", page_icon="🌍")


# Título y subtítulo
st.title("Proyecto Integrador: Los Vagabundos")
st.subheader("Un Viaje Creativo con Los Vagabundos")

# Imagen de fondo
image = Image.open("./static/Los Vagabundos.png") 
st.image(image, width=700, use_column_width=True)  

# Integrantes
st.header("Nuestro Equipo")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("./static/SAMUEL ROJAS HURTADO.jpg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Samuel Rojas**")
    st.write("Descansar los ojos")

with col2:
    st.image("./static/Mateo.jpg", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Mateo Alvarez**")
    st.write("Dormir")

with col3:
    st.image("./static/Johana.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Johana**")
    st.write("No Ir a Clase")

col4, col5, = st.columns(2)

with col4:
    st.image("./static/Alexander.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Alexander Rubiano**")
    st.write("No Hacer Nada")

with col5:
    st.image("./static/Angello.png", width=200)  # Reemplaza con la ruta de la foto
    st.write("**Angello Gomez**")
    st.write("No Ayudar")


# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
[Escribe aquí una breve descripción del proyecto, incluyendo el objetivo principal, la problemática que aborda y el enfoque que se utiliza. Puedes ser creativo y usar un lenguaje atractivo.]
""")

# Más información
st.header("Más Información")

# Puedes añadir secciones como:
# - Tecnología utilizada
# - Resultados esperados
# - Presentación de resultados (fecha y formato)
# - Contacto para preguntas

st.write("""
[Agrega la información adicional que consideres relevante.]
""")

# Footer con links
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px;">
        <a href="https://www.google.com">Google</a> |
        <a href="https://www.facebook.com">Facebook</a> |
        <a href="https://www.linkedin.com">LinkedIn</a>
    </div>
    """,
    unsafe_allow_html=True,
)