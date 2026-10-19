import sys
from errors import CalculatorError
from tokenizer import Tokenizer
from parser_rpn import RPNParser
from evaluator import Evaluator

def main():
    tokenizer = Tokenizer()
    parser = RPNParser()
    evaluator = Evaluator()

    print("=== Python Tudományos Számológép (RPN / Shunting-Yard) ===")
    print("Támogatott operátorok: +, -, *, /, ^")
    print("Támogatott függvények: sin, cos, tan, sqrt, log, ln, abs")
    print("Támogatott konstansok: pi, e")
    print("Kilépéshez írd be: 'exit' vagy 'quit'\n")

    while True:
        try:
            expr = input("calc> ").strip()
            if not expr:
                continue

            if expr.lower() in ('exit', 'quit', 'q'):
                print("A viszontlátásra!")
                break

            # Adatfolyam (Pipeline)
            tokens = tokenizer.tokenize(expr)
            rpn = parser.parse(tokens)
            result = evaluator.evaluate(rpn)

            # Eredmény formázása (ha egész szám, elhagyjuk a felesleges .0-t)
            if result.is_integer():
                print(f"= {int(result)}")
            else:
                print(f"= {result}")

        except CalculatorError as e:
            print(f"[HIBA] {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nA viszontlátásra!")
            sys.exit(0)
        except Exception as e:
            print(f"[VÁRATLAN HIBA] {e}")

if __name__ == "__main__":
    main()