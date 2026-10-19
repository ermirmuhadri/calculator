
import math
from errors import EvaluateError
from operations import OPERATORS, FUNCTIONS
from tokenizer import Token

class Evaluator:
    def evaluate(self, rpn_tokens: list[Token]) -> float:
        stack = []

        for token in rpn_tokens:
            if token.type == 'NUMBER':
                stack.append(float(token.value))

            elif token.type == 'UNARY_MINUS':
                if not stack:
                    raise EvaluateError("Hibás kifejezés: hiányzó operandus az unáris mínuszhoz.")
                val = stack.pop()
                stack.append(-val)

            elif token.type == 'OP':
                if len(stack) < 2:
                    raise EvaluateError(f"Hibás kifejezés: hiányzó operandus a(z) '{token.value}' művelethez.")
                b = stack.pop()
                a = stack.pop()

                try:
                    func = OPERATORS[token.value]['func']
                    res = func(a, b)
                except ZeroDivisionError:
                    raise EvaluateError("Nullával való osztás nem megengedett!")
                except Exception as e:
                    raise EvaluateError(f"Matematikai hiba a művelet végrehajtásakor: {e}")

                stack.append(res)

            elif token.type == 'IDENT':
                func_name = token.value.lower()
                if func_name not in FUNCTIONS:
                    raise EvaluateError(f"Ismeretlen függvény: '{token.value}'")

                if not stack:
                    raise EvaluateError(f"Hiányzó argumentum a(z) '{func_name}' függvényhez.")
                arg = stack.pop()

                try:
                    res = FUNCTIONS[func_name](arg)
                except ValueError as e:
                    raise EvaluateError(f"Érvénytelen argumentum a(z) '{func_name}' függvényhez (pl. negatív gyök vagy logaritmus): {e}")
                except Exception as e:
                    raise EvaluateError(f"Matematikai hiba a(z) '{func_name}' kiszámításakor: {e}")

                stack.append(res)

        if len(stack) != 1:
            raise EvaluateError("Érvénytelen kifejezés: túl sok operandus maradt a veremben.")

        return stack[0]