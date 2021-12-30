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
    return cursor.fetchall()


def get_simple_invoice(inv_id):
    cursor.execute('''
        SELECT 
            ih."id" "id",
            provider."name" "provider",
            buyer."name" "buyer",
            carrier."name" "carrier",
            consignee."name" "consignee",
            ih."id_pay_settl_doc" "doc_num",
            ih."date_pay_settl_doc" "doc_date",
            ih."extensions" "extensions"                    
        FROM 
            "invoice_header" ih
            JOIN "company" provider ON provider."id" = ih."provider"
            JOIN "company" buyer ON buyer."id" = ih."buyer"
            JOIN "company" carrier ON carrier."id" = ih."carrier"
            JOIN "company" consignee ON consignee."id" = ih."consignee"
        WHERE %s = ih.id
        ''', (inv_id, ))
    invoice = cursor.fetchone()

    cursor.execute('''
        SELECT 
            inv."id_product" "id",
            inv."count" "count"         
        FROM 
            "invoice" inv
        WHERE %s = inv.id_header
    ''', (inv_id,))
    products = cursor.fetchall()
    return invoice, products


def update_invoice(inv_id, provider, buyer, carrier, consignee, extensions, doc_num, doc_date, product_list):
    update_invoice_header(inv_id, provider, buyer, carrier, consignee, extensions, doc_num, doc_date)
    update_product_list(inv_id, product_list)


def update_invoice_header(inv_id, provider, buyer, carrier, consignee, extensions, doc_num, doc_date):
    cursor.execute('''
        UPDATE invoice_header
        SET id_pay_settl_doc=%s, date_pay_settl_doc=%s, provider=%s, buyer=%s, carrier=%s, consignee=%s, extensions=%s
        WHERE id = %s
    ''', (doc_num, doc_date, provider, buyer, carrier, consignee, extensions, inv_id))


def update_product_list(inv_id, new_product_list):
    cursor.execute('SELECT id_product, count FROM invoice WHERE id_header = %s', (inv_id, ))
    old_prods = [(p['id_product'], p['count']) for p in cursor.fetchall()]

    new_prods = [(inv_id, p[0], p[1]) for p in new_product_list if p not in old_prods]
    deleted_prods = [p[0] for p in old_prods if p not in new_product_list]

    if deleted_prods:
        cursor.execute('DELETE FROM invoice WHERE id_header = %s AND id_product=ANY(%s::integer[])', (inv_id, deleted_prods))

    if new_prods:
        insert = sql.SQL('INSERT INTO invoice(id_header, id_product, count) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, new_prods))
        )
        cursor.execute(insert)
