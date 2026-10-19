import math

# Operátorok precedenciája, asszociativitása és matematikai logikája
# 'L' = Balról jobbra (pl. 10 - 2 - 1 -> (10 - 2) - 1)
# 'R' = Jobbról balra (pl. 2 ^ 3 ^ 2 -> 2 ^ (3 ^ 2))
OPERATORS = {
    '+': {'prec': 1, 'assoc': 'L', 'func': lambda a, b: a + b},
    '-': {'prec': 1, 'assoc': 'L', 'func': lambda a, b: a - b},
    '*': {'prec': 2, 'assoc': 'L', 'func': lambda a, b: a * b},
    '/': {'prec': 2, 'assoc': 'L', 'func': lambda a, b: a / b},
    '^': {'prec': 3, 'assoc': 'R', 'func': lambda a, b: a ** b},
}

# Támogatott matematikai függvények (1 argumentumosak)
FUNCTIONS = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log10,  # 10-es alapú logaritmus
    'ln': math.log,     # Természetes logaritmus
    'abs': abs,
}

# Beépített konstansok
CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
}
