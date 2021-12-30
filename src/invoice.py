from datetime import date

from config import sql, CURSOR as cursor


def create_invoice(provider, buyer, carrier, consignee, extensions, doc_num, doc_date, product_list):
    invoice_id = create_invoice_header(provider, buyer, carrier, consignee, extensions, doc_num, doc_date)
    values = []
    for i in product_list:
        values.append((invoice_id, i[0], i[1]))
    insert = sql.SQL('INSERT INTO invoice(id_header, id_product, count) VALUES {}').format(
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


def get_invoice_list_from_date_period(date_from, date_to):
    cursor.execute('''
    SELECT 
        ih."id" "invoice_num",
        ih."date" "invoice_date",
        comp."id" "buyer_num",
        comp."name" "buyer_name",
        sum(prod."price" * inv."count") "sum",
        sum(CASE
            WHEN prod."NDS" = 2 THEN prod."price" * inv."count" * 0.8
            ELSE 0
        END) "20withoutNDS",
        sum(CASE
            WHEN prod."NDS" = 2 THEN prod."price" * inv."count" * 0.2
            ELSE 0
        END) "20NDS",
        sum(CASE
            WHEN prod."NDS" = 1 THEN prod."price" * inv."count" * 0.9
            ELSE 0
        END) "10withoutNDS",
        sum(CASE
            WHEN prod."NDS" = 1 THEN prod."price" * inv."count" * 0.1
            ELSE 0
        END) "10NDS",
        sum(CASE
            WHEN prod."NDS" > 30 THEN prod."price" * inv."count"
            ELSE 0
        END) "without_tax",
        sum(CASE
            WHEN prod."NDS" = 31 THEN prod."price" * inv."count"
            ELSE 0
        END) "export"
    FROM 
        "invoice" inv
        JOIN "invoice_header" ih ON inv."id_header" = ih."id"
        JOIN "company" comp ON ih."buyer" = comp."id"
        JOIN "product" prod ON prod."id" = inv."id_product"
    WHERE %s <= ih."date" AND ih."date" <= %s
    GROUP BY ih."id", comp."id"
    ORDER BY ih."date", ih."id"
    ''', (date_from, date_to))
    invoices = cursor.fetchall()
    return invoices
