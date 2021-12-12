from datetime import date

from config import sql, CURSOR as cursor


def create_product(name, measurement, price, excise_duty, NDS, OKDP):
    d = date.today()
    values = [
        (name, measurement, price, excise_duty, NDS, OKDP, d)
    ]
    print(values)
    insert = sql.SQL('INSERT INTO product (name, measurement, price, excise_duty, "NDC", "OKDP", date) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)


def get_product_list():
    cursor.execute('SELECT id, name FROM product')
    orgs = cursor.fetchall()
    return orgs
