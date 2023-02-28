from .Validador import isWellFormed

# Esta función toma una proposición negada y una tabla de valores de verdad,
# y devuelve el valor de verdad de la proposición negada.
def parseNegation(P, truthValues):
    return not parseProposition(P, truthValues)

# Esta función toma dos proposiciones y una tabla de valores de verdad,
# y devuelve el valor de verdad de la disyunción de ambas proposiciones.
def parseDisjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) or parseProposition(Q, truthValues)

# Esta función toma dos proposiciones y una tabla de valores de verdad,
# y devuelve el valor de verdad de la conjunción de ambas proposiciones.
def parseConjunction(P, Q, truthValues):
    return parseProposition(P, truthValues) and parseProposition(Q, truthValues)

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