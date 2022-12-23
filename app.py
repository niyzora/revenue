from flask import Flask, make_response, request, render_template
import io
from io import StringIO
import csv
import pandas as pd
from pandas import MultiIndex, Int16Dtype
import numpy as np
import joblib

app = Flask(__name__)


def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    
    return """
        <html>
            <body>
                <h1>Barcelona airbnb price prediction</h1>
                </br>
                </br>
                <p> Insert your CSV file with listing data and then download the Result
                <form action="/transform" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" class="btn btn-block"/>
                    </br>
                    </br>
                    <button type="submit" class="btn btn-primary btn-block btn-large">Predict</button>
                </form>
            </body>
        </html>
    """


@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    if not f:
        return "No file"

    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    print(csv_input)

    
    stream.seek(0)
    result = transform(stream.read())
    
    input_file = 'model_xgb.bin'
    with open(input_file, 'rb') as f_in:
        sc, model = joblib.load(f_in)
    
    # reading the table
    df = pd.read_csv(StringIO(result)).T.reset_index().drop('index', axis=1)
    df.columns = df.iloc[0]
    df2 = df[1:].reset_index(drop=True)
    # prediction
    df2['prediction'] = str(round(np.expm1(model.predict(sc.transform(df2)))[0])) + " euro"

    # download the result file
    response = make_response(df2.T.to_csv())
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 9696, debug = True)