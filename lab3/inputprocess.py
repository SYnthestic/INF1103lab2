class InputProcessor:
    def __init__(self):
        self.entry_inp = "0"
        self.inventory_entry = []
        self.failed_entries = 0

    def input_num(self):
        self.entry_inp = input("Enter a number between 0 and 500: ")
        return self.entry_inp