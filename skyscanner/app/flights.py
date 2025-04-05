import requests
import json
from telegram_alerts import TelegramNotifier

def get_flight_prices(api_key, date, origin, origin_id, destination, destination_id,
                     cabin_class="economy", adults=1, children=0, infants=0,
                     locale="en-US", market="IN", currency="INR"):
    url = "https://skyscanner89.p.rapidapi.com/flights/one-way/list"

    params = {
        "date": date,
        "origin": origin,
        "originId": origin_id,
        "destination": destination,
        "destinationId": destination_id,
        "cabinClass": cabin_class,
        "adults": adults,
        "children": children,
        "infants": infants,
        "locale": locale,
        "market": market,
        "currency": currency
    }

    headers = {
        "x-rapidapi-host": "skyscanner89.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

def process_flight_data(flight_data, origin, destination, date):
    if not flight_data:
        print("No flight data received.")
        return

    with open("flight_data.json", "w", encoding="utf-8") as file:
        json.dump(flight_data, file, indent=4)

    print("\nFlight data saved to flight_data.json")

    try:
        buckets = flight_data.get("data", {}).get("itineraries", {}).get("buckets", [])
    except AttributeError:
        print("Invalid API response structure")
        return

    all_flights = []
    for bucket in buckets:
        if isinstance(bucket, dict) and "items" in bucket:
            all_flights.extend(bucket["items"])

    if not all_flights:
        print("No flight itineraries found in response.")
        return

    print("\n\u2708\ufe0f Available Flights:")
    cheapest = float('inf')
    currency = ""
    carriers = set()

    for flight in all_flights:
        price_info = flight.get("price", {})
        legs = flight.get("legs", [])

        if not price_info or not legs:
            continue

        try:
            raw_price = price_info.get("raw")
            formatted_price = price_info.get("formatted", "$0")
            currency = formatted_price[0] if formatted_price else "$"

            for leg in legs:
                for carrier in leg.get("carriers", {}).get("marketing", []):
                    carriers.add(carrier.get("name", "Unknown"))

            first_segment = legs[0].get("segments", [{}])[0]
            last_segment = legs[-1].get("segments", [{}])[-1]

            departure = first_segment.get("departure", "N/A")
            arrival = last_segment.get("arrival", "N/A")
            stops = sum(leg.get("stopCount", 0) for leg in legs)
            duration = legs[0].get("durationInMinutes", "N/A")

            if raw_price is not None:
                price = float(raw_price)
                cheapest = min(cheapest, price)
                print(f"Carriers: {', '.join(carriers)}")
                print(f"Price: {currency}{price:.2f}")
                print(f"Departure: {departure} | Arrival: {arrival}")
                print(f"Stops: {stops} | Duration: {duration} mins")
                print("-" * 40)

        except (KeyError, TypeError, ValueError) as e:
            print(f"Skipping invalid flight: {str(e)}")

    if cheapest != float('inf'):
        print(f"\n💰 Cheapest Flight Price: {currency}{cheapest:.2f}")
        message = (
            f"\ud83d\udcb0 <b>Cheapest Flight Found!</b>\n"
            f"From: {origin}\n"
            f"To: {destination}\n"
            f"Carriers: {', '.join(carriers)}\n"
            f"Price: {currency}{cheapest:.2f}\n"
            f"Date: {date}"
        )
        notifier = TelegramNotifier()
        if notifier.send_alert(message):
            print("Telegram alert sent successfully!")
        else:
            print("Failed to send Telegram alert")
