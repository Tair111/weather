from pprint import pprint

import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import json

app = Flask(__name__)

API = '5dd749b2f141ddbfd300a8b434132de1'


@app.before_request
def before_first_request():
    init_db()


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    # получем список городов, где ранее смотрели погоду
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM city')
    cities = [row[1] for row in cursor.fetchall()]
    conn.close()

    search = request.args.get('term')  # Получаем текст поиска из параметра 'term'
    matches = [city for city in cities if search.lower() in city.lower()]

    return jsonify(matches)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    tempriche = ""
    name_city = None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM city')
    cities = [row[1] for row in cursor.fetchall()]
    conn.close()

    try:
        if request.method == 'POST':
            name_city = request.form['city'].lower()
            res = requests.get(f'https://api.openweathermap.org/data/2.5/find?q={name_city}&type=like&APPID={API}&units=metric')
            data = json.loads(res.text)
            tem = data['list'][1]['main']['temp']
            tempriche = f'температура в {name_city} равна {tem}'
    except Exception as ex:
        print(ex)
        tempriche = f'Не удалось узнать погоду, повторите запрос'

    try:
        if name_city:
            conn = get_db_connection()
            conn.execute('INSERT INTO city (name_city) VALUES (?)', (name_city,))
            conn.commit()
            conn.close()
    except Exception as exc:
        print(exc)

    return render_template('weather.html', tempriche=tempriche, cities=cities)

def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS city (id INTEGER PRIMARY KEY AUTOINCREMENT, name_city TEXT UNIQUE NOT NULL)')
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def close_db_connection(conn):
    conn.close()


if __name__ == '__main__':
    app.run()