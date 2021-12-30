import datetime
from calendar import monthrange
from tkinter import *

from src.invoice import get_invoice_list_from_date_period
from view.create_invoice import CreateInvoice


class MainView:
    def __init__(self):
        self.root = Tk()
        self.root.title('Книга продаж')
        self.root.geometry('1200x600')

        self.menu = Menu(self.root)
        self.create_main_menu()

        # для списка счет-фактур
        today = datetime.date.today()
        self.date_from = datetime.date(today.year, today.month, 1)
        self.date_to = datetime.date(today.year, today.month, monthrange(today.year, today.month)[1])

        self.content = Frame(self.root)  # главное окно
        self.sales_book = Frame(self.content)  # только для списка счет-фактур, приизменении даты меняется только он

        self.show_sales_book()

    def create_main_menu(self):
        # меню
        sales_book = Menu(self.menu, tearoff=0)
        sales_book.add_command(label='Показать за период', command=self.show_sales_book)
        self.menu.add_cascade(label='Книга продаж', menu=sales_book)

        invoice = Menu(self.menu, tearoff=0)
        invoice.add_command(label='Добавить', command=self.add_invoice)
        self.menu.add_cascade(label='Счет-фактура', menu=invoice)

        search = Menu(self.menu, tearoff=0)
        search.add_command(label='по номеру', command=self.by_num)
        self.menu.add_cascade(label='Поиск счет-фактур', menu=search)

        self.root.config(menu=self.menu)

    def show_sales_book(self):
        self.content.destroy()
        self.content = Frame(self.root)

        # чтение даты
        ldf = Label(self.content, text="Продажа за период с ")
        self.edf = Entry(self.content)
        self.edf.insert(0, str(self.date_from))
        ldt = Label(self.content, text="по")
        self.edt = Entry(self.content)
        self.edt.insert(0, str(self.date_to))

        # кнопка обновления
        upd = Button(self.content, text='Составить для новой даты', command=self.update_sales_book)

        self.create_invoice_list()

        ldf.grid(row=3, column=0)
        self.edf.grid(row=3, column=1)
        ldt.grid(row=3, column=2)
        self.edt.grid(row=3, column=3)
        upd.grid(row=5)
        self.content.pack()

    def update_sales_book(self):
        ddf = self.edf.get()
        if ddf:
            self.date_from = ddf
        ddt = self.edt.get()
        if ddt:
            self.date_to = ddt
        self.create_invoice_list()

    def create_invoice_list(self):
        self.sales_book.destroy()
        self.sales_book = Frame(self.content)

        # шапка
        Label(master=self.sales_book, wraplength=100, text="Дата и номер счет-фактуры поставщика").grid(row=0, column=0, rowspan=4)
        Label(master=self.sales_book, wraplength=100, text="Наименование покупателя").grid(row=0, column=1, rowspan=4)
        Label(master=self.sales_book, wraplength=100, text="Идентификационный номер покупателя").grid(row=0, column=2, rowspan=4)
        Label(master=self.sales_book, wraplength=100, text="Всего продаж, включая НДС").grid(row=0, column=3, rowspan=4)
        Label(master=self.sales_book, wraplength=600, text="В том числе").grid(row=0, column=4, columnspan=6)

        Label(master=self.sales_book, wraplength=400, text="Продажи, облагаемые налогом по ставке").grid(row=1, column=4, columnspan=4)
        Label(master=self.sales_book, wraplength=200, text="Продажи, не облагаемые налогом").grid(row=1, column=8, columnspan=2)

        Label(master=self.sales_book, wraplength=200, text="20%").grid(row=2, column=4, columnspan=2)
        Label(master=self.sales_book, wraplength=200, text="10%").grid(row=2, column=6, columnspan=2)
        Label(master=self.sales_book, wraplength=100, text="Всего").grid(row=2, column=8)
        Label(master=self.sales_book, wraplength=100, text="Из них экспорт").grid(row=2, column=9)

        Label(master=self.sales_book, wraplength=100, text="Стоимость продаж без НДС").grid(row=3, column=4)
        Label(master=self.sales_book, wraplength=100, text="Сумма НДС").grid(row=3, column=5)
        Label(master=self.sales_book, wraplength=100, text="Стоимость продаж без НДС").grid(row=3, column=6)
        Label(master=self.sales_book, wraplength=100, text="Сумма НДС").grid(row=3, column=7)

        # список счет-фактур
        r = 4
        for inv in get_invoice_list_from_date_period(self.date_from, self.date_to):
            Label(master=self.sales_book, wraplength=100, text=f"{inv['invoice_date']} №{inv['invoice_num']}").grid(row=r, column=0)
            Label(master=self.sales_book, wraplength=100, text=inv['buyer_name']).grid(row=r, column=1)
            Label(master=self.sales_book, wraplength=100, text=inv['buyer_num']).grid(row=r, column=2)
            Label(master=self.sales_book, wraplength=100, text=inv['sum']).grid(row=r, column=3)
            Label(master=self.sales_book, wraplength=100, text=inv['20withoutNDS']).grid(row=r, column=4)
            Label(master=self.sales_book, wraplength=100, text=inv['20NDS']).grid(row=r, column=5)
            Label(master=self.sales_book, wraplength=100, text=inv['10withoutNDS']).grid(row=r, column=6)
            Label(master=self.sales_book, wraplength=100, text=inv['10NDS']).grid(row=r, column=7)
            Label(master=self.sales_book, wraplength=100, text=inv['without_tax']).grid(row=r, column=8)
            Label(master=self.sales_book, wraplength=100, text=inv['export']).grid(row=r, column=9)
            r += 1

        self.sales_book.grid(row=4, columnspan=4)

    def add_invoice(self):
        inv = CreateInvoice(self.root, self.content, self.show_sales_book)
        self.content = inv.content

    def by_num(self):
        # поиск счет-фактуры по номеру с возможностью редактировать и печатать
        pass

    def mainloop(self):
        self.root.mainloop()
