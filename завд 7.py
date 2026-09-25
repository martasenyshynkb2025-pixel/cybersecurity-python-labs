from decimal import Decimal, getcontext


getcontext().prec = 30


a_float = 4.00000000004
b_float = 4.00000000000
result_float = 4 / (a_float - b_float)


a_dec = Decimal('4.00000000004')
b_dec = Decimal('4.00000000000')
result_dec = Decimal('4') / (a_dec - b_dec)


difference = result_dec - Decimal(result_float)


print("Результат float:", result_float)
print("Результат Decimal:", result_dec)
print("Різниця між Decimal і float:", difference)