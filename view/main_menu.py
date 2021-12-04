from tkinter import *


def main_menu(content):
    # главное окно
    root = Tk()
    root.title('Книга продаж')
    root.geometry('400x250')

    # меню
    menu = Menu(root)

    sales_book = Menu(menu)
    sales_book.add_command(label='За другой период', command='')
    sales_book.add_command(label='Дополнить вручную')
    menu.add_cascade(label='Книга продаж', menu=sales_book)

    invoice = Menu(menu)
    invoice.add_command(label='Добавить')
    menu.add_cascade(label='Счет-фактура', menu=invoice)

    search = Menu(menu)
    # sales_book.add_command(label='За другой период')
    # sales_book.add_command(label='Дополнить вручную')
    menu.add_cascade(label='Поиск', menu=search)

    root.config(menu=menu)

    # наполнение
    # вызвать метод из параметров

    root.mainloop()
