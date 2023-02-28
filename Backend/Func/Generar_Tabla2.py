from .Proposicion import parseProposition

def writeTruthTable2(P):
    # Crea un diccionario vacío para almacenar los valores de verdad de las variables
    truthValues = {}

    # Itera sobre cada carácter en la proposición
    for i in range(len(P)):
        # Si el carácter es una letra mayúscula, agrega la variable al diccionario con un valor de verdad verdadero
        if P[i] in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
            truthValues[P[i]] = True

    # Inicializa una lista vacía para almacenar la tabla de verdad
    truthTable = []

    # Agrega el encabezado de la tabla de verdad a la matriz
    headerRow = []
    for statement in list(truthValues.keys()):
        headerRow.append(statement)
    headerRow.append(P)
    truthTable.append(headerRow)

    # Agrega la primera fila de la tabla de verdad a la matriz
    firstRow = []
    for truthValue in list(truthValues.values()):
        firstRow.append("V" if truthValue else "F")
    firstRow.append("V" if parseProposition(P, truthValues) else "F")
    truthTable.append(firstRow)

    # Comienza a iterar a través de todas las combinaciones posibles de valores de verdad
    j = len(truthValues.values()) - 1
    while True in truthValues.values():
        # Obtiene la variable a la que se le cambiará el valor de verdad
        variable = list(truthValues.keys())[j]
        # Cambia el valor de verdad de la variable
        truthValues[variable] = not truthValues[variable]

        # Si el valor de verdad de la variable se ha cambiado de verdadero a falso, agrega la fila correspondiente a la matriz
        if not truthValues[variable]:
            row = []
            for truthValue in list(truthValues.values()):
                row.append("V" if truthValue else "F")
            row.append("V" if parseProposition(P, truthValues) else "F")
            truthTable.append(row)
            j = len(truthValues.values()) - 1
        # Si el valor de verdad de la variable se ha cambiado de falso a verdadero, simplemente decrementa el índice
        else:
            j -= 1

        # Si se han recorrido todas las filas, sal del bucle
        if j < 0:
            break

    return truthTable
