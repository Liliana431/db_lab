from psycopg2 import sql, connect
import psycopg2.extras

connect = connect(dbname='sales_book', user='postgres',
                  password='1234qwer', host='localhost')
CURSOR = connect.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
connect.autocommit = True

