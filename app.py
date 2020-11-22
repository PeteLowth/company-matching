from flask import Flask, request, render_template, url_for
import numpy as np
import pandas as pd
from model import prepare_data, match_companies_knn, build_model

app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def makecalc():
    test_companies = request.get_json()

    df_prediction = match_companies_knn(test_companies, vectorizer, model, df, ignore_words)

    return df_prediction.to_json(orient="records")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/search', methods=['POST', 'GET'])
def search():
    test_companies = [x for x in request.form.values()]

    df_prediction = match_companies_knn(test_companies, vectorizer, model, df, ignore_words)

    n_neighbors = model.get_params()['n_neighbors']

    df_prediction_reshape = pd.DataFrame({
        'CompanyNumber': [df_prediction[f'match.{i}.CompanyNumber'][0] for i in range(n_neighbors)],
        'CompanyName': [df_prediction[f'match.{i}.CompanyName'][0] for i in range(n_neighbors)],
        'Score': [df_prediction[f'match.{i}.Distance'][0] for i in range(n_neighbors)]
    })

    return render_template("home.html", pred=df_prediction_reshape.to_html())


if __name__ == '__main__':
    datafile = 'data/BasicCompanyDataAsOneFile-2020-11-01.csv'

    ignore_words = ['LIMITED', 'LTD', 'PLC', 'LLP', 'GROUP', 'CO', 'COMPANY', 'UK']

    print('...Preparing companies house data')
    df = prepare_data(datafile, ignore_words)

    print('...Building the model')
    vectorizer, model = build_model(df, n_neighbors=10)

    app.run(debug=True, host='0.0.0.0')