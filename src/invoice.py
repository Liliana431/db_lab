from datetime import date

from config import sql, CURSOR as cursor


def create_invoice(provider, buyer, carrier, consignee, extensions, doc_num, doc_date, product_list):
    create_invoice_header()
    print("все ок")

    # d = date.today()
    # values = [
    #     (name, measurement, price, excise_duty, NDS, OKDP, d)
    # ]
    # insert = sql.SQL('INSERT INTO product (name, measurement, price, excise_duty, "NDC", "OKDP", date) VALUES {}').format(
    #     sql.SQL(',').join(map(sql.Literal, values))
    # )
    # cursor.execute(insert)


def create_invoice_header():
    pass


# def get_product_list():
#     cursor.execute('SELECT DISTINCT ON ("name") id, name FROM product ORDER BY "name", "date" DESC')
#     orgs = cursor.fetchall()
#     return orgs
#
#
# def get_product(id, count):
#     cursor.execute('SELECT * FROM product WHERE id = %s', str(id))
#     record = cursor.fetchone()
#     record['NDC'] = 10 if record['NDC'] == 1 else 20 if record['NDC'] == 2 else 0
#     record['count'] = count
#     record['sum_price'] = record['price'] * Decimal(count)
#     record['sum_excise_duty'] = record['excise_duty'] * Decimal(count)
#     record['sum_NDS'] = record['sum_price'] / (100 - record['NDC']) * record['NDC']
#     record['all_sum'] = record['sum_price'] + record['sum_NDS']
#     return record
