from errors import ParseError
from operations import OPERATORS, FUNCTIONS, CONSTANTS
from tokenizer import Token

class RPNParser:
    def parse(self, tokens: list[Token]) -> list[Token]:
        output_queue = []
        operator_stack = []

        for token in tokens:
            # 1. Számok azonnal a kimeneti sorba kerülnek
            if token.type == 'NUMBER':
                output_queue.append(token)

            # 2. Konstansok és függvények lekezelése
            elif token.type == 'IDENT':
                val = token.value.lower()
                if val in CONSTANTS:
                    # A konstanst (pl. pi, e) átalakítjuk számmá a kimeneten
                    output_queue.append(Token('NUMBER', str(CONSTANTS[val])))
                elif val in FUNCTIONS:
                    operator_stack.append(token)
                else:
                    raise ParseError(f"Ismeretlen függvény vagy konstans: '{token.value}'")

            # 3. Unáris mínusz (legmagasabb prioritás)
            elif token.type == 'UNARY_MINUS':
                operator_stack.append(token)

            # 4. Bináris operátorok (+, -, *, /, ^)
            elif token.type == 'OP':
                op1 = token.value
                op1_data = OPERATORS[op1]

                while operator_stack:
                    top = operator_stack[-1]
                    if top.type == 'LPAREN':
                        break

                    # Függvények és unáris mínuszok megelőzik a sima bináris operátorokat
                    if top.type in ('IDENT', 'UNARY_MINUS'):
                        output_queue.append(operator_stack.pop())
                        continue

                    if top.type == 'OP':
                        op2 = top.value
                        op2_data = OPERATORS[op2]

                        # Precedencia és asszociativitás vizsgálata
                        if (op1_data['assoc'] == 'L' and op1_data['prec'] <= op2_data['prec']) or \
                           (op1_data['assoc'] == 'R' and op1_data['prec'] < op2_data['prec']):
                            output_queue.append(operator_stack.pop())
                        else:
                            break
                    else:
                        break

                operator_stack.append(token)

            # 5. Nyitó zárójel a verembe
            elif token.type == 'LPAREN':
                operator_stack.append(token)

            # 6. Csukó zárójel esetén ürítjük a vermet a nyitó zárójelig
            elif token.type == 'RPAREN':
                found_lparen = False
                while operator_stack:
                    top = operator_stack.pop()
                    if top.type == 'LPAREN':
                        found_lparen = True
                        break
                    output_queue.append(top)

                if not found_lparen:
                    raise ParseError("Hibás zárójelezés: hiányzó nyitó zárójel '('")

                # Ha a zárójel előtt közvetlenül egy függvény állt (pl. sin(...)), az is átkerül a kimenetre
                if operator_stack and operator_stack[-1].type == 'IDENT':
                    output_queue.append(operator_stack.pop())

        # 7. A megmaradt operátorok átmozgatása a kimenetre
        while operator_stack:
            top = operator_stack.pop()
            if top.type in ('LPAREN', 'RPAREN'):
                raise ParseError("Hibás zárójelezés: hiányzó csukó zárójel ')'")
            output_queue.append(top)

        return output_queue