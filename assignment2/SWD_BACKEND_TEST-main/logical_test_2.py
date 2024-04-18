
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""


class NumberToRoman:
    def __init__(self, number):
        self._number = int(number.replace(',', ''))
        if not 0 < self.number <= 1000:
            raise ValueError('Input number must between 0 and 1,000')
        self.roman = {
            'm': ["", "M"],
            'c': ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"],
            'x': ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"],
            'i': ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
        }

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    def number_to_roman(self):
        thousands = self.roman['m'][self.number // 1000]
        hundreds = self.roman['c'][(self.number % 1000) // 100]
        tens = self.roman['x'][(self.number % 100) // 10]
        ones = self.roman['i'][self.number % 10]
        result = thousands + hundreds + tens + ones
        return result


if __name__ == "__main__":
    txt = 'Please insert number convert to roman numerals: '
    number = input(txt)
    try:
        result = NumberToRoman(number).number_to_roman()
        ans = f'The roman numerals of {number} is " {result} "'
        print(ans)
    except ValueError as e:
        print(f'{number}: {e}')
