import os
from flights import get_flight_prices, process_flight_data
from config_loader import get_airport_code

from dotenv import load_dotenv
load_dotenv()

def main():
    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        raise ValueError("Missing RAPIDAPI_KEY in environment variables")

    date = input("Enter the date (yyyy-mm-dd): ")

    destination_id, destination = get_airport_code("Enter destination code (e.g., JRG): ")
    print(f"Destination: {destination} (ID: {destination_id})")

    origin_id, origin = get_airport_code("Enter origin code (e.g., BLR): ")
    print(f"Origin: {origin} (ID: {origin_id})")

    flight_data = get_flight_prices(
        api_key=api_key,
        date=date,
        origin=origin,
        origin_id=origin_id,
        destination=destination,
        destination_id=destination_id
    )

    process_flight_data(flight_data, origin, destination, date)

if __name__ == "__main__":
    main()