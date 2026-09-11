entry_inp = "0"
inventory_entry = []
failed_entries = 0


while entry_inp != "exit":
    entry_inp = input("Enter a number between 0 and 500: ")
    if not entry_inp.isdigit() and entry_inp != "exit":
        print("Invalid input. Please enter a number.")
        failed_entries += 1
    elif entry_inp == "exit":
        print("Exiting the program.")
        print(f"Total Units Processed: {len(inventory_entry)}")
        print(f"Number of Failed/Rejected Entries: {failed_entries}")
    elif int(entry_inp) < 0:
        print("Invalid input. Please enter a non-negative number.")
        failed_entries += 1
    elif int(entry_inp) > 500:
        print("Invalid input. Please enter a number between 0 and 500.")      
        failed_entries += 1  
    elif 0 <= int(entry_inp) <= 500:
        inventory_entry.append(int(entry_inp))
        print(f"Entry {entry_inp} added to inventory.")
