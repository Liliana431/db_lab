from tkinter import *
from tkinter import ttk
import re

from src.invoice import create_invoice, get_simple_invoice, update_invoice
from src.organization import get_organization_list
from src.product import get_product_list, get_product
from view.create_organization import CreateOrganization
from view.create_product import CreateProduct


class CreateInvoice:
    def __init__(self, root, content, create_main_menu):
        self.create_main_menu = create_main_menu
        self.root = root
        self.content = content  # главное окно
        self.product = Frame(self.content)

        self.orgs = None
        self.all_prods = None
        self.product_list = []  # список продуктов вида (ид_прод, количество)

    def add_invoice(self):
        self.content.destroy()
        self.content = Frame(self.root)
        self.orgs = get_organization_list()
        orgs_name = []
        for org in self.orgs:
            orgs_name.append(org['name'])

        Label(master=self.content, wraplength=1000, text="Создать счет-фактуру").grid(row=0, column=0, columnspan=5)

        Button(self.content, text='Добавить организацию', command=self.add_organization).grid(row=1, column=0, columnspan=4)
        Button(self.content, text='Сохранить счет-фактуру', command=self.submit_invoice).grid(row=1, column=4, columnspan=4)

        Label(master=self.content, text="Поставщик").grid(row=2, column=0)
        self.provider = ttk.Combobox(master=self.content, values=orgs_name, width=60)
        self.provider.grid(row=2, column=1, columnspan=2)

        Label(master=self.content, text="Покупатель").grid(row=3, column=0)
        self.buyer = ttk.Combobox(master=self.content, values=orgs_name, width=60)
        self.buyer.grid(row=3, column=1, columnspan=2)

        Label(master=self.content, text="Грузоотправитель").grid(row=4, column=0)
        self.carrier = ttk.Combobox(master=self.content, values=orgs_name, width=60)
        self.carrier.grid(row=4, column=1, columnspan=2)

        Label(master=self.content, text="Грузополучатель").grid(row=5, column=0)
        self.consignee = ttk.Combobox(master=self.content, values=orgs_name, width=60)
        self.consignee.grid(row=5, column=1, columnspan=2)

        Label(master=self.content, wraplength=400, text="Номер платежно-рассчетного документа").grid(row=6, column=0)
        self.doc_num = Entry(master=self.content, width=60)
        self.doc_num.grid(row=6, column=1, columnspan=2)

        Label(master=self.content, wraplength=400, text="Дата платежно-рассчетного документа").grid(row=7, column=0)
        self.doc_date = Entry(master=self.content, width=60)
        self.doc_date.grid(row=7, column=1, columnspan=2)

        Label(master=self.content, wraplength=400, text="Дополнения").grid(row=8, column=0)
        self.extensions = Entry(master=self.content, width=60)
        self.extensions.grid(row=8, column=1, columnspan=2)

        self.add_product()

        self.content.pack()

    def update_invoice(self, invoice=None):
        self.content.destroy()
        self.content = Frame(self.root)

        self.orgs = get_organization_list()
        orgs_name = []
        for org in self.orgs:
            orgs_name.append(org['name'])

        Label(master=self.content, wraplength=1000, text="Обновить счет-фактуру").grid(row=0, column=0, columnspan=5)

        Label(master=self.content, text='Номер счет-фактуры').grid(row=1, column=0, columnspan=3)
        self.inv_id = Entry(master=self.content, width=10)
        self.inv_id.grid(row=1, column=3)
        if invoice:
            self.inv_id.insert(0, str(invoice['id']))

        Button(self.content, text='Найти', command=self.find_inv).grid(row=1, column=5)

        if invoice:
            Button(self.content, text='Добавить организацию', command=self.add_organization).grid(row=2, column=0, columnspan=4)
            Button(self.content, text='Обновить счет-фактуру', command=self.upd_invoice).grid(row=2, column=4, columnspan=4)

            Label(master=self.content, text="Поставщик").grid(row=3, column=0)
            self.provider = ttk.Combobox(master=self.content, values=orgs_name, width=60)
            self.provider.insert(0, invoice['provider'])
            self.provider.grid(row=3, column=1, columnspan=2)

            Label(master=self.content, text="Покупатель").grid(row=4, column=0)
            self.buyer = ttk.Combobox(master=self.content, values=orgs_name, width=60)
            self.buyer.insert(0, invoice['buyer'])
            self.buyer.grid(row=4, column=1, columnspan=2)

            Label(master=self.content, text="Грузоотправитель").grid(row=5, column=0)
            self.carrier = ttk.Combobox(master=self.content, values=orgs_name, width=60)
            self.carrier.insert(0, invoice['carrier'])
            self.carrier.grid(row=5, column=1, columnspan=2)

            Label(master=self.content, text="Грузополучатель").grid(row=6, column=0)
            self.consignee = ttk.Combobox(master=self.content, values=orgs_name, width=60)
            self.consignee.insert(0, invoice['consignee'])
            self.consignee.grid(row=6, column=1, columnspan=2)

            Label(master=self.content, wraplength=400, text="Номер платежно-рассчетного документа").grid(row=7, column=0)
            self.doc_num = Entry(master=self.content, width=60)
            self.doc_num.insert(0, invoice['doc_num'])
            self.doc_num.grid(row=7, column=1, columnspan=2)

            Label(master=self.content, wraplength=400, text="Дата платежно-рассчетного документа").grid(row=8, column=0)
            self.doc_date = Entry(master=self.content, width=60)
            self.doc_date.insert(0, invoice['doc_date'])
            self.doc_date.grid(row=8, column=1, columnspan=2)

            Label(master=self.content, wraplength=400, text="Дополнения").grid(row=9, column=0)
            self.extensions = Entry(master=self.content, width=60)
            self.extensions.insert(0, invoice['extensions'])
            self.extensions.grid(row=9, column=1, columnspan=2)

            self.add_product()

        self.content.pack()

    def find_inv(self):
        inv_id = self.inv_id.get()
        if not re.fullmatch(r'\d+', inv_id):
            self.update_invoice()
        else:
            self.invoice_id = inv_id
            inv, prods = get_simple_invoice(inv_id)
            self.product_list = []
            for p in prods:
                self.product_list.append((p['id'], p['count']))
            self.update_invoice(inv)

    def add_product(self):
        self.product.destroy()
        self.product = Frame(self.content)
        self.all_prods = get_product_list()
        products_name = []
        for prod in self.all_prods:
            products_name.append(prod['name'])

        Label(master=self.product, text="Добавить товар").grid(row=0, column=0)
        self.prod = ttk.Combobox(master=self.product, values=products_name, width=10)
        self.prod.grid(row=0, column=1)

        Label(master=self.product, text="количество").grid(row=0, column=2)
        self.count = Entry(master=self.product, width=10)
        self.count.grid(row=0, column=3)

        Button(self.product, text='ОК', command=self.add_prod_to_list).grid(row=0, column=4)
        Button(self.product, text='Создать новый товар', command=self.submit_product).grid(row=0, column=5)

        Label(master=self.product, text="Наименование товара").grid(row=1, column=0)
        Label(master=self.product, text="Код по ОКДП").grid(row=1, column=1)
        Label(master=self.product, text="Ед. изм.").grid(row=1, column=2)
        Label(master=self.product, text="Кол-во").grid(row=1, column=3)
        Label(master=self.product, text="Цена").grid(row=1, column=4)
        Label(master=self.product, text="В т.ч. акциз").grid(row=1, column=5)
        Label(master=self.product, text="Сумма").grid(row=1, column=6)
        Label(master=self.product, text="В т.ч. акциз").grid(row=1, column=7)
        Label(master=self.product, text="Ставка НДС, %").grid(row=1, column=8)
        Label(master=self.product, text="Сумма НДС").grid(row=1, column=9)
        Label(master=self.product, text="Всего с НДС").grid(row=1, column=10)

        i = 2
        to_be_paid = 0
        for p in self.product_list:
            prod = get_product(p[0], p[1])
            Label(master=self.product, text=prod['name']).grid(row=i, column=0)
            Label(master=self.product, text=prod['OKDP']).grid(row=i, column=1)
            Label(master=self.product, text=prod['measurement']).grid(row=i, column=2)
            Label(master=self.product, text=prod['count']).grid(row=i, column=3)
            Label(master=self.product, text=prod['price']).grid(row=i, column=4)
            Label(master=self.product, text=prod['excise_duty']).grid(row=i, column=5)
            Label(master=self.product, text=prod['sum_price']).grid(row=i, column=6)
            Label(master=self.product, text=prod['sum_excise_duty']).grid(row=i, column=7)
            Label(master=self.product, text=prod['NDS']).grid(row=i, column=8)
            Label(master=self.product, text=prod['sum_NDS']).grid(row=i, column=9)
            Label(master=self.product, text=prod['all_sum']).grid(row=i, column=10)
            to_be_paid += prod['all_sum']
            i += 1
        Label(master=self.product, text='Всего к оплате: ').grid(row=i, column=0)
        Label(master=self.product, text=to_be_paid).grid(row=i, column=1)

        Label(master=self.product, text='Удалить из списка продукт').grid(row=i+1, column=0, columnspan=2)
        self.del_prod = ttk.Combobox(master=self.product, values=products_name, width=10)
        self.del_prod.grid(row=i+1, column=2)
        Button(self.product, text='ОК', command=self.del_prod_to_list).grid(row=i+1, column=4)

        self.product.grid(row=10, column=0, columnspan=8)

    def add_prod_to_list(self):
        for prod in self.all_prods:
            if re.fullmatch(r'\d*(.\d*)?', self.count.get()) and self.prod.get() == prod['name']:
                self.product_list.append((prod['id'], float(self.count.get())))
                break
        self.add_product()

    def del_prod_to_list(self):
        for prod in self.all_prods:
            if self.del_prod.get() == prod['name']:
                for i in self.product_list:
                    if i[0] == prod['id']:
                        self.product_list.remove(i)
                break
        self.add_product()

    def submit_product(self):
        prod = CreateProduct(self.root, self.content, self.add_invoice)
        self.content.destroy()
        self.content = prod.content

    def submit_invoice(self):
        provider, buyer, carrier, consignee, doc_num, doc_date = None, None, None, None, None, None
        extensions = self.extensions.get()
        for org in self.orgs:
            if self.provider.get() == org['name']:
                provider = org['id']
            if self.buyer.get() == org['name']:
                buyer = org['id']
            if self.carrier.get() == org['name']:
                carrier = org['id']
            if self.consignee.get() == org['name']:
                consignee = org['id']

        if re.fullmatch(r'\d*', self.doc_num.get()):
            doc_num = self.doc_num.get()

        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', self.doc_date.get()):
            doc_date = self.doc_date.get()

        if not (provider and buyer and carrier and consignee and doc_num and doc_date):
            self.add_invoice()
        else:
            create_invoice(provider, buyer, carrier, consignee, extensions, doc_num, doc_date, self.product_list)
            self.content.destroy()
            self.create_main_menu()

    def upd_invoice(self):
        provider, buyer, carrier, consignee, doc_num, doc_date = None, None, None, None, None, None
        extensions = self.extensions.get()
        for org in self.orgs:
            if self.provider.get() == org['name']:
                provider = org['id']
            if self.buyer.get() == org['name']:
                buyer = org['id']
            if self.carrier.get() == org['name']:
                carrier = org['id']
            if self.consignee.get() == org['name']:
                consignee = org['id']

        if re.fullmatch(r'\d*', self.doc_num.get()):
            doc_num = self.doc_num.get()

        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', self.doc_date.get()):
            doc_date = self.doc_date.get()

        if not (provider and buyer and carrier and consignee and doc_num and doc_date):
            self.update_invoice()
        else:
            update_invoice(self.invoice_id, provider, buyer, carrier, consignee, extensions, doc_num, doc_date, self.product_list)
            self.content.destroy()
            self.create_main_menu()

    def add_organization(self):
        org = CreateOrganization(self.root, self.content, self.add_invoice)
        self.content = org.content
