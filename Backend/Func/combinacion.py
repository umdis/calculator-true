from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd



# Define los operadores lógicos permitidos
logical_operators = {'and', 'or', 'not', 'implies', 'iff'}
#logical_operators = {'∧', '∨', '¬', '→', '↔'}
# Función para verificar la sintaxis de la proposición


def is_well_formed(proposition):
    # Elimina todos los espacios en blanco y paréntesis
    proposition = ''.join(proposition.split())
    proposition = proposition.replace('(', '')
    proposition = proposition.replace(')', '')

    # Comprueba que solo se usen operadores lógicos permitidos
    words = proposition.split()
    for word in words:
        if word not in logical_operators and not is_valid_variable(word):
            return f"La palabra '{word}' no es un operador lógico permitido ni una variable válida"

    # Comprueba que no haya dos operadores consecutivos
    for i in range(len(words) - 1):
        if words[i] in logical_operators and words[i + 1] in logical_operators:
            return f"Hay dos operadores lógicos consecutivos: '{words[i]}' y '{words[i+1]}'"

    # Comprueba que la proposición no termine con un operador lógico
    if words[-1] in logical_operators:
        return f"La proposición no puede terminar con el operador lógico '{words[-1]}'"

    return True


# Función para comprobar si una cadena es una variable válida
def is_valid_variable(variable):
    if len(variable) == 0:
        return False
    if not variable[0].isalpha():
        return False
    for c in variable[1:]:
        if not c.isalnum() and c != '_':
            return False
    return True

# Función para convertir la proposición en una expresión de Sympy


def to_sympy_expression(proposition):
    # Reemplaza los operadores lógicos por sus equivalentes en Sympy
    proposition = proposition.replace('and', '&')
    proposition = proposition.replace('or', '|')
    proposition = proposition.replace('not', '~')
    proposition = proposition.replace('implies', '>>')
    proposition = proposition.replace('iff', '==')

    try:
        return sympify(proposition)
    except SympifyError as e:
        error_type = type(e).__name__
        error_location = str(e).split('\'')[1]
        return f"Error de sintaxis en la proposición: {error_type} en {error_location}"


def realizar_calculo(proposicion):
    check = is_well_formed(proposicion)
    if check is True:
        expresion = to_sympy_expression(proposicion)
        if expresion is not None:
            return expresion
        else:
            print('Error al convertir la proposición a una expresión de Sympy')
    else:
        print(check)



# Función para obtener los valores de verdad de una proposición
def obtener_valores_de_verdad(proposicion):
    # Parsear la proposición como una expresión simbólica
    expr = sympify(proposicion)
    # Obtener las variables de la proposición
    variables = list(expr.free_symbols)
    # Crear una tabla de verdad completa
    tabla = []
    # Crear una lista para almacenar las columnas de operaciones lógicas
    columnas_operaciones = []
    for i in range(2**len(variables)):
        fila = []
        for j, variable in enumerate(variables):
            valor_variable = (i // 2**j) % 2
            fila.append(True if valor_variable == 1 else False)
        # Evaluamos cada operación lógica y añadimos su resultado como una columna adicional
        for operacion in expr.atoms(And, Or, Not, Xor, Implies, Equivalent):
            resultado_operacion = operacion.subs(
                {variables[k]: (i // 2**k) % 2 for k in range(len(variables))})
            nombre_operacion = str(operacion)
            if nombre_operacion not in columnas_operaciones:
                columnas_operaciones.append(nombre_operacion)
            fila.append(str(bool(resultado_operacion)))
        tabla.append(fila)

    # Agregar las columnas de operaciones lógicas al conjunto de columnas
    columnas = variables + columnas_operaciones

    # Ordenar las columnas de menor a mayor longitud
    columnas_ordenadas = sorted(columnas, key=lambda x: len(str(x)))

    # Crear un DataFrame de pandas con la tabla de verdad
    df = pd.DataFrame(tabla, columns=columnas_ordenadas)

    # Agregar una columna con los valores finales de la proposición
    df[proposicion] = df.apply(lambda row: str(
        bool(expr.subs({variables[k]: row[k] for k in range(len(variables))}))), axis=1)


    
    matriz_de_listas = [df.columns.tolist()] + df.values.tolist()
    
    return (matriz_de_listas)

def validar_proposicion(prop):
    try:
        expresion = simplify(sympify(prop))
        return True
    except:
        return False


# Ejemplo de uso
proposicion = input("Digite una proposicion logica:")

if validar_proposicion(proposicion) == True:
    expresion = realizar_calculo(proposicion)
    if expresion is not None:
        print(obtener_valores_de_verdad(str(expresion)))
    else:
        print('La proposición no está bien formada')
else:
    print('La proposición no está bien formada verifique la sintaxis e intente nuevamente')