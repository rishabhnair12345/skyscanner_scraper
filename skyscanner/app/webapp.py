from flask import Flask, render_template, request
import os
from flights import get_flight_prices, process_flight_data
from config_loader import get_airport_code, get_location_id
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        destination_id=get_location_id(destination)
        origin_id=get_location_id(origin)
        api_key = request.form['api_key'] or os.getenv("RAPIDAPI_KEY")

        if not api_key:
            return render_template('index.html', error="API Key is required.")

        flights = get_flight_prices(
        api_key=api_key,
        date=date,
        origin=origin,
        origin_id=origin_id,
        destination=destination,
        destination_id=destination_id)
        results = process_flight_data(flights, origin, destination, date)
        return render_template('index.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
