# product = [["Laptop", 599, 50], ["Mouse", 39, 120], ["Keyboard", 95, 80]]
product = [
    {"product_name": "Laptop", "product_price": 599, "product_stocks": 50},
    {"product_name": "Mouse", "product_price": 39, "product_stocks": 120},
    {"product_name": "Keyboard", "product_price": 95, "product_stocks": 80}
]

print("Product Names:")
for item in product:
    print(item['product_name'])

product_inp = input("Enter product name: ")
price_inp = input("Enter product price: ")
stocks_inp = input("Enter product stocks: ")

data_inp = {
    "product_name": product_inp,
    "product_price": price_inp,
    "product_stocks": stocks_inp
}

product.append(data_inp)

# Print the updated list to verify
print("\nAfter Adding New Product:")
for item in product:
    print(item['product_name'])