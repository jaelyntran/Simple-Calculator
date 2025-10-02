import tkinter as tk
from simple_calculator_logic import calculate_expression, parse_equation


class SimpleCalculator(tk.Tk):
    def __init__(self, history):
        super().__init__()
        self.history = history

        self.title("Simple Calculator")
        self.geometry("400x600")
        self.minsize(300, 450)
        self.configure(bg="white")

        self.result_var = tk.StringVar()
        self.equation_var = tk.StringVar()
        self.history_listbox = tk.Listbox()
        self.bind("<Return>", self.on_equals)

        self.create_widgets()

    def create_widgets(self):
        # Top equation display (borderless label)
        equation_label = tk.Label(self,
                                  textvariable=self.equation_var,
                                  font=("Helvetica", 25),
                                  anchor="e",
                                  bg="white",
                                  fg="#555555")
        equation_label.grid(row=0, column=0, columnspan=4,
                            sticky="nsew", padx=20, pady=(5, 0))

        display = tk.Entry(self,
                           textvariable=self.result_var,
                           font=("Helvetica", 40),
                           bd=3,
                           relief="sunken",
                           justify="right")
        display.grid(row=1, column=0, columnspan=4,
                     sticky="nsew", padx=20, pady=(0, 15), ipady=10)

        # Button configuration
        buttons = [
            ('C', '#f28b82'), ('+/-', '#fbbc04'), ('%', '#fbbc04'), ('/', '#fbbc04'),
            ('7', '#ffffff'), ('8', '#ffffff'), ('9', '#ffffff'), ('*', '#fbbc04'),
            ('4', '#ffffff'), ('5', '#ffffff'), ('6', '#ffffff'), ('-', '#fbbc04'),
            ('1', '#ffffff'), ('2', '#ffffff'), ('3', '#ffffff'), ('+', '#fbbc04'),
            ('0', '#ffffff', 2), ('.', '#ffffff'), ('=', '#34a853')
        ]

        # Place buttons in grid
        row_index = 2
        col_index = 0
        for b in buttons:
            text, color = b[0], b[1]
            colspan = b[2] if len(b) > 2 else 1

            if text == 'C':
                cmd = self.clear
            elif text == '+/-':
                cmd = self.sign_inverse
            elif text == '=':
                cmd = self.on_equals
            else:
                cmd = lambda t=text: self.button_click(t)

            btn = tk.Button(self,
                            text=text,
                            bg=color,
                            font=("Helvetica", 18),
                            fg="#000000" if text not in ('=', '/', '*', '-', '+') else "#ffffff",
                            command=cmd)

            left_pad = 20 if col_index == 0 else 5
            right_pad = 20 if col_index + colspan - 1 == 3 else 5

            btn.grid(row=row_index, column=col_index, columnspan=colspan,
                     sticky="nsew", padx=(left_pad, right_pad), pady=(5, 0))

            col_index += colspan
            if col_index > 3:
                col_index = 0
                row_index += 1

        history_label = tk.Label(self,
                                 text="History",
                                font=("Helvetica", 16, "bold"),
                                bg="white",
                                fg="#555555",
                                anchor="w")
        history_label.grid(row=row_index, column=0, columnspan=4,
                           sticky="nsew", padx=20, pady=(5, 0))

        self.history_listbox = tk.Listbox(self,
                                          height=5,
                                          font=("Helvetica", 14),
                                          relief="groove",
                                          activestyle='none')
        self.history_listbox.grid(row=row_index + 1, column=0, columnspan=4,
                                  sticky="nsew", padx=20, pady=(0, 20))

        # Configure grid weights for responsive resizing
        for i in range(row_index + 1):
            self.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.grid_columnconfigure(j, weight=1)

    # --- Calculator logic ---
    def sign_inverse(self):
        cur_text = self.result_var.get()
        if cur_text == '':
            self.result_var.set('-')
        elif cur_text.startswith('-'):
            self.result_var.set(cur_text[1:])
        else:
            try:
                val = float(cur_text)
                val *= -1
                if val.is_integer():
                    val = int(val)
                self.result_var.set(str(val))
            except ValueError:
                self.show_error("Invalid input")

    def button_click(self, text):
        cur_text = self.result_var.get()
        if cur_text == '' and text in '+*/%':
            return
        self.result_var.set(cur_text + text)

    def on_equals(self, event=None):
        user_input = self.result_var.get()
        try:
            expression = parse_equation(user_input)
            result = calculate_expression(expression)
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 8)
            self.result_var.set(result)
            self.equation_var.set(user_input)

            self.history.append(f"{user_input} = {result}")
            if len(self.history) > 5:
                self.history.pop(0)

            self.update_history_listbox()
        except Exception as e:
            self.show_error(str(e))

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for text in self.history:
            self.history_listbox.insert(tk.END, text)

    def clear(self):
        self.result_var.set('')
        self.equation_var.set('')

    def show_error(self, msg):
        top = tk.Toplevel(self)
        top.title("Error")
        tk.Label(top, text=msg, padx=20, pady=20).pack()
        tk.Button(top, text="OK", command=top.destroy).pack(pady=10)