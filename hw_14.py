from flask import Flask, jsonify

from utils import get_base, get_one_request

app = Flask(__name__)


# Вьюшка, которая реализует поиск по названию (шаг 1)
@app.get('/movie/<title>')
def get_by_title(title):
    query = f"""
       SELECT * FROM netflix
       WHERE title LIKE '%{title}%'
       ORDER BY date_added 
       DESC
    """

    get_part_of_base = get_one_request(query)

    movie = {"title": get_part_of_base["title"],
             "country": get_part_of_base["country"],
             "release_year": get_part_of_base["release_year"],
             "genre": get_part_of_base["listed_in"],
             "description": get_part_of_base["description"],
             }

    return jsonify(movie)


# Вьюшка, которая реализует поиск по диапазону лет выпуска (шаг 2)
@app.get('/movie/<year_before>/to/<year_after>')
def get_by_years(year_before, year_after):
    query = f"""
       SELECT title, release_year
       FROM netflix
       WHERE release_year BETWEEN '{year_before}' AND '{year_after}'
       LIMIT 100
    """
    get_part_of_base = get_base(query)
    data_base = []

    for row in get_part_of_base:
        data_base.append(
            {"title": row["title"],
             "release_year": row["release_year"],
             }
        )

    return jsonify(data_base)

# Вьюшка, которая реализует поиск по рейтингу (шаг 3)
@app.get('/movie/rating/<rating>')
def get_by_category(rating):
    query = f"""
       SELECT title, rating, description
       FROM netflix
       """

    if rating == "children":
        query += "WHERE rating LIKE '%G%'"
    elif rating == "family":
        query += "WHERE rating LIKE '%G%' OR rating LIKE '%PG%' OR rating LIKE '%PG-13%'"
    elif rating == "adult":
        query += "WHERE rating LIKE '%R%' OR rating LIKE '%NC-17%'"
    else:
        return jsonify(status=404)

    get_part_of_base = get_base(query)
    data = []

    for row in get_part_of_base:
        data.append(
            {"title": row["title"],
             "rating": row["rating"],
             "description": row["description"],
             }
        )

    return jsonify(data)


# Вьюшка, которая получает название жанра в качестве аргумента и возвращает 10 самых свежих фильмов в формате json (шаг 4)
@app.get('/genre/<listed_in>')
def get_by_genre(listed_in):
    query = f"""
           SELECT title, description 
           FROM netflix
           WHERE listed_in LIKE '%{listed_in}%'
           ORDER BY date_added  
           DESC
           LIMIT 10
        """

    get_part_of_base = get_base(query)
    data = []

    for row in get_part_of_base:
        data.append(
            {"title": row["title"],
             "description": row["description"],
             }
        )

    return jsonify(data)


if __name__ == "__main__":
    app.run(port=7001, debug=True)
