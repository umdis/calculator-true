from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware as StarletteCORSMiddleware
from classes.operation import Operation

import itertools
import re
from sympy import symbols, Not, And, Or, Implies, Equivalent, simplify_logic


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verificar_sintaxis(expresion):
    stack = []
    for char in expresion:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack


def convertir_sympy(expresion, simbolo_dict):
    # Eliminar los paréntesis externos si están presentes
    if expresion.startswith('(') and expresion.endswith(')'):
        expresion = expresion[1:-1]

    match = re.search(r'(?<![\w()])↔(?![\w()])', expresion)
    if match:
        i = match.start()
        left = convertir_sympy(expresion[:i].strip(), simbolo_dict)
        right = convertir_sympy(expresion[i + 1:].strip(), simbolo_dict)
        return Equivalent(left, right)

    return eval(expresion.replace("¬", "~").replace("∧", "&").replace("∨", "|").replace("→", ">>"), simbolo_dict)



def revertir_operadores(expresion_sympy):
    expresion = str(expresion_sympy).replace("~", "¬").replace("&", "∧").replace("|", "∨").replace(">>", "→").replace("==", "↔")
    return expresion

def generar_tabla_de_verdad(expresion):
    if not verificar_sintaxis(expresion):
        raise ValueError("Sintaxis de la proposición incorrecta")

    variables = sorted(list(set(re.findall(r'[A-Za-z]', expresion))))
    simbolos = symbols(" ".join(variables))
    simbolo_dict = {str(var): var for var in simbolos}
    formula = convertir_sympy(expresion, simbolo_dict)

    encabezado = variables + [expresion]
    tabla = [encabezado]

    for valores in itertools.product([False, True], repeat=len(variables)):
        asignacion = dict(zip(simbolos, valores))
        fila = [valor for valor in valores]

        if not isinstance(formula, bool):
            fila.append(formula.subs(asignacion))
        else:
            fila += [formula]

        tabla.append([("V" if valor else "F") for valor in fila[:-1]] + [("V" if fila[-1] else "F")])

    return tabla

expresion = "(A ↔ ¬B)"
tabla_de_verdad = generar_tabla_de_verdad(expresion)
# La variable "tabla_de_verdad" esta la matriz

@app.get("/")
def read_root():
    return {"response": "Welcome to use free Algebra boolean calculator"}

#Corregir
@app.post('/formula')
def procesar_proposicion(operation: Operation):
    proposicion = operation.formula
    expresion = realizar_calculo(proposicion)
    if expresion is not None:
        response = obtener_valores_de_verdad(str(expresion))
        print(response)
        return {"response": response}
    else:
        return {"error": 'La proposición no está bien formada'}