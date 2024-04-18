from re import search


class Factorial:
    """
    This class will calculate a factorial number
        :argument:
            number (int): Number to calculate factorial
    """

    def __init__(self, number):
        self._number = number

    @property
    def number(self):
        """
        Getter Method
        """
        return self._number

    @number.setter
    def number(self, number):
        """
        Setter Method
        """
        if type(number) is int:
            self._number = number
        else:
            raise TypeError('this argument is not int type')

    def factorial(self):
        """
        This method will calculate like a factorial function
            :return:
                result (int): Result of factorial
        """
        if self.number == 1 or self.number == 0:
            return 1
        else:
            result = self.number
            self.number = self.number - 1
            return result * self.factorial()

    def find_zero_in_factorial(self):
        """
        This method will find how many zero at end of the factorial
            :return:
                result (int): Amount of zero at end of factorial
        """
        fact = self.factorial()
        facts = str(fact)
        m = search(pattern=r'(0+$)', string=facts)
        result = m.group(1)
        return len(result)


if __name__ == "__main__":

    number = int(input("Please insert number of factorial: "))
    zero = Factorial(number).find_zero_in_factorial()
    result = f'Amount of zero at end of factorial is {zero}'
    print(result)
