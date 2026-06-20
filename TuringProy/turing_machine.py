from binary_validator import BinaryValidator
from binary_arithmetic import BinaryArithmetic


class TuringStep:
    def __init__(self, number, state, tape, head, read, write, move, description):
        self.number = number
        self.state = state
        self.tape = tape.copy()
        self.head = head
        self.read = read
        self.write = write
        self.move = move
        self.description = description


class TuringMachine:
    BLANK = "□"

    def __init__(self):
        self.reset()

    def reset(self):
        self.expression = ""
        self.operator = "+"
        self.tape = []
        self.head = 0
        self.state = "q0"
        self.steps = []
        self.accepted = False
        self.result = ""
        self.error = ""

    def load(self, expression: str):
        self.reset()
        self.expression = expression.strip()

        valid, message = BinaryValidator.validate(self.expression)
        if not valid:
            self.error = message
            self.state = "qr"
            self.tape = list(self.expression) if self.expression else [self.BLANK]
            self.head = 0
            self._record("qr", "?", "?", "N", message)
            return False

        self.operator = "+" if "+" in self.expression else "-"
        self.tape = [self.BLANK] + list(self.expression) + [self.BLANK]
        self.head = 1
        self.state = "q0"
        return True

    def run(self, max_steps=30000):
        if self.state == "qr":
            return self.steps

        if self.operator == "+":
            return self._run_addition(max_steps)
        return self._run_subtraction(max_steps)

    def _run_addition(self, max_steps):
        self._seek_right_blank()

        while True:
            if self._limit_exceeded(max_steps):
                break

            if not self._right_operand_has_one():
                self._cleanup()
                self._accept("Estado final de aceptación. Resultado binario de la suma: {}")
                break

            self._go_to_right_blank()
            self._decrement_right_operand()
            self._go_to_operator()
            self._increment_left_operand()
            self._go_to_right_blank()

        return self.steps

    def _run_subtraction(self, max_steps):
        self._seek_right_blank()

        while True:
            if self._limit_exceeded(max_steps):
                break

            if not self._right_operand_has_one():
                self._cleanup()
                self._accept("Estado final de aceptación. Resultado binario de la resta: {}")
                break

            self._go_to_right_blank()
            self._decrement_right_operand()
            self._go_to_operator()
            if not self._decrement_left_operand():
                self.accepted = False
                self.state = "qr"
                self.result = "ERROR"
                self.error = "La resta produce un valor negativo. Se requiere que el primer operando sea mayor o igual al segundo."
                self._record("qr", self._read(), self._read(), "N", self.error)
                break
            self._go_to_right_blank()

        return self.steps

    def _limit_exceeded(self, max_steps):
        if len(self.steps) > max_steps:
            self.error = "Se excedió el límite máximo de pasos."
            self.state = "qr"
            self._record("qr", self._read(), self._read(), "N", self.error)
            return True
        return False

    def _accept(self, message_template):
        self.accepted = True
        self.state = "qf"
        self.result = self._extract_result()
        self._normalize_final_tape()
        self._record("qf", self._read(), self._read(), "N", message_template.format(self.result))

    def stats(self):
        return {
            "entrada": self.expression,
            "resultado": self.result if self.accepted else "ERROR",
            "estado_final": self.state,
            "aceptada": "Sí" if self.accepted else "No",
            "pasos": len(self.steps),
            "movimientos": len([s for s in self.steps if s.move in ("L", "R")]),
            "operacion": "Suma" if self.operator == "+" else "Resta",
        }

    def _ensure_tape_limits(self):
        if self.head < 0:
            self.tape.insert(0, self.BLANK)
            self.head = 0
        if self.head >= len(self.tape):
            self.tape.append(self.BLANK)

    def _read(self):
        self._ensure_tape_limits()
        return self.tape[self.head]

    def _write(self, symbol):
        self._ensure_tape_limits()
        self.tape[self.head] = symbol

    def _record(self, state, read, write, move, description):
        self.steps.append(TuringStep(len(self.steps) + 1, state, self.tape, self.head, read, write, move, description))

    def _transition(self, state, write, move, description):
        read = self._read()
        self._write(write)
        if move == "R":
            self.head += 1
        elif move == "L":
            self.head -= 1
        self._ensure_tape_limits()
        self.state = state
        self._record(state, read, write, move, description)

    def _seek_right_blank(self):
        while self._read() != self.BLANK:
            self._transition("q_seek_end", self._read(), "R", "Avanza hacia el blanco final de la cinta.")
        self._record("q_check_start", self._read(), self._read(), "N", "Cabezal ubicado al final del segundo operando.")

    def _right_operand_has_one(self):
        self._transition("q_check_right", self.BLANK, "L", "Revisa si el segundo operando todavía es mayor que cero.")
        while True:
            symbol = self._read()
            if symbol == "1":
                self._record("q_check_found_one", symbol, symbol, "N", "Se encontró un 1 en el segundo operando.")
                return True
            if symbol == "0":
                self._transition("q_check_right", "0", "L", "Continúa buscando un 1 en el segundo operando.")
            elif symbol in ("+", "-"):
                self._record("q_check_zero", symbol, symbol, "N", "El segundo operando ya vale cero.")
                return False
            else:
                self.error = f"Símbolo inesperado durante revisión: {symbol}"
                self.state = "qr"
                self._record("qr", symbol, symbol, "N", self.error)
                return False

    def _go_to_right_blank(self):
        while self._read() != self.BLANK:
            self._transition("q_return_end", self._read(), "R", "Regresa al extremo derecho de la cinta.")
        self._record("q_at_end", self._read(), self._read(), "N", "Cabezal listo en el extremo derecho.")

    def _decrement_right_operand(self):
        self._transition("q_dec_start", self.BLANK, "L", "Comienza decremento del segundo operando.")
        while True:
            symbol = self._read()
            if symbol == "1":
                self._transition("q_dec_done", "0", "N", "Decremento terminado: cambia 1 por 0.")
                return True
            if symbol == "0":
                self._transition("q_dec_borrow", "1", "L", "Préstamo binario: cambia 0 por 1 y continúa.")

    def _go_to_operator(self):
        while self._read() not in ("+", "-"):
            self._transition("q_seek_op", self._read(), "L", "Busca el operador de la expresión.")
        self._record("q_operator", self._read(), self._read(), "N", f"Operador '{self._read()}' localizado.")

    def _increment_left_operand(self):
        self._transition("q_inc_start", self._read(), "L", "Comienza incremento del primer operando.")
        while True:
            symbol = self._read()
            if symbol == "0":
                self._transition("q_inc_done", "1", "N", "Incremento terminado: cambia 0 por 1.")
                return True
            if symbol == "1":
                self._transition("q_inc_carry", "0", "L", "Acarreo binario: cambia 1 por 0 y continúa.")
            elif symbol == self.BLANK:
                self._transition("q_inc_extend", "1", "N", "Acarreo final: escribe 1 al inicio.")
                return True

    def _decrement_left_operand(self):
        self._transition("q_sub_start", self._read(), "L", "Comienza decremento del primer operando para realizar la resta.")
        while True:
            symbol = self._read()
            if symbol == "1":
                self._transition("q_sub_done", "0", "N", "Decremento del primer operando terminado: cambia 1 por 0.")
                return True
            if symbol == "0":
                self._transition("q_sub_borrow", "1", "L", "Préstamo en el primer operando: cambia 0 por 1 y continúa.")
            elif symbol == self.BLANK:
                return False

    def _cleanup(self):
        while self._read() not in ("+", "-") and self._read() != self.BLANK:
            self._transition("q_seek_cleanup", self._read(), "R", "Avanza hasta el operador para iniciar limpieza.")
        while self._read() != self.BLANK:
            self._transition("q_cleanup", self.BLANK, "R", "Borra operador y ceros restantes del segundo operando.")
        self._record("q_cleanup_done", self.BLANK, self.BLANK, "N", "Limpieza terminada.")

    def _extract_result(self):
        # Se toma únicamente la parte izquierda antes del operador o blanco de limpieza.
        chars = []
        for s in self.tape:
            if s in ("+", "-"):
                break
            if s in ("0", "1"):
                chars.append(s)
        result = "".join(chars).lstrip("0")
        return result if result else "0"

    def _normalize_final_tape(self):
        self.tape = [self.BLANK] + list(self.result) + [self.BLANK]
        self.head = len(self.tape) - 1

    @staticmethod
    def transition_table():
        return [
            ("q_seek_end", "0,1,+,-", "mismo", "R", "q_seek_end"),
            ("q_seek_end", "□", "□", "N", "q_check_start"),
            ("q_check_right", "0", "0", "L", "q_check_right"),
            ("q_check_right", "1", "1", "N", "q_check_found_one"),
            ("q_check_right", "+,-", "mismo", "N", "q_check_zero"),
            ("q_return_end", "0,1,+,-", "mismo", "R", "q_return_end"),
            ("q_dec_borrow", "0", "1", "L", "q_dec_borrow"),
            ("q_dec_borrow", "1", "0", "N", "q_dec_done"),
            ("q_seek_op", "0,1", "mismo", "L", "q_seek_op"),
            ("q_seek_op", "+,-", "mismo", "N", "q_operator"),
            ("q_inc_carry", "1", "0", "L", "q_inc_carry"),
            ("q_inc_carry", "0", "1", "N", "q_inc_done"),
            ("q_inc_carry", "□", "1", "N", "q_inc_extend"),
            ("q_sub_borrow", "0", "1", "L", "q_sub_borrow"),
            ("q_sub_borrow", "1", "0", "N", "q_sub_done"),
            ("q_sub_borrow", "□", "□", "N", "qr"),
            ("q_cleanup", "+,-,0", "□", "R", "q_cleanup"),
            ("q_cleanup", "□", "□", "N", "qf"),
        ]

    @staticmethod
    def formal_delta_text():
        text = "FUNCIÓN DE TRANSICIÓN FORMAL δ\n\n"
        for state, read, write, move, next_state in TuringMachine.transition_table():
            text += f"δ({state}, {read}) = ({next_state}, {write}, {move})\n"
        return text
