
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""


class NumToTxtThai:
    """
    This class will provide about how to convert number to Thai text
        :argument:
            number : Number that want to convert
    """

    def __init__(self, number):
        self._number = float(number.replace(",", ""))
        if not 0 <= self.number < 10000000:
            raise ValueError("Input must be between 0 and 9,999,999")

        self.num_text = {
            '0': "ศูนย์",
            '1': "หนึ่ง",
            '2': "สอง",
            '3': "สาม",
            '4': "สี่",
            '5': "ห้า",
            '6': "หก",
            '7': "เจ็ด",
            '8': "แปด",
            '9': "เก้า" ,
            '10': "สิบ" ,
            '100': "ร้อย" ,
            '1000': "พัน" ,
            '10000': "หมื่น",
            '1000000': "ล้าน",
        }

    @property
    def number(self):
        """
        Getter method
        """
        return self._number

    @number.setter
    def number(self, number):
        """
        Setter method
        """
        self._number = number

    def float_to_thai(self):
        """
        This method will provide prepare data before convert to Thai text
            :return:
                thai_text : Thai text
        """

        num_str = str(self.number)
        num_decimals = 0
        if '.' in num_str:
            num_decimals = len(num_str.split('.')[1])
        else:
            num_decimals = 0

        if num_decimals > 0:
            num_str = "{:.{}f}".format(self.number, num_decimals).rstrip('0').rstrip('.')

        parts = num_str.split('.')
        int_part = parts[0]
        if len(parts) > 1:
            dec_part = parts[1]
        else:
            dec_part = '0'
        thai_int = self.int_to_thai(int(int_part))
        thai_dec = self.dec_to_thai(dec_part)
        if thai_dec:
            thai_text = thai_int + "จุด" + thai_dec
        else:
            thai_text = thai_int
        return thai_text

    def int_to_thai(self, number):
        """
        This method will convert integer to Thai text
            :param:
                number (int): Integer number convert to Thai text
            :return:
                thai_text : Thai text convert from integer number
        """
        if number == 0:
            return self.num_text['0']
        if number < 10:
            return self.num_text[str(number)]
        thai_text = ''
        unit_values = [(1000000, 'ล้าน'), (100000, 'แสน'), (10000, 'หมื่น'),
                    (1000, 'พัน'), (100, 'ร้อย'), (10, 'สิบ'), (1, '')]
        for unit, text in unit_values:
            if number >= unit:
                digit = number // unit
                number %= unit
                if digit == 1:
                    if unit == 10:
                        thai_text += "สิบ"
                    elif unit == 1 and number == 0:
                        thai_text += "เอ็ด"
                    else:
                        thai_text += self.num_text[str(digit)] + text
                elif digit == 2 and unit == 10:
                    thai_text += "ยี่สิบ"
                elif digit > 0:
                    thai_text += self.num_text[str(digit)] + text
        return thai_text

    def dec_to_thai(self, number):
        """
        This method will convert decimal number to Thai text
            :param:
                number : Number in decimal form to convert to Thai text
            :return:
                 thai_text : Thai text convert from decimal number
        """
        if number == "0":
            return ''
        thai_text = ''
        for digit in number:
            thai_text += self.num_text[digit]
        return thai_text


if __name__ == "__main__":
    txt = 'Please insert number for covert to Thai language: '
    number = input(txt)
    try:
        thai_text = NumToTxtThai(number).float_to_thai()
        ans = f'Thai text of {number} is " {thai_text} "'
        print(ans)
    except ValueError as e:
        print(f"{number}: {e}")
