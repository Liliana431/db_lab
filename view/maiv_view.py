from tkinter import *
from tkinter import ttk

from src.organization import get_organization_list
from src.sales_book import SalesBook
from view.create_invoice import CreateInvoice


class MainView:
    def __init__(self):
        self.invoice_list = SalesBook()
        self.root = Tk()
        self.root.title('Книга продаж')
        self.root.geometry('1000x600')

        self.menu = Menu(self.root)
        self.create_main_menu()

        # для списка счет-фактур
        self.date_from = self.invoice_list.date_from
        self.date_to = self.invoice_list.date_to

        self.content = Frame(self.root)  # главное окно
        self.sales_book = Frame(self.content)  # только для списка счет-фактур, приизменении даты меняется только он

        self.show_sales_book()

    def create_main_menu(self):
        # меню
        sales_book = Menu(self.menu, tearoff=0)
        sales_book.add_command(label='Дополнить вручную')
        sales_book.add_command(label='Показать за период', command=self.show_sales_book)
        self.menu.add_cascade(label='Книга продаж', menu=sales_book)

        invoice = Menu(self.menu, tearoff=0)
        invoice.add_command(label='Добавить', command=self.add_invoice)
        self.menu.add_cascade(label='Счет-фактура', menu=invoice)

        search = Menu(self.menu, tearoff=0)
        search.add_command(label='Счет-фактура по номеру')
        self.menu.add_cascade(label='Поиск', menu=search)

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
        Label(master=self.sales_book, text=(str(self.date_from) + ' ' + str(self.date_to))).grid(row=6)
        self.sales_book.grid(row=4, columnspan=4)

    def add_invoice(self):
        inv = CreateInvoice(self.root, self.content, self.create_main_menu)
        self.content = inv.content

    def mainloop(self):
        self.root.mainloop()
