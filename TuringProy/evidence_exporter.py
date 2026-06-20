import os
from datetime import datetime


class EvidenceExporter:
    @staticmethod
    def safe_filename(expression):
        return expression.replace("+", "_mas_").replace("-", "_menos_").replace("/", "_")

    @staticmethod
    def export(expression, result, steps, stats, filename=None):
        os.makedirs("evidence", exist_ok=True)

        if filename is None:
            clean = EvidenceExporter.safe_filename(expression)
            filename = f"evidence/evidencia_{clean}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write("EVIDENCIA DE SIMULACIÓN\n")
            file.write("Máquina de Turing para suma y resta binaria\n")
            file.write("=" * 70 + "\n\n")

            file.write(f"Fecha: {datetime.now()}\n")
            file.write(f"Entrada: {expression}\n")
            file.write(f"Resultado: {result}\n")
            file.write(f"Estado final: {stats['estado_final']}\n")
            file.write(f"Cadena aceptada: {stats['aceptada']}\n")
            file.write(f"Pasos ejecutados: {stats['pasos']}\n")
            file.write(f"Movimientos realizados: {stats['movimientos']}\n\n")

            file.write("DESCRIPCIÓN DEL MÉTODO\n")
            file.write("-" * 70 + "\n")
            file.write(
                "La máquina realiza la suma binaria mediante operaciones sucesivas. "
                "Mientras el segundo operando sea mayor que cero, decrementa dicho "
                "operando en una unidad y aumenta el primer operando en una unidad. "
                "Cuando el segundo operando llega a cero, la máquina limpia la cinta "
                "y acepta la cadena dejando únicamente el resultado binario.\n\n"
            )

            file.write("PASOS DE EJECUCIÓN\n")
            file.write("-" * 70 + "\n")

            for step in steps:
                file.write(f"Paso {step.number}\n")
                file.write(f"Estado: {step.state}\n")
                file.write(f"Cinta: {' '.join(step.tape)}\n")
                file.write(f"Cabezal: {step.head}\n")
                file.write(f"Lee: {step.read}\n")
                file.write(f"Escribe: {step.write}\n")
                file.write(f"Movimiento: {step.move}\n")
                file.write(f"Descripción: {step.description}\n")
                file.write("-" * 70 + "\n")

            file.write("\nCONCLUSIÓN DE LA PRUEBA\n")
            file.write("-" * 70 + "\n")

            if stats["aceptada"] == "Sí":
                file.write(
                    "La cadena fue aceptada porque pertenece al lenguaje definido "
                    "L = { x + y | x,y ∈ {0,1}+ } y la máquina obtuvo correctamente "
                    "el resultado de la suma binaria.\n"
                )
            else:
                file.write(
                    "La cadena fue rechazada porque no cumple con el lenguaje definido "
                    "o contiene símbolos que no pertenecen al alfabeto permitido.\n"
                )

        return filename