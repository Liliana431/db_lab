from psycopg2 import sql, connect

connect = connect(dbname='sales_book', user='postgres',
                  password='1234qwer', host='localhost')
CURSOR = connect.cursor()
connect.autocommit = True
