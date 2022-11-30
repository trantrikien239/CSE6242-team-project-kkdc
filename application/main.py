from flask import Flask, render_template, request, jsonify
import sqlite3
from models.group_recommender_mf import GroupRecommenderMF
from models.explicit_mf_with_bias import SGDExplicitBiasMF
import pandas as pd 
import json

from flask_cors import CORS #comment this on deployment

app = Flask(__name__, static_folder="static")
CORS(app) #comment this on deployment

group_mf = GroupRecommenderMF(
    full_model_file_path = "data/model_sgd_mf_v4_50__1666837325.pkl",
    item_encoder_file_path="data/anime_encoder.csv")

anime_df = pd.read_csv("data/anime.csv")

def connect_to_db():
    db_url = "data/6242project.db"
    conn = sqlite3.connect(db_url)
    conn.text_factory = str

    return conn


@app.route('/')
@app.route('/index')
def index():

    conn = connect_to_db()
    get_data = "SELECT * FROM group_rating_sample"
    cursor = conn.execute(get_data)
    data = cursor.fetchall()
    #print(data)  

    conn.close()
    return render_template("index.html")

@app.route('/collect', methods=['POST'])
def collect_form_data():
    data = request.form['jdata']
    data = json.loads(data)

    conn = connect_to_db()
    for i in range(len(data['ratings'])):
        conn.execute("INSERT INTO test(name, anime_name_user_input, rating) VALUES ('{}', '{}', {});"
                    .format(data['name'], data['animes'][i], data['ratings'][i]))
        conn.commit()
    conn.close()    

    return data

@app.route('/predict', methods=['POST'])
def generate_predictions():

    conn = connect_to_db()
    cursor = conn.execute("SELECT name, anime_id, rating FROM group_rating_sample")
    data = cursor.fetchall()
    conn.close()   

    group_rating_df = pd.DataFrame(data, columns=["user_name", "item_id", "rating"])

    recommendations = group_mf.recommend_group(group_rating_df, reg=int(request.form.get("reg")), 
                                                rec_type=request.form.get("rec_type"), 
                                                agg_method=request.form.get("agg_method"))

    users = recommendations.columns[1:-1].to_list()
    
    results = recommendations.merge(anime_df, left_on="item_id", right_on="MAL_ID", how="inner")
    print(results['Genres'])
    results_dict = {"results": []}

    for i in range(10):
        temp = {
            "anime_name": results['English name'][i],
            "overall_score": results['recommendation_score'][i],
            "genres": results['Genres'][i].split(", "),
            "individual_predictions": {}
        }
        for user in users:
            temp["individual_predictions"][user] = results[user][i]

        results_dict["results"].append(temp.copy())
        

    return jsonify(results_dict)
 
if __name__ == '__main__':
    app.run(debug=True)