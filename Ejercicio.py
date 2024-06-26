from chatgpt import ChatConversation


class Ejercicio:
    def __init__(self, texto):
        # Inicialización de los atributos donde se almacenarán los datos.
        self.materia = None
        self.titulo = None
        self.enunciado = None
        self.aclaracion_enunciado = None
        self.contexto_materia = None
        self.contexto_ejercicio = None
        self.soluciones = []
        self.soluciones_incorrectas = [] # {'texto','error_conceptual', 'pregunta_socratica', 'respuesta'}
        self.dudas_enunciado = []    # {'texto','respuesta'}
        self.preguntas_socraticas = [] # {'texto','respuesta'}
        self.extrae_de_texto(texto)


    # Prompt para el tutor socrático
    def prompt_tutor(self):
        prompt = 'Eres un tutor socrático y debes ayudar a un estudiante con el siguiente ejercicio:\n'
        prompt += f'#TÍTULO: {self.titulo}'
        if self.materia:
            prompt += f'#MATERIA: {self.materia}\n'
        if self.bloque:
            prompt += f'#BLOQUE: {self.bloque}\n'
        prompt += f'#ENUNCIADO: {self.enunciado}\n'
        if self.contexto_materia:
            prompt += f'#CONTEXTO MATERIA: {self.contexto_materia}\n'
        if self.contexto_ejercicio:    
            prompt += f'#CONTEXTO EJERCICIO: {self.contexto_ejercicio}\n'
        if self.aclaracion_enunciado:
            prompt += f'Si el estudiante plantea alguna duda, debes responderla usando la información:\n'
            prompt += f'#ACLARACIÓN ENUNCIADO: {self.aclaracion_enunciado}\n'
        if self.dudas_enunciado:
            prompt += f'Si el estudiante planteal alguna de las siguientes dudas del enenciado, responde lo que se indica:\n'
            for duda in self.dudas_enunciado:
                prompt += f'#DUDA ENUNCIADO: {duda["texto"]}\n#RESPUESTA: {duda["respuesta"]}\n'
        if self.preguntas_socraticas:        
            prompt += 'Si el estudiante plantea alguna de las siguientes preguntas, responde lo que se indica:'
            for pregunta in self.preguntas_socraticas:
                prompt += f'#PREGUNTA SOCRÁTICA: {pregunta["texto"]}\n#RESPUESTA: {pregunta["respuesta"]}\n'
        if self.soluciones:
            prompt += 'Las posibles soluciones correctas del ejercicio son:'
            for solucion in self.soluciones:
                prompt += f'#SOLUCIÓN: {solucion}\n'
        if self.soluciones_incorrectas:    
            prompt += '\nAdemás, debes tener en cuenta las siguientes soluciones incorrectas:'
            for incorrecta in self.soluciones_incorrectas:
                prompt += f'#SOLUCIÓN INCORRECTA: {incorrecta["texto"]}\n#ERROR CONCEPTUAL: {incorrecta["error_conceptual"]}\n#PREGUNTA A INCORRECTA: {incorrecta["pregunta_socratica"]}\n#RESPUESTA: {incorrecta["respuesta"]}\n'
        prompt += '''
Si el estudiante plantea alguna duda sobre la solución, debes responderla de forma socrática.
Nunca debes dar la respuesta directa, sino plantear preguntas que ayuden al estudiante a llegar a la respuesta correcta.'''
        return prompt
        
    # Método para corregir el ejercicio
    # Parámetros:
    #   - respuesta: La solución propuesta por el estudiante
    # Retorna diccionario con las siguientes llaves:
    #   - 'correcta': True si la solución es correcta, False si es incorrecta
    #   - 'numero_solucion': el número de la solución correcta o incorrecta que más se parece a la del estudiante. (empieza en 0)
    #   - 'error_conceptual': Si la solución es incorrecta, el error conceptual cometido
    #   - 'pregunta_socratica': Si la solución es incorrecta, la pregunta socrática a realizar
    #   - 'respuesta_socratica': Si la solución es incorrecta, la respuesta a la pregunta socrática
    def corregir(self, respuesta, model = "gpt-4-1106-preview"):

        prompt = f'''
### IMPORTANT AI ROLE: You are not a chatbot. You act as the AI service. 

Dado el siguiente problema:

#TÍTULO: {self.titulo}
#MATERIA: {self.materia}
#BLOQUE: {self.bloque}
#ENUNCIADO: {self.enunciado}
#CONTEXTO MATERIA: {self.contexto_materia}
#CONTEXTO EJERCICIO: {self.contexto_ejercicio}

Con las siguientes soluciones correctas:
'''
        for i,solucion in enumerate(self.soluciones):
            prompt += f'SOLUCIÓN CORRECTA {i}: {solucion}\n'
        prompt += f'''\n
Y con las siguientes soluciones incorrectas:
'''
        for i,incorrecta in enumerate(self.soluciones_incorrectas):
            prompt += f'SOLUCIÓN INCORRECTA {i}: {incorrecta["texto"]}\n'
        prompt += f'''\n
A partir de la solución propuesta por el estudiante:

"{respuesta}"

Analiza a que SOLUCIÓN CORRECTA o SOLUCIÓN INCORRECTA se parece más.

Responde únicamente:
'''
        for i in range(len(self.soluciones)):
            prompt += f'SOLUCIÓN_CORRECTA_{i} ó '
        for i in range(len(self.soluciones_incorrectas)):
            prompt += f'SOLUCIÓN_INCORRECTA_{i} ó '
        prompt += f'''
ó SOLUCIÓN_CORRECTA_DIFERENTE si la solución es correcta y no se parece a ninguna solución correcta.
ó SOLUCIÓN_INCORRECTA_DIFERENTE si la solución es incorrecta y no se parece a ninguna solución incorrecta.

Recuerda que debes responder con la solución correcta o incorrecta que más se parezca a la solución propuesta por el estudiante.
'''
        #print(prompt)
        chat = ChatConversation()
        LLM_response = chat.send_message(prompt)
        print(LLM_response)
        try:
            numero_solucion = int(LLM_response.split('_')[2])
        except:
            numero_solucion = None
        if LLM_response.startswith('SOLUCIÓN_CORRECTA'):
            return {'correcta': True, 'numero_solucion': numero_solucion, 'error_conceptual': None, 'pregunta_socratica': None, 'respuesta_socratica': None}
        elif LLM_response=='SOLUCIÓN_CORRECTA_DIFERENTE':
            return {'correcta': True, 'numero_solucion': None, 'error_conceptual': None, 'pregunta_socratica': None, 'respuesta_socratica': None}
        elif LLM_response=='SOLUCIÓN_INCORRECTA_DIFERENTE':
            return {'correcta': False, 'numero_solucion': None, 'error_conceptual': None, 'pregunta_socratica': None, 'respuesta_socratica': None}
        elif LLM_response.startswith('SOLUCIÓN_INCORRECTA'):
            incorrecta = self.soluciones_incorrectas[numero_solucion]
            return {'correcta': False, 'numero_solucion': numero_solucion, 'error_conceptual': incorrecta['error_conceptual'], 'pregunta_socratica': incorrecta['pregunta_socratica'], 'respuesta_socratica': incorrecta['respuesta']}
 
    # Método para extraer la información de un texto y almacenarla en los atributos de la clase.
    def extrae_de_texto(self, texto):
        lineas = texto.split('\n')
        seccion_actual = None
        for linea in lineas:
            linea = linea.strip()
            if linea == '' or linea.startswith('//'):
                continue
            if linea.startswith('MATERIA:'):
                self.materia = linea.split('MATERIA:')[1].strip()
                seccion_actual = 'materia'
            elif linea.startswith('BLOQUE:'):
                self.bloque = linea.split('BLOQUE:')[1].strip()
                seccion_actual = 'bloque'
            elif linea.startswith('TÍTULO:'):
                self.titulo = linea.split('TÍTULO:')[1].strip()
                seccion_actual = 'titulo'
            elif linea.startswith('ENUNCIADO:'):
                self.enunciado = linea.split('ENUNCIADO:')[1].strip()
                seccion_actual = 'enunciado'
            elif linea.startswith('CONTEXTO MATERIA:'):
                self.contexto_materia = linea.split('CONTEXTO MATERIA:')[1].strip()
                seccion_actual = 'contexto_materia'
            elif linea.startswith('CONTEXTO EJERCICIO:'):
                self.contexto_ejercicio = linea.split('CONTEXTO EJERCICIO:')[1].strip()
                seccion_actual = 'contexto_ejercicio'    
            elif linea.startswith('SOLUCIÓN:'):
                solucion = linea.split(':')[1].strip()
                self.soluciones.append(solucion)
                seccion_actual = 'solucion'
            elif linea.startswith('ACLARACIÓN ENUNCIADO:'):
                self.aclaracion_enunciado = linea.split('ACLARACIÓN ENUNCIADO:')[1].strip()
                seccion_actual = 'aclaracion'
            elif linea.startswith('DUDA ENUNCIADO:'):
                duda = linea.split(':')[1].strip()
                self.dudas_enunciado.append({'texto': duda, 'respuesta': None})
                seccion_actual = 'duda'
            elif linea.startswith('PREGUNTA SOCRÁTICA:'):
                pregunta = linea.split(':')[1].strip()
                self.preguntas_socraticas.append({'texto': pregunta, 'respuesta': None})
                seccion_actual = 'socratica'
            elif  linea.startswith('SOLUCIÓN INCORRECTA:'):
                incorrecta = linea.split(':')[1].strip()
                self.soluciones_incorrectas.append({'texto': incorrecta,'error_conceptual': None, 'pregunta_socratica': None, 'respuesta': None})
                seccion_actual = 'incorrecta'
            #Continua el texto con la sección actual
            elif seccion_actual == 'materia':
                self.materia = (self.materia+'\n'+linea).strip()
            elif seccion_actual == 'bloque':
                self.bloque = (self.bloque+'\n'+linea).strip()
            elif seccion_actual == 'titulo':
                self.titulo = (self.titulo+'\n'+linea).strip()
            elif seccion_actual == 'enunciado':
                self.enunciado = (self.enunciado+'\n'+linea).strip()
            elif seccion_actual == 'contexto_materia':
                self.contexto_materia = (self.contexto_materia+'\n'+linea).strip()
            elif seccion_actual == 'contexto_ejercicio':
                self.contexto_ejercicio = (self.contexto_ejercicio+'\n'+linea).strip()
            elif seccion_actual == 'aclaracion':
                self.aclaracion_enunciado += linea + ' '
            elif seccion_actual == 'solucion':
                self.soluciones[-1] = (self.soluciones[-1]+'\n'+linea).strip()
            elif seccion_actual == 'duda':
                if linea.startswith('RESPUESTA:'):
                    self.dudas_enunciado[-1]['respuesta'] =  linea.split('RESPUESTA:')[1].strip()
                    seccion_actual = 'duda_R'
                else:
                    self.dudas_enunciado[-1]['texto'] = (self.dudas_enunciado[-1]['texto']+'\n'+linea).strip()
            elif seccion_actual == 'duda_R':
                self.dudas_enunciado[-1]['respuesta'] = (self.dudas_enunciado[-1]['respuesta']+'\n'+linea).strip()
            elif seccion_actual == 'socratica':
                if linea.startswith('RESPUESTA:'):
                    self.preguntas_socraticas[-1]['respuesta'] =  linea.split('RESPUESTA:')[1].strip()
                    seccion_actual = 'socratica_R'
                else:
                    self.preguntas_socraticas[-1]['texto'] = (self.preguntas_socraticas[-1]['texto']+'\n'+linea).strip()
            elif seccion_actual == 'socratica_R':
                self.preguntas_socraticas[-1]['respuesta'] = (self.preguntas_socraticas[-1]['respuesta']+'\n'+linea).strip()
            elif seccion_actual == 'incorrecta':
                if linea.startswith('ERROR CONCEPTUAL:'):
                    self.soluciones_incorrectas[-1]['error_conceptual'] = linea.split(':')[1].strip()
                    seccion_actual = 'incorrecta_error'
                else:
                    self.soluciones_incorrectas[-1]['texto'] = (self.soluciones_incorrectas[-1]['texto']+'\n'+linea).strip()
            elif seccion_actual == 'incorrecta_error':
                if linea.startswith('PREGUNTA A INCORRECTA:'):
                    self.soluciones_incorrectas[-1]['pregunta_socratica'] = linea.split(':')[1].strip()
                    seccion_actual = 'incorrecta_pregunta'
                else:
                    self.soluciones_incorrectas[-1]['error_conceptual'] = (self.soluciones_incorrectas[-1]['error_conceptual']+'\n'+linea).strip()
            elif seccion_actual == 'incorrecta_pregunta':
                if linea.startswith('RESPUESTA:'):
                    self.soluciones_incorrectas[-1]['respuesta'] = linea.split('RESPUESTA:')[1].strip()
                    seccion_actual = 'incorrecta_respuesta'
                else:
                    self.soluciones_incorrectas[-1]['pregunta_socratica'] = (self.soluciones_incorrectas[-1]['pregunta_socratica']+'\n'+linea).strip()

def cargar_de_fichero(nombre_fichero):
    with open(nombre_fichero, 'r', encoding='utf-8') as archivo:
        texto = archivo.read()
        # Crear un objeto Ejercicio a partir del texto del archivo
        ejercicio = Ejercicio(texto)
    return ejercicio



        