data = {
    "inventory": {
        "P001": {"name": "Laptop"},
        "P002": {"name": "Mouse"},
        "P003": {"name": "Wires"},
        "P004": {"name": "Spoons"}
    }
}

# Safely finds the maximum numeric value among the keys
highest_num = max(int(pid[1:]) for pid in data["inventory"]) + 1
highest_id = f"P{highest_num:03d}"

print(highest_id)  # Output: P005