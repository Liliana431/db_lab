from datetime import date
from decimal import Decimal

from config import sql, CURSOR as cursor


def create_product(name, measurement, price, excise_duty, NDS, OKDP):
    d = date.today()
    values = [
        (name, measurement, price, excise_duty, NDS, OKDP, d)
    ]
    insert = sql.SQL('INSERT INTO product (name, measurement, price, excise_duty, "NDS", "OKDP", date) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)


def get_product_list():
    cursor.execute('SELECT DISTINCT ON ("name") id, name FROM product ORDER BY "name", "date" DESC')
    orgs = cursor.fetchall()
    return orgs


def get_product(id, count):
    cursor.execute('SELECT * FROM product WHERE id = %s', str(id))
    record = cursor.fetchone()
    record['NDS'] = 10 if record['NDS'] == 1 else 20 if record['NDS'] == 2 else 0
    record['count'] = count
    record['all_sum'] = record['price'] * Decimal(count)
    record['sum_NDS'] = record['all_sum'] * Decimal(record['NDS'] / 100)
    record['sum_price'] = record['all_sum'] - record['sum_NDS']
    record['sum_excise_duty'] = record['excise_duty'] * Decimal(count)
    return record
