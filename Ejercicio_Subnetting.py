import openai
from chatgpt import ChatConversation
import streamlit as st
from streamlit_chat import message

st.set_page_config(layout="wide")

with st.sidebar:
    openai_api_key = st.text_input('OpenAI API Key',key='chatbot_api_key')
    "[Información sobre el proyecto](https://www.upv.es)"
#    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

#openai_api_key = st.secrets.OPENAI_API_KEY # No puede ir al principio

st.title("Tutor Socrático 💬")
col1, col2 = st.columns([0.4,0.6]) # Dividir la pantalla en dos columnas

with col1: # Columna de la izquierda
   st.subheader("Ejercicio 1")
   st.write('¿Cuantos bits ha de tener el campo de host de una dirección IP para poder contener 4 direcciones de host?')
   #user_input = st.text_area('Inserta tu respuesta aquí:', height=100)
   user_input = st.number_input('tu respuesta:', min_value=0, step=1, format="%i")

   if st.button('Corregir'):
      if user_input == 3:
         st.success('Respuesta correcta.') 
         st.session_state.messages.append({"role": "assistant", "content": "¡Felicidades! Has acertado."})
         #message("¡Felicidades! Has acertado.") 
      else:
         st.error('La respuesta no es correcta.')
         st.session_state.messages.append({"role": "system", "content": f"el usuario a contestado {user_input}"})
         response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
         msg = response.choices[0].message
         st.session_state.messages.append(msg)
         #message(msg.content)
    
with col2: # Columna de la derecha
   if "messages" not in st.session_state:
      st.session_state["messages"] = [
         {"role": "user", "content": "Eres un tutor socrático. Es decir has de ayudar al alunos a reflexionar pero nunca darle la respuesta. "+
               "La pregunta es: ¿Cuantos bits ha de tener el campo de host de una dirección IP para poder contener 4 direcciones de host?"+
               "Un error frecuente es no recordar que en el campo de host hay que reservar la dirección de red y la dirección de broadcast."},
         {"role": "assistant", "content": "¡Hola! Soy tu profe particular. ¿Cómo puedo ayudarte?"}]

   with st.form("chat_input", clear_on_submit=True):
      a, b = st.columns([4, 1])
      user_input = a.text_input(
         label="Your message:",
         placeholder="Escribe aqui tus preguntas.",
         label_visibility="collapsed",
      )
      b.form_submit_button("Enviar", use_container_width=True)

   if user_input and not openai_api_key:
            st.info("Has de introducir un API key de OpenAI para continuar.")
    
   if user_input and openai_api_key:
      openai.api_key = openai_api_key
      st.session_state.messages.append({"role": "user", "content": user_input})
      #message(user_input, is_user=True)
      #response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
      #msg = response.choices[0].message

      chat = ChatConversation(api_key=openai_api_key)#   system_prompt="Eres un tutor socrático. Es decir has de ayudar al alumnos a reflexionar pero nunca darle la respuesta.")
      msg = chat.send_message(user_input)

      st.session_state.messages.append(msg)
      #message(msg.content)

   for msg in reversed(st.session_state.messages):
      if msg["role"] != "system":
         message(msg["content"], is_user=msg["role"] == "user")
