from prettytable import PrettyTable


class BeautyView:
    def create_table(self, data):
        raise NotImplementedError

    def create_row(self, data, exchange):
        raise NotImplementedError


class ExchangeView(BeautyView):
    def create_row(self, data, exchange):
        x = PrettyTable()
        x.field_names = ["Дата", f"Продаж {exchange}", f"Купівля {exchange}"]
        for i in data:
            x.add_row(i)
        return x

    def create_table(self, data):
        pass