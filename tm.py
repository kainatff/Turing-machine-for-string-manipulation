import tkinter as tk

class TuringMachine:
    def __init__(self, tape=""):
        self.tape = list(tape)
        self.head_position = 0
        self.state = 'idle'

    def move_head_left(self):
        if self.head_position > 0:
            self.head_position -= 1
            return True
        return False

    def move_head_right(self):
        self.head_position += 1
        if self.head_position == len(self.tape):
            self.tape.append('_')
        return True

    def write_symbol(self, symbol):
        if len(self.tape) > self.head_position:
            self.tape[self.head_position] = symbol
        else:
            self.tape.append(symbol)

    def read_symbol(self):
        if len(self.tape) > self.head_position:
            return self.tape[self.head_position]
        return '_'

    def reverse_string(self):
        self.tape = self.tape[::-1]

    def count_letters(self):
        count = sum(1 for char in self.tape if char.isalpha())
        self.tape = [str(count)]

    def is_palindrome(self):
        alphanumeric_tape = [char.lower() for char in self.tape if char.isalnum()]
        return alphanumeric_tape == alphanumeric_tape[::-1]

    def convert_to_lower(self):
        self.tape = [char.lower() for char in self.tape]

    def convert_to_upper(self):
        self.tape = [char.upper() for char in self.tape]

    def exit(self):
        self.master.quit()

    def process_operations(self, operations, callback, verdict_callback=None):
        if operations:
            operation, *params = operations.pop(0)
            func = getattr(self, operation)
            if params:
                func(*params)
            else:
                func()
            callback()
            if operation == 'is_palindrome' and verdict_callback:
                verdict_callback(self.is_palindrome())
            self.set_master(self.master)
            self.master.after(300, lambda: self.process_operations(operations, callback, verdict_callback))

    def set_master(self, master):
        self.master = master

class TuringMachineGUI:
    def __init__(self, master):
        self.master = master
        master.title("Turing Machine")

        self.label = tk.Label(master, text="Input String:")
        self.label.grid(row=0, column=0)

        self.input_entry = tk.Entry(master)
        self.input_entry.grid(row=0, column=1)

        self.reverse_button = tk.Button(master, text="Reverse", command=lambda: self.start_machine('reverse_string'))
        self.reverse_button.grid(row=1, column=0)

        self.count_letters_button = tk.Button(master, text="Count Letters", command=lambda: self.start_machine('count_letters'))
        self.count_letters_button.grid(row=1, column=1)

        self.is_palindrome_button = tk.Button(master, text="Check Palindrome", command=lambda: self.start_machine('is_palindrome'))
        self.is_palindrome_button.grid(row=2, column=0)

        self.lowercase_button = tk.Button(master, text="Convert to Lowercase", command=lambda: self.start_machine('convert_to_lower'))
        self.lowercase_button.grid(row=2, column=1)

        self.uppercase_button = tk.Button(master, text="Convert to Uppercase", command=lambda: self.start_machine('convert_to_upper'))
        self.uppercase_button.grid(row=3, column=0)

        self.exit_button = tk.Button(master, text="Exit", command=lambda: self.start_machine('exit'))
        self.exit_button.grid(row=3, column=1)

        self.result_label = tk.Label(master, text="")
        self.result_label.grid(row=4, column=0, columnspan=2)

        self.tape_frame = tk.Frame(master)
        self.tape_frame.grid(row=5, column=0, columnspan=2)

        self.tm = TuringMachine()
        self.tm.set_master(master)
        self.update_tape_display()

    def update_tape_display(self):
        for widget in self.tape_frame.winfo_children():
            widget.destroy()
        for i, symbol in enumerate(self.tm.tape):
            label = tk.Label(self.tape_frame, text=symbol, width=2, borderwidth=1, relief="solid")
            label.grid(row=0, column=i)
            if i == self.tm.head_position:
                label.config(bg='lightgreen')

    def start_machine(self, operation, *params):
        input_str = self.input_entry.get()
        self.tm = TuringMachine(input_str)
        self.tm.set_master(self.master)
        operations = [('move_head_right',) for _ in range(len(input_str))]  # Move to the end of the string initially
        operations.append((operation, *params))
        if operation in ['reverse_string']:
            operations.extend([('move_head_left',) for _ in range(len(input_str))])  # Optionally move back to start
        self.clear_verdict()
        self.tm.process_operations(operations, self.update_tape_display, self.show_verdict)

    def show_verdict(self, is_palindrome):
        if is_palindrome:
            self.result_label.config(text="The input is a palindrome.")
        else:
            self.result_label.config(text="The input is not a palindrome.")

    def clear_verdict(self):
        self.result_label.config(text="")

root = tk.Tk()
app = TuringMachineGUI(root)
root.mainloop()