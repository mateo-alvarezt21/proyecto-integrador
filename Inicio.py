import streamlit as st
from PIL import Image

st.set_page_config(layout="wide", page_title="Virtual Coach: League of Legends", page_icon="🎮")


# Título y subtítulo
st.title("Virtual Coach: Los Vagabundos")
st.subheader("Mejora tus habilidades con un entrenador virtual impulsado por Gemini")

# Imagen de fondo
image = Image.open("./static/Los Vagabundos.png") 
st.image(image, use_column_width=True)

# Integrantes
st.header("Nuestro Equipo")
st.write("*Roles y responsabilidades dentro del proyecto:*")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("./static/SAMUEL ROJAS HURTADO.jpg", width=150)  # Tamaño estandarizado
    st.write("*Samuel Rojas*")
    st.write("Backend Developer")
    st.write("Desarrolla la lógica del sistema y la integración con Gemini.")


with col2:
    st.image("./static/Mateo.jpg", width=200)  # Tamaño estandarizado
    st.write("*Mateo Alvarez*")
    st.write("Project Manager")
    st.write("Coordina el equipo y asegura el cumplimiento de los objetivos.")

with col3:
    st.image("./static/Johana.png", width=200)  # Tamaño estandarizado
    st.write("*Johana Gómez*")
    st.write("UI/UX Designer")
    st.write("Diseña la interfaz y experiencia del usuario del entrenador virtual.")

col4, col5 = st.columns(2)

with col4:
    st.image("./static/Alexander.png", width=200)  # Tamaño estandarizado
    st.write("*Alexander Rubiano*")
    st.write("Frontend Developer")
    st.write("Implementa las vistas y funcionalidad de la aplicación.")

with col5:
    st.image("./static/Angello.png", width=200)  # Tamaño estandarizado
    st.write("*Angello Gomez*")
    st.write("Machine Learning Specialist")
    st.write("Optimiza el modelo de ChatGPT para ofrecer respuestas personalizadas.")


# Descripción del proyecto
st.header("Sobre el Proyecto")
st.write("""
*Virtual Coach* es una aplicación diseñada para jugadores de *League of Legends* que busca mejorar su rendimiento a través de un entrenador virtual. Este sistema utiliza la tecnología de *Gemini* para proporcionar recomendaciones personalizadas, análisis de jugadas, y estrategias adaptadas al estilo de juego del usuario. 
El proyecto busca resolver la problemática de falta de guías accesibles y prácticas para los jugadores que desean mejorar en este juego competitivo.
""")

# Más información
st.header("Más Información")
st.write("""
### Tecnologías Utilizadas:
- *Frontend:* Streamlit para la interfaz web.
- *Backend:* Python y Gemini para la generación de contenido y análisis.
- *Diseño:* Figma para prototipos y diseño de interfaz.

### Resultados Esperados:
- Una herramienta funcional que permita a los jugadores recibir asesoramiento personalizado.
- Incremento en las habilidades de los usuarios con métricas demostrables.
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