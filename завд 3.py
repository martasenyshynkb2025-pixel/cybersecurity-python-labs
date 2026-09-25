

number = 20080301


binary = bin(number)
hexadecimal = hex(number)


bits = number.bit_length()
bytes_count = (bits + 7) // 8  

print("Дата у числовій формі:", number)
print("У двійковій формі:", binary)
print("У шістнадцятковій формі:", hexadecimal)
print("Кількість бітів:", bits)
print("Кількість байтів:", bytes_count)