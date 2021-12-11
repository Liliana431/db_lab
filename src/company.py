from config import sql, CURSOR as cursor


def create_company(name, city, address, phone_number, pay_account, currency, INN, OKONH, OKPO):
    values = [
        (name, city, address, phone_number, pay_account, currency, INN, OKONH, OKPO)
    ]
    insert = sql.SQL('INSERT INTO company (name, phone_number, city, address, pay_account, currency, "INN", "OKONH", "OKPO") VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )
    cursor.execute(insert)
