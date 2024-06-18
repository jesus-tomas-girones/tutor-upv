# Función para cargar el archivo y crear un objeto de ArchivoEjercicio
from Ejercicio import Ejercicio
from chatgpt import ChatConversation

def cargar_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        texto = archivo.read()
        ejercicio = Ejercicio(texto)
    return ejercicio

# Función para imprimir información importante del ejercicio
def imprimir_informacion(ejercicio):
    print("Materia:", ejercicio.materia)
    print("Título:", ejercicio.titulo)
    print("Enunciado:", ejercicio.enunciado)
    print("Contexto:", ejercicio.contexto)
    print("Soluciones Propuestas:")
    for solucion in ejercicio.soluciones:
        print("  -", solucion)
    print("Aclaración del Enunciado:", ejercicio.aclaracion_enunciado)
    print("Dudas del Enunciado:")
    for duda in ejercicio.dudas_enunciado:
        print("  -", duda['texto'])
        print("     Respuesta:", duda['respuesta'])
    print("Preguntas Socráticas:")
    for pregunta in ejercicio.preguntas_socraticas:
        print("  -", pregunta['texto'])
        print("     Respuesta:", pregunta['respuesta'])
    print("Soluciones Incorrectas:")
    for incorrecta in ejercicio.soluciones_incorrectas:
        print("  -", incorrecta['texto'])
        print("     Error Conceptual:", incorrecta['error_conceptual'])
        print("     Pregunta Socrática:", incorrecta['pregunta_socratica'])
        print("     Respuesta:", incorrecta['respuesta'])
        
test = [ 
    {'t': 'El hombre se llama Juan.', 'correcta':False, 'num': None}, #SOLUCIÓN_INCORRECTA_DIFERENTE
    {'t': 'El hombre es de la isla.', 'correcta':False, 'num': 0}, #SOLUCIÓN_INCORRECTA_0
    {'t': 'El hombre no es nativo.', 'correcta':False, 'num': 1}, #SOLUCIÓN_INCORRECTA_1
    {'t': 'Dado que la chica siempre dice la verdad, el hombre no es de la isla.', 'correcta':False, 'num': 2}, #SOLUCIÓN_INCORRECTA_2
    #SOLUCIONES_CORRECTAS
    {'t': 'El hombre es de la isla, dado que la frase que afirma nunca puede ser verdadera.', 'correcta':True, 'num': None}, 
    {'t': 'El no dice la verdad, es nativo.', 'correcta':True, 'num': None}, 
    {'t': 'El hombre es nativo. La frase que dice nunca puede ser verdad. Está mintiendo.', 'correcta':True, 'num': None}, 
    
]

# Ejecución principal
if __name__ == "__main__":
    nombre_archivo = './ejercicios/isla_mentirosos.txt'  # Asegúrate de que el archivo exista en esta ruta
    ejercicio = cargar_archivo(nombre_archivo)

    #imprimir_informacion(ejercicio)
    errores = 0
    for t in test:
        print('\n', t['t'])
        LLM_response = ejercicio.corregir(t['t']) #, model="gpt-3.5-turbo") 
        print(LLM_response)
        if (t['correcta']):
            if LLM_response['correcta']:
                print('ACIERTO')
            else:
                print('ERROR')
                errores += 1
        else:
            if LLM_response['correcta']:
                print('ERROR')
                errores += 1
            else:
                if t['num'] == LLM_response['numero_solucion']:
                    print('ACIERTO')
                else:
                    print('ERROR')
                    errores += 1
    print('Errores:', errores, '  ********************************')


    #print('Solución propuesta: ', solución1)
    #corrección = ejercicio.corregir(solución1, model="gpt-3.5-turbo")
    #print(corrección)
