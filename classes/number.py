class Number:
    @staticmethod
    def ToUnifiedStyleNumber(number):
        if not number:
            return None

        if not isinstance(number, str):
            return None

        if len(number) == 12 and number.startswith('+'):
            number = number[1:]

        if not number.isnumeric():
            return None

        if len(number) == 10:
            number = '7' + number

        if len(number) == 11:
            if number.startswith('8'):
                number = '7' + number[1:]

            if number.startswith('7'):
                return number

        return None

    @staticmethod
    def IsUnifiedStyleNumber(number):
        return number and isinstance(number, str) and number.isnumeric() and len(number) == 11 and number.startswith('7')
