import datetime
from calendar import monthrange


class SalesBook:
    def __init__(self, date_from=None, date_to=None):
        today = datetime.date.today()
        if not date_from:
            self.date_from = datetime.date(today.year, today.month, 1)
        if not date_to:
            self.date_to = datetime.date(today.year, today.month, monthrange(today.year, today.month)[1])
        self.invoice_list = None
        self.read_invoice_list()

    def read_invoice_list(self):
        self.invoice_list = [1, 2]
