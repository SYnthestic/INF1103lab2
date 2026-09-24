entry_inp = "0"
inventory_entry = []
failed_entries = 0
delivery_amount = 0

def get_valid_input(failed_entries, delivery_amount, inventory_entry, entry_inp):
    if entry_inp == "exit":
        tax_amount = calculate_tax(delivery_amount)
        print("Delivery Amount:", delivery_amount)
        print(f"Total tax amount: {tax_amount}")
    elif not entry_inp.isdigit():
        print("Invalid input. Please enter a non-negative number.")
        failed_entries += 1
    elif int(entry_inp) > 500:
        print("Invalid input. Please enter a number between 0 and 500.")
        failed_entries += 1
    else:
        inventory_entry.append(int(entry_inp))
        delivery_amount = process_delivery(delivery_amount, int(entry_inp))
        print(f"Entry {entry_inp} added to inventory.")

    return failed_entries, delivery_amount

def process_delivery(delivery_amount, entry_inp):
    if entry_inp > 0:
        delivery_amount += entry_inp
        print(f"Delivery amount updated to: {delivery_amount}")
        return delivery_amount
    else:
        print("No delivery amount added for zero or negative entries.") 
        return delivery_amount

def calculate_tax(delivery_amount):
    tax_rate = 0.1  # 10% tax rate
    tax_amount = delivery_amount * tax_rate
    return tax_amount

def generate_report(failed_entries, inventory_entry):
    print("\nExiting the program.")
    print(f"Total Units Processed: {len(inventory_entry)}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")


while entry_inp != "exit":
    entry_inp = input("Enter a number between 0 and 500 (or type 'exit'): ")
    failed_entries, delivery_amount = get_valid_input(
        failed_entries, delivery_amount, inventory_entry, entry_inp
    )

generate_report(failed_entries, inventory_entry)
