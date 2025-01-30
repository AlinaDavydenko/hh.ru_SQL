import psycopg2

# подключение к базе данных
with psycopg2.connect(
    host='localhost',
    database='hh_ru_db',
    user='postgres',
    password='81726354'
) as conn:
    with connection.cursor() as cur:
        # составление запросов, execute query
        cur.execute('CREATE TABLE vacancy(post_id int PRIMARY KEY, )')
        cur.execute('SELECT * FROM vacancy')
        conn.commit()
        rows = cur.fetchall()
        cur.execute('DROP TABLE vacancy')

for row in rows:
    print(row)

# закрываем курсор
cur.close()

connection.close()

# connection.commit()
