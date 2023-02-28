# Esta función comprueba si una proposición está bien formada,
# es decir, si tiene paréntesis abiertos y cerrados correctamente.
# Retorna True si es bien formada, False en caso contrario.
def isWellFormed(P):
    bracketLevel = 0
    for c in P:
        if c == "(":
            bracketLevel += 1
        if c == ")":
            if bracketLevel == 0:
                return False
            bracketLevel -= 1
    return bracketLevel == 0

# Esta función toma una proposición negada y una tabla de valores de verdad,
# y devuelve el valor de verdad de la proposición negada.
def parseNegation(P, truthValues):
    return not parseProposition(P, truthValues)

# Esta función toma dos proposiciones y una tabla de valores de verdad,
# y devuelve el valor de verdad de la conjunción de ambas proposiciones.
def parseConjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) and parseProposition(Q, truthValues)

# Esta función toma dos proposiciones y una tabla de valores de verdad,
# y devuelve el valor de verdad de la disyunción de ambas proposiciones.
def parseDisjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) or parseProposition(Q, truthValues)

# Esta función toma dos proposiciones y una tabla de valores de verdad,
# y devuelve el valor de verdad de la implicación de P hacia Q.
def parseConditional(P, Q, truthValues):
    return (not parseProposition(P, truthValues)) or parseProposition(Q, truthValues)

# Esta función toma dos proposiciones y una tabla de valores de verdad,
# y devuelve el valor de verdad de la bicondicional de ambas proposiciones.
def parseBiconditional(P, Q, truthValues):
    return parseProposition(P, truthValues) == parseProposition(Q, truthValues)

# Esta función toma una proposición y una tabla de valores de verdad,
# y devuelve el valor de verdad de la proposición.
def parseProposition(P, truthValues):
    # Quitamos los espacios de la proposición para simplificar el procesamiento.
    P = P.replace(" ", "")

    # Si la proposición no está bien formada, retornamos "Error".
    if not isWellFormed(P):
        return "Error"

    # Quitamos los paréntesis externos si la proposición es bien formada.
    while P[0] == "(" and P[-1] == ")" and isWellFormed(P[1:len(P) - 1]):
        P = P[1:len(P) - 1]

    # Si la proposición es una variable proposicional, retornamos su valor de verdad.
    if len(P) == 1:
        return truthValues[P]

    # Buscamos el operador más externo de la proposición y aplicamos la función correspondiente.
    # Esto se hace en orden inverso para que encontremos primero los operadores más externos.
     # Buscamos el operador de implicación (→) más externo.
    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "→" and bracketLevel == 0:
            return parseConditional(P[0:i], P[i + 1:], truthValues)

    # Buscamos el operador de doble implicación (↔) más externo.
    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "↔" and bracketLevel == 0:
            return parseBiconditional(P[0:i], P[i + 1:], truthValues)

    # Buscamos el operador de disyunción (∨) más externo.
    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∨" and bracketLevel == 0:
            return parseDisjunction(P[0:i], P[i + 1:], truthValues)

    # Buscamos el operador de conjunción (∧) más externo.
    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "∧" and bracketLevel == 0:
            return parseConjunction(P[0:i], P[i + 1:], truthValues)

    # Buscamos el operador de negación (¬) más externo.
    bracketLevel = 0
    for i in reversed(range(len(P))):
        if P[i] == "(":
            bracketLevel += 1
        if P[i] == ")":
            bracketLevel -= 1
        if P[i] == "¬" and bracketLevel == 0:
            return parseNegation(P[i + 1:], truthValues)

# Esta función toma una expresion
def writeTruthTable(P):
    # Crea un diccionario vacío para almacenar los valores de verdad de las variables
    truthValues = {}

    # Itera sobre cada carácter en la proposición
    for i in range(len(P)):
        # Si el carácter es una letra mayúscula, agrega la variable al diccionario con un valor de verdad verdadero
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

            
writeTruthTable("P ∨ (Q → (R ∧ T))")
