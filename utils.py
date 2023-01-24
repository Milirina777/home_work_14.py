import sqlite3


def get_base(query):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        my_base = cursor.fetchall()

        return my_base


def get_one_request(query):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute(query)
        my_base = cursor.fetchone()

        return my_base

# Функция шага 6 - получает на выходе список названий картин с их описаниями.
def get_by_catalog(type_, release_year, listed_in):
    conn = sqlite3.connect("netflix.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT title FROM netflix 
               WHERE type = ? AND release_year = ? AND listed_in = ? 
               ORDER BY title ASC
               LIMIT 100""", [type_, release_year, listed_in])
    data = cursor.fetchall()
    result = []

    for index in data:
        result.append({"title": index[0]})

    return result

# Функция шага 5 - которая получает имена двух актеров и возвращает список тех, кто играет с ними в паре больше 2 раз.
def cut_by_cast(actor_1, actor_2):
    conn = sqlite3.connect("netflix.db")
    cursor = conn.cursor()
    cursor.execute(f"""SELECT COUNT (netflix.cast) FROM netflix 
               WHERE netflix.cast LIKE '%{actor_1}%' AND netflix.cast LIKE '%{actor_2}%'""")
    result = cursor.fetchall()
    count = int(result[0][0])

    cursor.execute(f"""SELECT * FROM netflix 
                  WHERE netflix.cast LIKE '%{actor_1}%' AND netflix.cast LIKE '%{actor_2}%'""")
    result = cursor.fetchall()
    data_base = []
    if count >= 2:
        for row in result:
            data_base.append(
                {"cast": row[4],
                 }
            )

    return data_base


print(get_by_catalog("Movie", 2017, "Comedies"))
print(cut_by_cast("Ajay Devgn", "Arshad Warsi"))
