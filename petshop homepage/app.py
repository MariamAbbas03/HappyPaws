from flask import Flask, render_template, request, redirect, url_for
import os
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

conn = psycopg2.connect(
    dbname="trial433",
    user="postgres",
    password="mayan",
    host='127.0.0.1',
    port=5433
)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS items
                  (id SERIAL PRIMARY KEY,
                   name TEXT,
                   type TEXT,
                   image_url TEXT,
                   price REAL)''')
conn.commit()

sample_data = [
    ('Cat Food', 'Food', 'cat_food.jpg', 10.99),
    ('Dog Collar', 'Accessory', 'dog_collar.jpg', 15.99),
    ('Fish Tank', 'Accessory', 'fish_tank.jpg', 59.99)
]

cursor.execute('SELECT * FROM items')
if not cursor.fetchall():
    cursor.executemany('INSERT INTO items (name, type, image_url, price) VALUES (%s, %s, %s, %s)', sample_data)
    conn.commit()

@app.route('/')
def home():
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        price = request.form['price']
        image = request.files['image']

        cursor.execute('SELECT * FROM items WHERE name = %s', (name,))
        existing_item = cursor.fetchone()
        if existing_item:
            return "Item already exists!"
        else:
            image_filename = image.filename
            image.save(os.path.join('static/images', image_filename))

            cursor.execute('INSERT INTO items (name, type, image_url, price) VALUES (%s, %s, %s, %s)',
                           (name, type, image_filename, price))
            conn.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
