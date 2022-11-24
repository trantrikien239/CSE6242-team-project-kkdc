from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    conn = sqlite3.connect("data/6242project.db")
    conn.text_factory = str

    get_data = "SELECT * FROM group_rating_sample"
    cursor = conn.execute(get_data)
    data = cursor.fetchall()
    print(data)

    conn.close()
    return data

if __name__ == '__main__':
    app.run(debug=True)