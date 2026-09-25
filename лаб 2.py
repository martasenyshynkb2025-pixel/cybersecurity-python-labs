date_str = "01032008"

number = int(date_str)

binary = bin(number)

hexadecimal = hex(number)

bit_length = number.bit_length()

byte_length = (bit_length + 7) // 8

print("Дата народження як число:", number)
print("У двійковій формі:", binary)
print("У шістнадцятковій формі:", hexadecimal)
print("Кількість бітів:", bit_length)
print("Кількість байтів:", byte_length)