from tkinter import *
import re
from tkinter import ttk

from src.organization import create_organization
from src.product import create_product


class CreateProduct:
    def __init__(self, root, content, add_invoice):
        self.add_invoice = add_invoice
        self.root = root
        self.content = content  # главное окно

        self.name_text = ''
        self.measurement_text = ''
        self.price_text = ''
        self.excise_duty_text = ''
        self.OKDP_text = ''
        self.NDS_text = ''

        self.add_product()

    def add_product(self):
        self.content.destroy()
        self.content = Frame(self.root)

        Label(master=self.content, wraplength=1000, text="Создать продукт").grid(row=0, column=0, columnspan=5)

        Label(master=self.content, wraplength=400, text="Название").grid(row=1, column=0, columnspan=2)
        self.name = Entry(master=self.content)
        self.name.insert(0, self.name_text)
        self.name.grid(row=1, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Единица измерения").grid(row=2, column=0, columnspan=2)
        self.measurement = Entry(master=self.content)
        self.measurement.insert(0, self.measurement_text)
        self.measurement.grid(row=2, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Цена").grid(row=3, column=0, columnspan=2)
        self.price = Entry(master=self.content)
        self.price.insert(0, self.price_text)
        self.price.grid(row=3, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Сумма акциза для единицы товара").grid(row=4, column=0, columnspan=2)
        self.excise_duty = Entry(master=self.content)
        self.excise_duty.insert(0, self.excise_duty_text)
        self.excise_duty.grid(row=4, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="НДС").grid(row=5, column=0, columnspan=2)
        self.NDS = ttk.Combobox(master=self.content, values=['10%', '20%', 'товар, не облагаемый налогом', 'товар на экспорт'])
        self.NDS.grid(row=5, column=2, columnspan=3)

        Label(master=self.content, wraplength=400, text="Код ОКДП").grid(row=6, column=0, columnspan=2)
        self.OKDP = Entry(master=self.content)
        self.OKDP.insert(0, self.OKDP_text)
        self.OKDP.grid(row=6, column=2, columnspan=3)

        Button(self.content, text='Сохранить продукт', command=self.submit_product).grid(row=10)
        self.content.pack()

    def submit_product(self):
        self.name_text = self.name.get().strip()
        self.measurement_text = self.measurement.get().strip()
        if re.fullmatch(r'\d*[.,]\d\d', self.price.get()):
            self.price_text = self.price.get()
        else:
            self.price_text = ''

        if re.fullmatch(r'\d*[.,]\d\d', self.excise_duty.get()):
            self.excise_duty_text = self.excise_duty.get()
        else:
            self.excise_duty_text = ''
        if re.fullmatch(r'\d{2,9}', self.OKDP.get()):
            self.OKPO_text = int(self.OKDP.get())
        else:
            self.OKPO_text = ''

        case_NDS = {
            '10%': 1,
            '20%': 2,
            'товар, не облагаемый налогом': 32,
            'товар на экспорт': 31
        }
        self.NDS_text = case_NDS[self.NDS.get()]

        if not (self.name_text
                and self.measurement_text
                and self.price_text
                and self.excise_duty_text
                and self.OKPO_text
                and self.NDS_text):
            self.add_product()
        else:
            create_product(name=self.name_text,
                           measurement=self.measurement_text,
                           price=self.price_text,
                           excise_duty=self.excise_duty_text,
                           OKDP=self.OKPO_text,
                           NDS=self.NDS_text)
            # print(self.name_text
            #     , self.measurement_text
            #     , self.price_text
            #     , self.excise_duty_text
            #     , self.OKPO_text
            #     , self.NDS_text)
            self.content.destroy()
            self.add_invoice()
