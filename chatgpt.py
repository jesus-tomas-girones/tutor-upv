if __name__ == "__main__":
    print("Este fichero no se puede ejecutar, es un módulo.")
    exit()

from openai import OpenAI
from api_keys import openai_api_key

# Ejemplo de uso:
#   chat = ChatConversation()
#   print(chat.send_message("Hello, how are you?"))

class ChatConversation:
  
  global_cost = 0       # Coste total de todas las conversaciones
  global_tokens_in = 0  # Tokens de entrada totales
  global_tokens_out = 0 # Tokens de salida totales

  def __init__(self, api_key: str = "", system_prompt: str = "", model: str = "gpt-4-1106-preview"):
    if not api_key:
      api_key = openai_api_key # API Key definida en /api_keys.py

    self.clientOpenAI = OpenAI(api_key=api_key)
    self.model = model
    self.cost = 0 
    self.tokens_in = 0
    self.tokens_out = 0
    self.messages = []
    if system_prompt:
      self.messages.append({"role": "system", "content": system_prompt})

  def send_message(self, user_prompt: str) -> str:
    self.messages.append({"role": "user", "content": user_prompt})
    response = self.clientOpenAI.chat.completions.create(
            model = self.model,
            messages = self.messages
    )
    if response.usage:
      self.tokens_in += response.usage.prompt_tokens
      #global_tokens_in += response.usage.prompt_tokens
      self.tokens_out += response.usage.completion_tokens
      #global_tokens_out += response.usage.completion_tokens
      cost = self.get_cost(response.usage.prompt_tokens, response.usage.completion_tokens)
      self.cost += cost
      #global_cost += cost

    chatbot_response = response.choices[0].message.content
    if chatbot_response is None:
      raise RuntimeError("ERROR: ChatGPT did not give a response back")
      return "ERROR: ChatGPT did not give a response back"

    self.messages.append({"role": "assistant", "content": chatbot_response })
    return chatbot_response

  def get_cost(self, tokens_in: int, tokens_out: int) -> float:
    if self.model in ["gpt-4-1106-preview"]:  #4-Turbo, 128K de contexto, entrenado hasta Abril 2023
      cost_per_token_in  = 0.01/1000
      cost_per_token_out = 0.03/1000
    elif self.model in ["gpt-4", "gpt-4-0613", "gpt-4-0314"]:
      cost_per_token_in  = 0.03/1000
      cost_per_token_out = 0.06/1000
    elif self.model in ["gpt-4-32k", "gpt-4-32k-0613", "gpt-4-32k-0314"]:
      cost_per_token_in  = 0.06/1000
      cost_per_token_out = 0.12/1000
    elif self.model in ["gpt-3.5-turbo-instruct"]: #No para ChatBot
      cost_per_token_in  = 0.0015/1000
      cost_per_token_out = 0.0020/1000
    elif self.model in ["gpt-3.5-turbo-1106", "gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613"]:
      cost_per_token_in  = 0.0010/1000
      cost_per_token_out = 0.0020/1000
    else:
      print(f'Unknown model {self.model}, not calculating costs')
      cost_per_token_in  = 0.0
      cost_per_token_out = 0.0
      
    return tokens_in*cost_per_token_in + tokens_out*cost_per_token_out