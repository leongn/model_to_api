# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

import os
import json
from sklearn.externals import joblib
import flask
import pandas as pd

#Define the path
prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

# Load the model components
tfidf_vectorizer = joblib.load(os.path.join(model_path, 'tfidf_vectorizer.pkl'))
classifier = joblib.load(os.path.join(model_path, 'classifier.pkl'))

# The flask app for serving predictions
app = flask.Flask(__name__)
@app.route('/ping', methods=['GET'])
def ping():
    # Check if the classifier was loaded correctly
    try:
        classifier
        status = 200
    except:
        status = 400
    return flask.Response(response= json.dumps(' '), status=status, mimetype='application/json' )

@app.route('/invocations', methods=['POST']))
def transformation():
    # Get input JSON data and convert it to a DF
    input_json = flask.request.get_json()
    input_json = json.dumps(input_json['input'])
    input_df = pd.read_json(input_json,orient='list')

    # Tokenize data and predict
    input_tokenized = tfidf_vectorizer.transform(input_df.text)
    predictions = list(classifier.predict(input_tokenized))

    # Transform predicted labels (0 and 1) to easier to understand Negative and Positive labels
    predictions = list(map(lambda x: 'Positive' if x == 1 else 'Negative', predictions))

    # Transform predictions to JSON
    result = {'output': []}
    list_out = []
    for label in predictions:
        row_format = {'label': label}
        list_out.append(row_format)
    result['output'] = list_out
    result = json.dumps(result)
    return flask.Response(response=result, status=200, mimetype='application/json')
