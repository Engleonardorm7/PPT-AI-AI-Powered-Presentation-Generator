import streamlit as st

# Configuración básica de la página
st.set_page_config(page_title="Chatbot", layout="centered")

# Título y descripción
st.title("Chatbot")
st.write("Graphical user unterface")

# Sección para almacenar los mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para enviar el mensaje y almacenarlo en el historial
def send_message():
    if st.session_state.user_input:
        st.session_state.messages.append(("Usuario", st.session_state.user_input))
        # Aquí es donde se llamaría a la función del chatbot para generar respuesta
        # Por ejemplo, podría ser algo como: bot_response = chatbot_response(st.session_state.user_input)
        # Pero para la interfaz, dejaremos una respuesta de prueba
        bot_response = "This is a sample answer."
        st.session_state.messages.append(("Chatbot", bot_response))
        st.session_state.user_input = ""  # Limpiar el input después de enviar

# Mostrar el historial de mensajes
st.write("## Chat")
for sender, message in st.session_state.messages:
    if sender == "Usuario":
        st.markdown(f"**{sender}:** {message}")
    else:
        st.markdown(f"**{sender}:** {message}")

# Barra de entrada para el usuario
st.text_input("Type...:", key="user_input", on_change=send_message)
