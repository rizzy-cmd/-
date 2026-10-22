#1.Лексер
def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]

        # Пропускаем пробелы
        if char == ' ':
            i += 1
            continue

        # Если это цифра или точка (число)
        if char.isdigit() or char == '.':
            num_str = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            # Превращаем строку в число (int или float)
            num = float(num_str) if '.' in num_str else int(num_str)
            tokens.append(('NUMBER', num))
            continue

        # Если это слово (например, fact)
        if char.isalpha():
            word = ""
            while i < len(expression) and expression[i].isalpha():
                word += expression[i]
                i += 1
            if word == 'fact':
                tokens.append(('FACT', word))
            else:
                raise ValueError(f"Неизвестное слово: {word}")
            continue

        # Операторы
        if char in '+-*/':
            tokens.append(('OP', char))
            i += 1
            continue

        # Оператор == (два символа)
        if char == '=' and i + 1 < len(expression) and expression[i + 1] == '=':
            tokens.append(('OP', '=='))
            i += 2
            continue

        # Скобки
        if char in '()':
            tokens.append(('BRACKET', char))
            i += 1
            continue

        raise ValueError(f"Недопустимый символ: {char}")

    tokens.append(('EOF', 'EOF'))  # Конец файла
    return tokens
#=======================================================================================================================
#Парсер
def parse_expression(tokens, pos):
    # Самый низкий приоритет - это ==
    left = parse_additive(tokens, pos)
    while tokens[pos[0]][0] == 'OP' and tokens[pos[0]][1] == '==':
        pos[0] += 1
        right = parse_additive(tokens, pos)
        left = 1 if left == right else 0
    return left


def parse_additive(tokens, pos):
    # Сложение и вычитание
    left = parse_term(tokens, pos)
    while tokens[pos[0]][0] == 'OP' and tokens[pos[0]][1] in '+-':
        op = tokens[pos[0]][1]
        pos[0] += 1
        right = parse_term(tokens, pos)
        if op == '+':
            left += right
        else:
            left -= right
    return left


def parse_term(tokens, pos):
    # Умножение и деление
    left = parse_factor(tokens, pos)
    while tokens[pos[0]][0] == 'OP' and tokens[pos[0]][1] in '*/':
        op = tokens[pos[0]][1]
        pos[0] += 1
        right = parse_factor(tokens, pos)
        if op == '*':
            left *= right
        else:
            if right == 0:
                raise ValueError("Деление на ноль")
            left /= right
    return left


def parse_factor(tokens, pos):
    # Числа, скобки, унарный минус и fact()
    token = tokens[pos[0]]

    # Число
    if token[0] == 'NUMBER':
        pos[0] += 1
        return token[1]

    # Скобки
    if token[0] == 'BRACKET' and token[1] == '(':
        pos[0] += 1
        result = parse_expression(tokens, pos)
        if tokens[pos[0]][0] != 'BRACKET' or tokens[pos[0]][1] != ')':
            raise ValueError("Не закрыта скобка")
        pos[0] += 1
        return result

    # Унарный минус (например, -5)
    if token[0] == 'OP' and token[1] == '-':
        pos[0] += 1
        return -parse_factor(tokens, pos)

    # Унарный плюс (например, +5)
    if token[0] == 'OP' and token[1] == '+':
        pos[0] += 1
        return parse_factor(tokens, pos)

    # Функция fact()
    if token[0] == 'FACT':
        pos[0] += 1
        if tokens[pos[0]][0] != 'BRACKET' or tokens[pos[0]][1] != '(':
            raise ValueError("После fact должна идти скобка")
        pos[0] += 1

        val = parse_expression(tokens, pos)

        if tokens[pos[0]][0] != 'BRACKET' or tokens[pos[0]][1] != ')':
            raise ValueError("Не закрыта скобка в fact()")
        pos[0] += 1

        if isinstance(val, float):
            if not val.is_integer():
                raise ValueError("Факториал только для целых чисел")
        if val < 0:
            raise ValueError("Факториал отрицательного числа")
        num = int(val) # На случай если число - float без остатка, переводит в целое
        res = 1
        for i in range(2, num + 1):
            res *= i
        return res

    raise ValueError(f"Неожиданный символ: {token}")
#======================================================================================================================
# Главная функция вычисления
def calculate(expression):
    if not expression.strip():
        return 0
    tokens = tokenize(expression)
    pos = [0]  # Храним текущую позицию в списке
    result = parse_expression(tokens, pos)

    # Проверяем, что дошли до конца (нет лишних скобок)
    if tokens[pos[0]][0] != 'EOF':
        raise ValueError("Ошибка в выражении (лишние символы)")

    # Если результат 5.0, делаем его 5
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    return result
#======================================================================================================================
# Запуск калькулятора

print("Введите выражение (или 'exit'):")
while True:
    expr = input("> ")
    if expr == 'exit': break
    try: print("Результат:", calculate(expr))
    except Exception as e: print("Ошибка:", e)


