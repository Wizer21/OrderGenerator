
class Item:
    def __init__(self, new_name, new_added_months):
        self.name = new_name
        self.sells_history = []

        for i in range(0, new_added_months):
            self.sells_history.append(0)

    def add_month(self, val):
        self.sells_history.append(val)


