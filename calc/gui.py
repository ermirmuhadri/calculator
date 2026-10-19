import tkinter as tk
from errors import CalculatorError
from tokenizer import Tokenizer
from parser_rpn import RPNParser
from evaluator import Evaluator

class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tudományos Számológép")
        self.geometry("380x560")
        self.resizable(False, False)
        self.configure(bg="#0f172a")  # Dark slate háttér

        # Pipeline motorok inicializálása
        self.tokenizer = Tokenizer()
        self.parser = RPNParser()
        self.evaluator = Evaluator()

        self._create_widgets()

    def _create_widgets(self):
        # Kijelző (Entry)
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            self,
            textvariable=self.display_var,
            font=("Consolas", 20),
            bg="#1e293b",
            fg="#f8fafc",
            insertbackground="#f8fafc",
            bd=0,
            justify="right"
        )
        self.display.pack(fill="x", padx=15, pady=20, ipady=12)
        self.display.focus_set()
        self.display.bind("<Return>", lambda event: self.calculate())

        # Gombok kerete
        button_frame = tk.Frame(self, bg="#0f172a")
        button_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Egységes, 6 sor x 5 oszlop elrendezés
        buttons_layout = [
            ['C', 'DEL', '(', ')', '^'],
            ['sin', 'cos', 'tan', 'sqrt', '/'],
            ['log', '7', '8', '9', '*'],
            ['ln', '4', '5', '6', '-'],
            ['abs', '1', '2', '3', '+'],
            ['pi', 'e', '0', '.', '=']
        ]

        for row_idx, row in enumerate(buttons_layout):
            button_frame.rowconfigure(row_idx, weight=1)
            for col_idx, text in enumerate(row):
                button_frame.columnconfigure(col_idx, weight=1)
                
                # Színséma a gomb funkciója szerint
                bg_color = "#334155"  # Számok és alapgombok
                fg_color = "#f8fafc"
                
                if text in ('=', '+', '-', '*', '/', '^'):
                    bg_color = "#2563eb"  # Operátorok (Kék)
                elif text in ('C', 'DEL'):
                    bg_color = "#dc2626"  # Törlés (Piros)
                elif text in ('sin', 'cos', 'tan', 'sqrt', 'log', 'ln', 'abs', 'pi', 'e'):
                    bg_color = "#475569"  # Tudományos függvények/konstansok

                btn = tk.Button(
                    button_frame,
                    text=text,
                    font=("Segoe UI", 11, "bold"),
                    bg=bg_color,
                    fg=fg_color,
                    activebackground="#1e293b",
                    activeforeground="#ffffff",
                    bd=0,
                    relief="flat",
                    command=lambda t=text: self._on_button_click(t)
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=2, pady=2)

    def _on_button_click(self, char: str):
        if char == 'C':
            self.display_var.set("")
        elif char == 'DEL':
            current = self.display_var.get()
            self.display_var.set(current[:-1])
        elif char == '=':
            self.calculate()
        elif char in ('sin', 'cos', 'tan', 'sqrt', 'log', 'ln', 'abs'):
            current = self.display_var.get()
            self.display_var.set(current + f"{char}(")
        else:
            current = self.display_var.get()
            self.display_var.set(current + char)
            
        self.display.icursor(tk.END)

    def calculate(self):
        expr = self.display_var.get().strip()
        if not expr:
            return

        try:
            tokens = self.tokenizer.tokenize(expr)
            rpn = self.parser.parse(tokens)
            result = self.evaluator.evaluate(rpn)

            if result.is_integer():
                res_str = str(int(result))
            else:
                res_str = f"{result:.8g}"

            self.display_var.set(res_str)

        except CalculatorError as e:
            self.display_var.set(f"HIBA: {e}")
        except Exception:
            self.display_var.set("SZINTAXIS HIBA")

if __name__ == "__main__":
    app = CalculatorGUI()
    app.mainloop()