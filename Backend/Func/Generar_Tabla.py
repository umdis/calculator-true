from .Proposicion import parseProposition

# Esta función toma una expresion y genera la tabla de la verdad y su resultado
def writeTruthTable(P):
    # Crea un diccionario vacío para almacenar los valores de verdad de las variables
    truthValues = {}

    # Itera sobre cada carácter en la proposición
    for i in range(len(P)):
        # Si el carácter es una letra mayúscula, agrega la variable al diccionario con un valor de verdad verdadero
        #Modificar para que acepte minusculas!!!!!!!!!!!!!!!!
        if P[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            truthValues[P[i]] = True

    # Imprime el encabezado de la tabla de verdad, que consiste en las variables de la proposición y la proposición misma
    for statement in list(truthValues.keys()):
        print(statement, end=" | ")
    print(P)

    # Imprime la primera fila de la tabla de verdad, que consiste en los valores de verdad de las variables
    for truthValue in list(truthValues.values()):
        print("T" if truthValue else "F", end=" | ")
    # Evalúa la proposición y imprime su valor de verdad
    print("T" if parseProposition(P, truthValues) else "F")

    # Comienza a iterar a través de todas las combinaciones posibles de valores de verdad
    j = len(truthValues.values()) - 1
    while True in truthValues.values():
        # Obtiene la variable a la que se le cambiará el valor de verdad
        variable = list(truthValues.keys())[j]
        # Cambia el valor de verdad de la variable
        truthValues[variable] = not truthValues[variable]

        # Si el valor de verdad de la variable se ha cambiado de verdadero a falso, imprime la fila correspondiente
        if not truthValues[variable]:
            for truthValue in list(truthValues.values()):
                print("T" if truthValue else "F", end=" | ")
            # Evalúa la proposición y imprime su valor de verdad
            print("T" if parseProposition(P, truthValues) else "F")
            j = len(truthValues.values()) - 1
        # Si el valor de verdad de la variable se ha cambiado de falso a verdadero, simplemente decrementa el índice
        else:
            j -= 1