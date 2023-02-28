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