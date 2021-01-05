from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from Utils import *
from TableWidget import *

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
        self.table_item_average = TableWidgetItem()
        self.table_item_tosell = TableWidgetItem()

        for i in range(0, new_added_months):
            self.sells_history.append(0)

    def calc_average(self, months_average, months_to_buy):
        my_list = self.sells_history.copy()
        my_list.reverse()
        average = 0

        for y in range(0, months_average):
            average += my_list[y]
        average = average / months_average

        self.monthly_sells = average

        if 1 < average:
            average = round(average)
        else:
            average = round(average, 2)

        self.table_item_average.setText(Utils.float_to_str(average))

        self.calc_tobuy(months_to_buy)

    def calc_tobuy(self, months_to_buy):
        tobuy = (months_to_buy * self.monthly_sells) - self.stock
        if 1 < tobuy:
            tobuy = round(tobuy)
        else:
            tobuy = round(tobuy, 2)

        self.to_buy = tobuy
        self.table_item_tosell.setText(str(tobuy))