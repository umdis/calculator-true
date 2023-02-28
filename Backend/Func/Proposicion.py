from .Validador import isWellFormed

def parseProposition(P, truthValues):
    """
    Esta función toma una proposición y una tabla de valores de verdad,
    y devuelve el valor de verdad de la proposición.
    """
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
    operators = [("→", parseConditional), ("↔", parseBiconditional),
                 ("∨", parseDisjunction), ("∧", parseConjunction),
                 ("¬", parseNegation)]
    
    for operator, function in operators:
        bracketLevel = 0
        for i in reversed(range(len(P))):
            if P[i] == "(":
                bracketLevel += 1
            if P[i] == ")":
                bracketLevel -= 1
            if P[i] == operator and bracketLevel == 0:
                return function(P[0:i], P[i + 1:], truthValues)
    
    return "Error"

def parseNegation(P, truthValues):
    """
    Esta función toma una proposición negada y una tabla de valores de verdad,
    y devuelve el valor de verdad de la proposición negada.
    """
    return not parseProposition(P, truthValues)

def parseDisjunction(P, Q, truthValues):
    """
    Esta función toma dos proposiciones y una tabla de valores de verdad,
    y devuelve el valor de verdad de la disyunción de ambas proposiciones.
    """
    return parseProposition(P, truthValues) or parseProposition(Q, truthValues)

def parseConjunction(P, Q, truthValues):
    """
    Esta función toma dos proposiciones y una tabla de valores de verdad,
    y devuelve el valor de verdad de la conjunción de ambas proposiciones.
    """
    return parseProposition(P, truthValues) and parseProposition(Q, truthValues)

def parseConditional(P, Q, truthValues):
    """
    Esta función toma dos proposiciones y una tabla de valores de verdad,
    y devuelve el valor de verdad de la implicación de P hacia Q.
    """
    return (not parseProposition(P, truthValues)) or parseProposition(Q, truthValues)

def parseBiconditional(P, Q, truthValues):
    """
    Esta función toma dos proposiciones y una tabla de valores de verdad,
    y devuelve el valor de verdad de la bicondicional de ambas proposiciones.
    """
    return parseProposition(P, truthValues) == parseProposition(Q, truthValues)
