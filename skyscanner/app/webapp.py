from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
from .flights import get_flight_prices, process_flight_data
from .config_loader import get_airport_code, get_location_id
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        origin = request.form['origin']
        destination = request.form['destination']
        date = request.form['date']
        destination_id=get_location_id(destination)
        origin_id=get_location_id(origin)
        email_id = request.form['email']
        api_key = request.form['api_key'] or os.getenv("RAPIDAPI_KEY")

      
        flights = get_flight_prices(
        api_key=api_key,
        date=date,
        origin=origin,
        origin_id=origin_id,
        destination=destination,
        destination_id=destination_id)
        results = process_flight_data(flights, origin, destination, date)
        msg=Message('Flight Search Results', sender=os.getenv('EMAIL_USER'), recipients=[email_id])
        msg.subject = "Flight Search Results"
        msg.body = "Hello," "\n\n"+results+" \n\nThank you for using our flight search service!"
        mail.send(msg)
        print("Email sent successfully")
        # Render the results on the web page
        return render_template('index.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
