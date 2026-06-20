class BinaryValidator:
    """
    Lenguaje:
    L = { x op y | x, y ∈ {0,1}+, op ∈ {+, -} }

    Gramática:
    S → B O B
    O → + | -
    B → 0B | 1B | 0 | 1
    """

    @staticmethod
    def validate(expression: str):
        expression = expression.strip()

        if not expression:
            return False, "La entrada está vacía."

        operators = expression.count("+") + expression.count("-")
        if operators != 1:
            return False, "La cadena debe contener exactamente un operador: '+' o '-'."

        operator = "+" if "+" in expression else "-"
        left, right = expression.split(operator)

        if left == "" or right == "":
            return False, f"Debe existir un número binario antes y después del operador '{operator}'."

        for char in left + right:
            if char not in ("0", "1"):
                return False, f"Símbolo inválido encontrado: '{char}'."

        return True, "Cadena válida."

    @staticmethod
    def grammar_text():
        return """
GRAMÁTICA DEL LENGUAJE

Lenguaje:
L = { x op y | x, y ∈ {0,1}+, op ∈ {+, -} }

op puede ser suma (+) o resta (-).
En resta, el proyecto acepta resultados no negativos: x >= y.

Gramática:
S → B O B
O → + | -
B → 0B | 1B | 0 | 1

Alfabeto:
Σ = {0, 1, +, -}

Ejemplos válidos:
101+11
10+1
101-10
1110-101

Ejemplos inválidos:
102+1
101+
+111
10*1
"""
