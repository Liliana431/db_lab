from datetime import date

from config import sql, CURSOR as cursor


def create_product(name, measurement, price, excise_duty, NDS, OKDP):
    d = date.today()
    values = [
        (name, measurement, price, excise_duty, NDS, OKDP, d)
    ]
    insert = sql.SQL('INSERT INTO product (name, measurement, price, excise_duty, "NDC", "OKDP", date) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)


def get_product_list():
    cursor.execute('SELECT DISTINCT ON ("name") id, name FROM product ORDER BY "name", "date" DESC')
    orgs = cursor.fetchall()
    return orgs


def get_product(id, count):
    cursor.execute('SELECT * FROM product WHERE id = %s', str(id))
    prod = {}
    record = cursor.fetchone()
    prod['name'] = record[1]
    prod['measurement'] = record[2]
    prod['price'] = float(record[3].replace(',', '.')[:-2])
    prod['excise_duty'] = float(record[4].replace(',', '.')[:-2])
    prod['OKDP'] = record[6]
    prod['NDC'] = 10 if record[5] == 1 else 20 if record[5] == 2 else 0
    prod['count'] = count
    prod['sum_price'] = prod['price'] * count
    prod['sum_excise_duty'] = prod['excise_duty'] * count
    prod['sum_NDS'] = prod['sum_price'] / (100 - prod['NDC']) * prod['NDC']
    prod['all_sum'] = prod['sum_price'] + prod['sum_NDS']
    return prod
