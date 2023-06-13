from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pandas as pd

from predictor import Predictor

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


predictor = Predictor()


def make_dataframe_from_json(data):
    # Чтобы конвертировать JSON в DataFrame нам нужен пустой DataFrame. В нем указываем
    # только те признаки, которые мы выбрали для обучения модели
    columns = [
        'Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience'
    ]
    df = pd.DataFrame(columns=columns)

    # С помощью функции loc мы перезаписываем элементы dataFrame, в данном случае нам нужен [0] элемент
    df.loc[0, 'Age'] = data.get("age")
    df.loc[0, 'Gender'] = data.get("gender")
    df.loc[0, 'Education Level'] = data.get("edu_level")
    df.loc[0, 'Job Title'] = data.get("job_title")
    df.loc[0, 'Years of Experience'] = data.get("years_exp")

    # Функция возвращает заполненный DataFrame, который может использоваться для предсказания
    return df


# Define predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve the JSON data from the request
    json = request.get_json()

    # Проверяем, что данные были переданы
    if json is None:
        return jsonify({'error': 'no data provided'})

    print('received: ', json)

    df = make_dataframe_from_json(json)

    # Make predictions using the trained model
    predictions = predictor.regressor.predict(df)

    # Create a JSON response containing the predictions
    response_data = {'predictions': predictions.tolist(), 'accuracy': predictor.accuracy}

    response = jsonify(response_data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('port', 5000))
