from openai import OpenAI
import streamlit as st

st.set_page_config(layout="wide")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Información sobre el proyecto](https://www.upv.es)"

if not st.session_state.get("chatbot_api_key"):
   openai_api_key = st.secrets.OPENAI_API_KEY # No puede ir al principio

#st.title("Tutor Socrático 💬")
col1, col2 = st.columns([0.5,0.5]) # Dividir la pantalla en dos columnas

with col1: # Columna de la izquierda
   st.subheader("Ejercicio 1")
   st.write('¿Cuantos bits ha de tener el campo de host de una dirección IP para poder contener 4 direcciones de host?')
   #user_input = st.text_area('Inserta tu respuesta aquí:', height=100)
   user_input = st.number_input('tu respuesta:', min_value=0, step=1, format="%i")

   if st.button('Corregir'):
      if user_input == 3:
         st.success('Respuesta correcta.') 
         st.session_state.messages.append({"role": "assistant", "content": "¡Felicidades! Has acertado."})
      else:
         st.error('La respuesta no es correcta.')
         st.session_state.messages.append({"role": "system", "content": f"el usuario a contestado {user_input}"})
         client = OpenAI(api_key=openai_api_key)
         response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
         msg = response.choices[0].message.content
         st.session_state.messages.append({"role": "assistant", "content": msg})
    
with col2: # Columna de la derecha
   st.subheader("Tutor Socrático 💬")
   if "messages" not in st.session_state:
      st.session_state["messages"] = [{"role": "assistant", "content": "¿Alguna duda con el ejercicio?"}]

   with st.container():
        for msg in st.session_state.messages:
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