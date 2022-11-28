from flask import Flask, render_template, request
from flask_cors import CORS #comment this on deployment
import sqlite3

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    conn = sqlite3.connect("data/6242project.db")
    conn.text_factory = str

    get_data = "SELECT * FROM group_rating_sample"
    cursor = conn.execute(get_data)
    data = cursor.fetchall()
    #print(data)  

    conn.close()
    return render_template("index.html")

@app.route('/collect', methods=['POST'])
def collect_form_data():
    data = request.form['javascript_data']
    print(data) 
    return data 

if __name__ == '__main__':
    app.run(debug=True)