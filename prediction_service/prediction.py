import joblib
from src.get_data import read_params
import numpy as np
import os
import json

params_path = "params.yaml"
schema_path = os.path.join('prediction_service', 'schema_in.json')


def loading_schema(schema_path=schema_path):
    """a function to load schema from schema_in.json"""
    with open(schema_path) as json_file:
        load_schema = json.load(json_file)
    return load_schema


# Error classes
class NotInRange(Exception):
    def __init__(self, message="Value entered is Not in range"):
        self.message = message
        super().__init__(self.message)


class NotInCols(Exception):
    def __init__(self, message="Name not in Column Names"):
        self.message = message
        super().__init__(self.message)


class WrongType(Exception):
    def __init__(self, message="Wrong Type of value Entered,only"
                               " float or integer values are accepted"):
        self.message = message
        super().__init__(self.message)


# error classes ended


def predict(data):
    config = read_params(params_path)
    model_dir_path = config['webapp_model_dir']
    model = joblib.load(model_dir_path)
    prediction = model.predict(data)[0]

    schema = loading_schema()
    target = schema['TARGET']

    try:
        if target['min'] <= prediction <= target['max']:
            return prediction
        else:
            raise NotInRange

    except NotInRange:
        return "Unexpected Prediction Value"


def validate_input(dict_request):
    def _validate_cols_name_and_val_range(col, val):
        schema = loading_schema()
        col = col.replace('_', ' ')
        if col in schema.keys():
            try:
                if schema[col]["min"] <= float(val) <= schema[col]['max']:
                    return True
                else:
                    raise NotInRange

            except TypeError:
                raise WrongType

        else:
            raise NotInCols

    for col, val in dict_request.items():
        if _validate_cols_name_and_val_range(col, val):
            continue
        else:
            return False

    else:
        return True


def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()
        data = [list(map(float, data))]
        response = predict(data)
        return response


def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.json.values())])
            response = predict(data)
            response = {"response": response}
            return response

    except Exception as e:
        error = {'error': f"Values Entered are not in Range or Column Name is not found "
                          f"correct, Error : {str(e)}",
                 "Expected Range is ": loading_schema()}
        return error
