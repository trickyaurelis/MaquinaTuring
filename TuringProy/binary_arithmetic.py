class BinaryArithmetic:
    @staticmethod
    def binary_to_decimal(binary: str) -> int:
        decimal = 0
        power = 0

        for bit in reversed(binary):
            if bit == "1":
                decimal += 2 ** power
            power += 1

        return decimal

    @staticmethod
    def decimal_to_binary(number: int) -> str:
        if number == 0:
            return "0"

        result = ""

        while number > 0:
            result = str(number % 2) + result
            number //= 2

        return result

    @staticmethod
    def add_binary(left: str, right: str) -> str:
        a = BinaryArithmetic.binary_to_decimal(left)
        b = BinaryArithmetic.binary_to_decimal(right)
        return BinaryArithmetic.decimal_to_binary(a + b)

    @staticmethod
    def subtract_binary(left: str, right: str) -> str:
        a = BinaryArithmetic.binary_to_decimal(left)
        b = BinaryArithmetic.binary_to_decimal(right)
        if a < b:
            raise ValueError("La resta binaria no puede ser negativa en este simulador.")
        return BinaryArithmetic.decimal_to_binary(a - b)
