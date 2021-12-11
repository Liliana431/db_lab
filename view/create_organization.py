from tkinter import *
import re

from src.organization import create_organization


class CreateOrganization:
    def __init__(self, root, content, add_invoice):
        self.add_invoice = add_invoice
        self.root = root
        self.content = content  # главное окно

        self.name_text = ''
        self.city_text = ''
        self.address_text = ''
        self.phone_number_text = ''
        self.pay_account_text = ''
        self.currency_text = ''
        self.INN_text = ''
        self.OKONH_text = ''
        self.OKPO_text = ''

        self.add_organization()

    def add_organization(self):
        self.content.destroy()
        self.content = Frame(self.root)

        Label(master=self.content, wraplength=1000, text="Создать организацию").grid(row=0, column=0, columnspan=5)

        Label(master=self.content, wraplength=400, text="Название").grid(row=1, column=0, columnspan=2)
        self.name = Entry(master=self.content)
        self.name.insert(0, self.name_text)
        self.name.grid(row=1, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Город").grid(row=2, column=0, columnspan=2)
        self.city = Entry(master=self.content)
        self.city.insert(0, self.city_text)
        self.city.grid(row=2, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Адрес").grid(row=3, column=0, columnspan=2)
        self.address = Entry(master=self.content)
        self.address.insert(0, self.address_text)
        self.address.grid(row=3, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Телефон").grid(row=4, column=0, columnspan=2)
        self.phone_number = Entry(master=self.content)
        self.phone_number.insert(0, self.phone_number_text)
        self.phone_number.grid(row=4, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Расчетный счет").grid(row=5, column=0, columnspan=2)
        self.pay_account = Entry(master=self.content)
        self.pay_account.insert(0, self.pay_account_text)
        self.pay_account.grid(row=5, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Валюта").grid(row=6, column=0, columnspan=2)
        self.currency = Entry(master=self.content)
        self.currency.insert(0, self.currency_text)
        self.currency.grid(row=6, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="ИНН").grid(row=7, column=0, columnspan=2)
        self.INN = Entry(master=self.content)
        self.INN.insert(0, self.INN_text)
        self.INN.grid(row=7, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="ОКОНХ").grid(row=8, column=0, columnspan=2)
        self.OKONH = Entry(master=self.content)
        self.OKONH.insert(0, self.OKONH_text)
        self.OKONH.grid(row=8, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="ОКПО").grid(row=9, column=0, columnspan=2)
        self.OKPO = Entry(master=self.content)
        self.OKPO.insert(0, self.OKPO_text)
        self.OKPO.grid(row=9, column=2, columnspan=3)

        Button(self.content, text='Сохранить организацию', command=self.submit_company).grid(row=10)

        self.content.pack()

    def submit_company(self):
        self.name_text = self.name.get().strip()
        self.city_text = self.city.get().strip()
        self.address_text = self.address.get().strip()
        if re.fullmatch(r'(\+7|8)\d{10}', self.phone_number.get()):
            self.phone_number_text = self.phone_number.get()
        else:
            self.phone_number_text = ''
        self.pay_account_text = self.pay_account.get().strip()
        self.currency_text = self.currency.get().strip()
        if re.fullmatch(r'\d{10}', self.INN.get()):
            self.INN_text = int(self.INN.get())
        else:
            self.INN_text = ''
        if re.fullmatch(r'\d{5}', self.OKONH.get()):
            self.OKONH_text = int(self.OKONH.get())
        else:
            self.OKONH_text = ''
        if re.fullmatch(r'\d{8}|\d{10}', self.OKPO.get()):
            self.OKPO_text = int(self.OKPO.get())
        else:
            self.OKPO_text = ''

        if not (self.name_text
                and self.city_text
                and self.address_text
                and self.phone_number_text
                and self.pay_account_text
                and self.currency_text
                and self.INN_text
                and self.OKONH_text
                and self.OKPO_text):
            self.add_organization()
        else:
            create_organization(name=self.name_text,
                                city=self.city_text,
                                address=self.address_text,
                                phone_number=self.phone_number_text,
                                pay_account=self.pay_account_text,
                                currency=self.currency_text,
                                INN=self.INN_text,
                                OKONH=self.OKONH_text,
                                OKPO=self.OKPO_text)
            self.content.destroy()
            self.add_invoice()
