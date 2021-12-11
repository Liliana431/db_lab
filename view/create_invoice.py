from tkinter import *
from tkinter import ttk

from src.organization import get_organization_list
from view.create_organization import CreateOrganization


class CreateInvoice:
    def __init__(self, root, content, create_main_menu):
        self.create_main_menu = create_main_menu
        self.root = root
        self.content = content  # главное окно

        self.orgs = None
        self.product_list = []

        self.add_invoice()

    def add_invoice(self):
        self.content.destroy()
        self.content = Frame(self.root)
        self.orgs = get_organization_list()
        orgs_name = []
        for org in self.orgs:
            orgs_name.append(org[1])

        Label(master=self.content, wraplength=1000, text="Создать счет-фактуру").grid(row=0, column=0, columnspan=5)

        Button(self.content, text='Добавить организацию', command=self.add_organization).grid(row=1, column=0)
        Button(self.content, text='Сохранить счет-фактуру', command=self.submit_invoice).grid(row=1, column=2)

        Label(master=self.content, wraplength=400, text="Поставщик").grid(row=2, column=0, columnspan=2)
        self.provider = ttk.Combobox(master=self.content, values=orgs_name)
        self.provider.grid(row=2, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Покупатель").grid(row=3, column=0, columnspan=2)
        self.buyer = ttk.Combobox(master=self.content, values=orgs_name)
        self.buyer.grid(row=3, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Грузоотправитель").grid(row=4, column=0, columnspan=2)
        self.carrier = ttk.Combobox(master=self.content, values=orgs_name)
        self.carrier.grid(row=4, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Грузополучатель").grid(row=5, column=0, columnspan=2)
        self.consignee = ttk.Combobox(master=self.content, values=orgs_name)
        self.consignee.grid(row=5, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Дополнения").grid(row=6, column=0, columnspan=2)
        self.extensions = Entry(master=self.content, width=60)
        self.extensions.grid(row=6, column=2, columnspan=3)

        self.submit_product()

        self.content.pack()

    def add_product(self):
        # перерисовать список
        Label(master=self.content, wraplength=200, text="Добавить товар").grid(row=7, column=0)
        Label(master=self.content, wraplength=200, text="строка выбора товара").grid(row=7, column=1)
        Label(master=self.content, wraplength=200, text="количество").grid(row=7, column=2)
        self.count = Entry(master=self.content)
        self.count.grid(row=7, column=3)
        Button(self.content, text='ОК', command=self.add_product).grid(row=7, column=4)
        Button(self.content, text='Создать новый товар', command=self.submit_product).grid(row=7, column=5)

        # product list

    def submit_product(self):
        # добавть новый
        pass

    def submit_invoice(self):
        provider, buyer, carrier, consignee = None, None, None, None
        extensions = self.extensions.get()
        for org in self.orgs:
            if self.provider.get() == org[1]:
                provider = org[0]
            if self.buyer.get() == org[1]:
                buyer = org[0]
            if self.carrier.get() == org[1]:
                carrier = org[0]
            if self.consignee.get() == org[1]:
                consignee = org[0]

        # информация о товарах

        if not (provider and buyer and carrier and consignee):
            self.add_invoice()
        else:
            pass

    def add_organization(self):
        org = CreateOrganization(self.root, self.content, self.add_invoice)
        self.content = org.content
