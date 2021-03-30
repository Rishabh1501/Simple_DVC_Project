import pytest
import os
import joblib
import json
import logging
from prediction_service.prediction import api_response, form_response
import prediction_service

input_data = {
    "incorrect_range":
        {"fixed_acidity": 7897897,
         "volatile_acidity": 555,
         "citric_acid": 99,
         "residual_sugar": 99,
         "chlorides": 12,
         "free_sulfur_dioxide": 789,
         "total_sulfur_dioxide": 75,
         "density": 2,
         "pH": 33,
         "sulphates": 9,
         "alcohol": 9
         },

    "correct_range":
        {"fixed_acidity": 5,
         "volatile_acidity": 1,
         "citric_acid": 0.5,
         "residual_sugar": 10,
         "chlorides": 0.5,
         "free_sulfur_dioxide": 3,
         "total_sulfur_dioxide": 75,
         "density": 1,
         "pH": 3,
         "sulphates": 1,
         "alcohol": 9
         },

    "incorrect_col":
        {"fixedacidity": 5,
         "volatileacidity": 1,
         "citricacid": 0.5,
         "residualsugar": 10,
         "chlorides": 0.5,
         "freeulfur dioxide": 3,
         "totalsulfur dioxide": 75,
         "density": 1,
         "pH": 3,
         "sulphates": 1,
         "alcohol": 9
         },

    "string_values":
        {"fixed_acidity": "a",
         "volatile_acidity": "b",
         "citric_acid": "c",
         "residual_sugar": "d",
         "chlorides": "e",
         "free_sulfur_dioxide": "f",
         "total_sulfur_dioxide": "g",
         "density": "h",
         "pH": "i",
         "sulphates": "j",
         "alcohol": "k"
         }

}

TARGET_range = {
    "min": 3.0,
    "max": 8.0
}


def test_form_response_correct_range(data=input_data["correct_range"]):
    res = form_response(data)
    assert TARGET_range["min"] <= res <= TARGET_range["max"]


def test_api_response_correct_range(data=input_data["correct_range"]):
    res = api_response(data)
    assert TARGET_range["min"] <= res["response"] <= TARGET_range["max"]


def test_form_response_incorrect_range(data=input_data["incorrect_range"]):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)


def test_api_response_incorrect_range(data=input_data["incorrect_range"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInRange().message


def test_api_response_incorrect_col(data=input_data["incorrect_col"]):
    res = api_response(data)
    assert res["response"] == prediction_service.prediction.NotInCols().message


def test_api_response_string_value(data=input_data['string_values']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.WrongType().message
