import psycopg2
conn = psycopg2.connect(dbname='sales_book', user='postgres',
                        password='1234qwer', host='localhost')
CURSOR = conn.cursor()
