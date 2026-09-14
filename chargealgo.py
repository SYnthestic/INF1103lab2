def chargesys(hours):
    if hours <= 2:
        price = 0.00
        return price
    elif hours <= 24:
        price = 2*(hours - 2)
        return price