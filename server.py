import ast
import os
import sys
import requests
import pandas as pd
from sklearn.externals import joblib
from flask import jsonify, request, make_response, send_from_directory
import dill as pickle

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

import logger
from app import app, mongo

# Creating a logger object to log the info and debug
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Porting variable to run the server on.
PORT = os.environ.get('PORT')

# Loading the saved model
CLF_FILENAME = 'model_v2.pk'
LOG.debug("Loading the model...")
loaded_model = None
with open(CLF_FILENAME,'rb') as f:
    loaded_model = pickle.load(f)
LOG.debug("The model has been loaded.")


@app.errorhandler(404)
def not_found(error):
    """
    Error handler
    """
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/show', methods=['GET'])
def apicall_getting_info():
    """
    API Call
    Getting all data from db(history of all queries)
    """
    l = [_ for _ in mongo.db.historyOfQueries["hw_collection"].find()]
    return make_response(jsonify({'result':l}), 200)


@app.route('/predict', methods=['POST'])
def apicall():
    """
    API Call
    Making predictions on house price based on descriptive data
    """
    request_json = request.get_json()
    try:
        df_test = pd.DataFrame(request_json)
    except Exception as e:
        raise e

    if df_test.empty:
        return(bad_request())
    else:
        # Running predictions
        LOG.info('Doing predictions now...')
        predictions = loaded_model.predict(df_test)
        prediction_series = list(pd.Series(predictions))
        final_predictions = pd.DataFrame(prediction_series)
        # Creating response for a query
        json_final_data = ast.literal_eval(final_predictions.to_json(orient="records", force_ascii=False))
        responses = jsonify(predictions=json_final_data)
        responses.status_code = 200
        # Saving data to db
        try:
            mongo.db.historyOfQueries["hw_collection"].insert_one({"input_data": request_json, "predictions": json_final_data})
        except Exception as e:
            print(e)

        return (responses)


if __name__ == '__main__':
    # Enabling debug mode if development env
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))
