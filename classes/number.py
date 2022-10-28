class Number:
    @staticmethod
    def ToUnifiedStyleNumber(number):
        if not number:
            return None

        if not isinstance(number, str):
            return None

        number = number.strip()

        if number.startswith('8'):
            number = number[1:]

        if len(number) == 10:
            number = '7' + number

        if len(number) == 11:
            number = '+' + number

        if len(number) == 12:
            if number.startswith('+') and number[1:].isnumeric():
                return number

        return None

    @staticmethod
    def IsUnifiedStyleNumber(number):
        return number and isinstance(number, str) and number.startswith('+') and number[1:].isnumeric() and len(number) == 12
