from config import sql, CURSOR as cursor


def create_organization(name, city, address, phone_number, pay_account, currency, INN, OKONH, OKPO):
    values = [
        (name, city, address, phone_number, pay_account, currency, INN, OKONH, OKPO)
    ]
    insert = sql.SQL('INSERT INTO company (name, phone_number, city, address, pay_account, currency, "INN", "OKONH", "OKPO") VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)


def get_organization_list():
    cursor.execute('SELECT id, name FROM company')
    orgs = cursor.fetchall()
    return orgs
