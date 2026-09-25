import sympy as sp
x = sp.Symbol('x', positive=True)

y = ln *(𝑥2 + 𝑥)

dy_dx = sp.diff(y, x)
print("Похідна функції:", dy_dx)

value_at_2_5 = dy_dx.subs(x, 2.5)
print("Значення похідної в точці x = 2.5:", value_at_2_5.evalf())