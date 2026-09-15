def dispense_drink(drink):
    match drink:
        case "Coke":
            print("Dispensing Coke.")
        case "Pepsi":
            print("Dispensing Pepsi.")
        case "Water":
            print("Dispensing Water.")
        case "Juice":
            print("Dispensing Juice.")
        case _:
            print("Invalid selection. Please choose a valid drink.")

    return drink