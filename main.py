import streamlit as st
from groq import Groq

st.set_page_config(page_title="Mi Chat de IA")

st.title("Chatbot")

nombre = st.text_input("¿Cuál es tu nombre?")

if st.button("Saludar"):
    st.write(f"Hola, {nombre}! Gracias por ingresar a nuestro ChatBot.")

MODELO = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

def crear_usuario_groq():
    clave = st.secrets["CLAVE_API"]
    return Groq(api_key = clave)

def configurar_modelo(cliente, modelo, mensajeEntrada):
    return cliente.chat.completions.create(
        model = modelo,
        messages = [{"role":"user", "content":mensajeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    #append() agrega elementos a la lista
    st.session_state.mensajes.append(
        {"role": rol, "content": contenido, "avatar": avatar}
    )

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]): 
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat : mostrar_historial()

def configurarPagina():
    st.sidebar.title("Configuración")
    seleccion = st.sidebar.selectbox(
        "Elegí un modelo",
        MODELO,
        index = 0
    )

    return seleccion

def generarRespuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
            
    return respuesta_completa

def main():
    modelo = configurarPagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat()
    mensaje = st.chat_input("Aca es donde comienza una épica historia!")

    if mensaje:
        actualizar_historial("user", mensaje, "✨")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generarRespuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "⚙")
                st.rerun()

if __name__ == "__main__":
    main()

#10%3 te da 1 (te da el resto de la division)