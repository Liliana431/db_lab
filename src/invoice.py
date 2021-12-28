from datetime import date

from config import sql, CURSOR as cursor


def create_invoice(provider, buyer, carrier, consignee, extensions, doc_num, doc_date, product_list):
    invoice_id = create_invoice_header(provider, buyer, carrier, consignee, extensions, doc_num, doc_date)
    values = []
    for i in product_list:
        values.append((invoice_id, i))
    insert = sql.SQL('INSERT INTO invoice(id_header, id_product) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)


def create_invoice_header(provider, buyer, carrier, consignee, extensions, doc_num, doc_date):
    d_today = date.today()
    values = [
        (d_today, doc_num, doc_date, provider, buyer, carrier, consignee, extensions)
    ]
    insert = sql.SQL('INSERT INTO invoice_header'
                     '(date, id_pay_settl_doc, date_pay_settl_doc, provider, buyer, carrier, consignee, extensions)'
                     'VALUES {} RETURNING id').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)
    return cursor.fetchone()['id']

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
