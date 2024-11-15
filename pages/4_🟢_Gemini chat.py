import streamlit as st
import google.generativeai as genai

# Obtener la API key desde secrets.toml
api_key = st.secrets["GEMINI_AI_CREDENTIALS"]["private_key_id"]
genai.configure(api_key=api_key)

st.title("Coach de League of Legends")

initial_context = (
    "Imagina que eres un coach profesional de League of Legends. "
    "Responde las preguntas como un experto en el juego, "
    "proporcionando estrategias, consejos para mejorar, y análisis de partidas."
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu pregunta sobre League of Legends..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    full_prompt = f"{initial_context}\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    response = model.generate_content(full_prompt)

    bot_response = response.text

    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Mostrar la respuesta del bot en la interfaz
    with st.chat_message("assistant"):
        st.markdown(bot_response)
