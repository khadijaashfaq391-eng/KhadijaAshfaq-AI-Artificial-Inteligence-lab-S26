from flask import Flask, render_template, request
import pickle
import joblib
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open('model.pkl', 'rb'))

# Load encoders
encoders = joblib.load('encoders.pkl')

# Load training columns
columns = joblib.load('columns.pkl')


@app.route('/')
def home():
    return render_template(
        'index.html',
        airlines=encoders['Airline'].classes_,
        sources=encoders['Source'].classes_,
        destinations=encoders['Destination'].classes_,
        stops=encoders['Total_Stops'].classes_,
        infos=encoders['Additional_Info'].classes_
    )


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        airline = request.form['Airline']
        source = request.form['Source']
        destination = request.form['Destination']
        total_stops = request.form['Total_Stops']
        additional_info = request.form['Additional_Info']

        journey_day = int(request.form['Journey_Day'])
        journey_month = int(request.form['Journey_Month'])

        duration = int(request.form['Duration'])

        dep_hour = int(request.form['Dep_Hour'])
        dep_min = int(request.form['Dep_Min'])

        arrival_hour = int(request.form['Arrival_Hour'])
        arrival_min = int(request.form['Arrival_Min'])

        # Encode categorical values
        airline = encoders['Airline'].transform([airline])[0]
        source = encoders['Source'].transform([source])[0]
        destination = encoders['Destination'].transform([destination])[0]
        total_stops = encoders['Total_Stops'].transform([total_stops])[0]
        additional_info = encoders['Additional_Info'].transform([additional_info])[0]

        # Create dataframe in exact training order
        input_data = pd.DataFrame([[
            airline,
            source,
            destination,
            total_stops,
            additional_info,
            journey_day,
            journey_month,
            duration,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min
        ]], columns=columns)

        # Prediction
        prediction = model.predict(input_data)[0]

        return render_template(
            'index.html',
            prediction_text=f'Predicted Flight Price: Rs. {round(prediction, 2)}',
            airlines=encoders['Airline'].classes_,
            sources=encoders['Source'].classes_,
            destinations=encoders['Destination'].classes_,
            stops=encoders['Total_Stops'].classes_,
            infos=encoders['Additional_Info'].classes_
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)