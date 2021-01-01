
class Item:
    def __init__(self, new_name, new_added_months):
        self.name = new_name
        self.reference = "000"
        self.sells_history = []
        self.stock = 0
        self.monthly_sells = 0
        self.to_buy = 0
        self.buy_price = 0
        self.sell_price = 0

        for i in range(0, new_added_months):
            self.sells_history.append(0)


