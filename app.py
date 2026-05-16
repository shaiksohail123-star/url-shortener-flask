from flask import Flask, render_template, request, redirect
import sqlite3
import random
import string

app = Flask(__name__)

# Create database table
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT NOT NULL
)
''')

conn.commit()
conn.close()


@app.route('/', methods=['GET', 'POST'])
def home():

    short_url = None

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        long_url = request.form['long_url']

        short_code = ''.join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

        cursor.execute(
            'INSERT INTO urls (long_url, short_code) VALUES (?, ?)',
            (long_url, short_code)
        )

        conn.commit()

        short_url = f"http://127.0.0.1:5000/{short_code}"

    cursor.execute('SELECT * FROM urls')

    all_urls = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        short_url=short_url,
        all_urls=all_urls
    )


@app.route('/<short_code>')
def redirect_to_url(short_code):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        'SELECT long_url FROM urls WHERE short_code=?',
        (short_code,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return redirect(result[0])

    return "URL not found"


if __name__ == '__main__':
    app.run(debug=True)