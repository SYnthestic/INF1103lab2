class Processor:
    def __init__(self):
        self.entry_inp = "0"
        self.inventory_entry = []
        self.failed_entries = 0

    def get_valid_input(self):
        print(self.failed_entries)
        if not self.entry_inp.isdigit() and self.entry_inp != "exit":
            print("Invalid input. Please enter a number.")
            self.failed_entries += 1
        elif self.entry_inp == "exit":
            pass
        elif int(self.entry_inp) < 0:
            print("Invalid input. Please enter a non-negative number.")
            self.failed_entries += 1
        elif int(self.entry_inp) > 500:
            print("Invalid input. Please enter a number between 0 and 500.")      
            self.failed_entries += 1  
        elif 0 <= int(self.entry_inp) <= 500:
            self.inventory_entry.append(int(self.entry_inp))
            print(f"Entry {self.entry_inp} added to inventory.")

    def generate_report(self):
        print("Exiting the program.")
        print(f"Total Units Processed: {len(self.inventory_entry)}")
        print(f"Number of Failed/Rejected Entries: {self.failed_entries}")