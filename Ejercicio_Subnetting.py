from openai import OpenAI
import streamlit as st
from Ejercicio import Ejercicio, cargar_de_fichero

#nombre_archivo = './ejercicios/isla_mentirosos.txt'  # Asegúrate de que el archivo exista en esta ruta
nombre_archivo = './ejercicios/circuito_1.txt' 
ejercicio = cargar_de_fichero(nombre_archivo)
if "messages" not in st.session_state:
   st.session_state.messages = []
   st.session_state.messages.append({"role": "system", "content": f"{ejercicio.prompt_tutor()}'"})
   st.session_state.messages.append({"role": "assistant", "content": "¿Alguna duda con el ejercicio?"})
   

st.set_page_config(layout="wide")
with st.sidebar:
   openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
   #añado variable binaria con un checkbox
   st.checkbox("Mostrar prompts del sistema", key="show_system_prompts")
   "[Información sobre el proyecto](https://www.upv.es)"

if not st.session_state.get("chatbot_api_key"):
   openai_api_key = st.secrets.OPENAI_API_KEY # No puede ir al principio

#st.title("Tutor Socrático 💬")
col1, col2 = st.columns([0.5,0.5]) # Dividir la pantalla en dos columnas

with col1: # Columna de la izquierda
   st.subheader(ejercicio.titulo)
   #st.write(f"{ejercicio.enunciado}")
   st.markdown(ejercicio.enunciado, unsafe_allow_html=True)
   user_input = st.text_area('tu respuesta:', height=100)

   if st.button('Corregir'):
      st.session_state.messages.append({"role": "system", "content": f"el usuario a contestado: '{user_input}'"})
      LLM_response = ejercicio.corregir(user_input)
      if LLM_response['correcta']:
         st.success('Respuesta correcta.') 
         st.session_state.messages.append({"role": "assistant", "content": "¡Felicidades! Has acertado."})
      else:
         st.error('La respuesta no es correcta.')
         st.write(f"Error conceptual: {LLM_response['error_conceptual']}")
         st.write(f"Pregunta Socrática: {LLM_response['pregunta_socratica']}")
         st.session_state.messages.append({"role": "assistant", "content": LLM_response['pregunta_socratica']})
    
with col2: # Columna de la derecha
   st.subheader("Tutor Socrático 💬")
   with st.container():
        for msg in st.session_state.messages:
            # si el rol no es system, mostrar el mensaje
            if msg["role"] != "system" or st.session_state.get("show_system_prompts"):
               st.chat_message(msg["role"]).write(msg["content"])
        # Añadir un contenedor vacío para asegurar que el scroll siempre esté visible en lo último
        st.write("")  
   
   if prompt := st.chat_input():
      if not openai_api_key:
         st.info("Por favor, añade tu clave API de OpenAI para continuar.")
         st.stop()

      client = OpenAI(api_key=openai_api_key)
      st.session_state.messages.append({"role": "user", "content": prompt})
      #st.chat_message("user").write(prompt)
      response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
      msg = response.choices[0].message.content
      st.session_state.messages.append({"role": "assistant", "content": msg})
      #st.chat_message("assistant").write(msg)
      st.experimental_rerun()
