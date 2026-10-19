import re
from errors import LexicalError

class Token:
    def __init__(self, type_: str, value: str):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Tokenizer:
    # Token típusok reguláris kifejezései
    TOKEN_SPECIFICATION = [
        ('NUMBER',   r'\d+(\.\d+)?'),  # Egész vagy lebegőpontos számok
        ('IDENT',    r'[a-zA-Z_]\w*'), # Függvények (sin, cos) vagy konstansok (pi, e)
        ('OP',       r'[+\-*/^]'),     # Műveleti jelek
        ('LPAREN',   r'\('),           # Nyitó zárójel
        ('RPAREN',   r'\)'),           # Zárójel bezárása
        ('SKIP',     r'\s+'),          # Szóközök (figyelmen kívül hagyjuk)
        ('MISMATCH', r'.'),            # Ismeretlen karakterek (hibadobás)
    ]

    def __init__(self):
        # Összeállítunk egyetlen kombinált regex mintát a csoportnevek alapján
        tok_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.TOKEN_SPECIFICATION)
        self.regex = re.compile(tok_regex)

    def tokenize(self, expression: str) -> list[Token]:
        raw_tokens = []
        for match in self.regex.finditer(expression):
            kind = match.lastgroup
            value = match.group()

            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise LexicalError(f"Ismeretlen karakter a kifejezésben: '{value}'")
            else:
                raw_tokens.append(Token(kind, value))

        return self._process_unary_operators(raw_tokens)

    def _process_unary_operators(self, tokens: list[Token]) -> list[Token]:
        """
        Megkülönbözteti a kivonást (-) az unáris mínusztól (negatív előjel).
        Ha a '-' az első token, vagy 'OP' / 'LPAREN' után áll, átnevezzük 'UNARY_MINUS'-ra.
        """
        processed = []
        for i, token in enumerate(tokens):
            if token.type == 'OP' and token.value == '-':
                # Unáris mínusz feltétele: a kifejezés elején van, vagy egy operátor/nyitó zárójel után áll
                is_unary = (i == 0) or (tokens[i - 1].type in ('OP', 'LPAREN'))
                if is_unary:
                    processed.append(Token('UNARY_MINUS', 'u-'))
                    continue
            processed.append(token)
        return processed