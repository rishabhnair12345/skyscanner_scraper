import requests
import configparser
import os
import json
from urllib.parse import urlencode

# Custom case-insensitive config parser
class CaseInsensitiveConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr  # Preserve original case

# Load configuration
config = CaseInsensitiveConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'location_ids.properties')
config.read(config_path)

def get_flight_prices(api_key, date, origin, origin_id, destination, destination_id, 
                     cabin_class="economy", adults=1, children=0, infants=0, 
                     locale="en-US", market="IN", currency="INR"):  # Fixed market code to ISO format
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
        "currency": currency # Now using ISO country code "IN" instead of "India"
    }
    
    headers = {
        "x-rapidapi-host": "skyscanner89.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

# Get user input with validation (unchanged)
def get_airport_code(prompt):
    while True:
        code = input(prompt).strip().upper()
        try:
            return config.get('DEFAULT', code), code
        except configparser.NoOptionError:
            valid_codes = ', '.join(config.options('DEFAULT'))
            print(f"Invalid code. Valid options: {valid_codes}\n")

# Improved flight data processing
def process_flight_data(flight_data):
    if not flight_data:
        print("No flight data received.")
        return

    # Save raw response
    with open("flight_data.json", "w", encoding="utf-8") as file:
        json.dump(flight_data, file, indent=4)
    
    print("\nFlight data saved to flight_data.json")

    # Extract itineraries from buckets
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

    # Process pricing information
    print("\n✈️ Available Flights:")
    cheapest = float('inf')
    currency = ""
    
    for flight in all_flights:
        if not isinstance(flight, dict):
            continue
            
        price_info = flight.get("price", {})
        legs = flight.get("legs", [])
        
        if not price_info or not legs:
            continue
            
        try:
            # Extract price details - FIXED KEY FROM "rawPrice" TO "raw"
            raw_price = price_info.get("raw")
            formatted_price = price_info.get("formatted", "$0")
            currency = formatted_price[0] if formatted_price else "$"
            
            # Extract airline names from all legs
            carriers = set()
            for leg in legs:
                for carrier in leg.get("carriers", {}).get("marketing", []):
                    carriers.add(carrier.get("name", "Unknown"))
            
            # Extract flight times
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
            continue

    if cheapest != float('inf'):
        print(f"\n💰 Cheapest Flight Price: {currency}{cheapest:.2f}")
    else:
        print("\nNo valid flight prices found.")


# Main execution (unchanged)
if __name__ == "__main__":
    api_key = "8d87e94546msh8fc03683c05156dp12c09fjsn145a5a14314d"  # Replace with your key
    
    date = input("Enter the date (yyyy-mm-dd): ")
    
    # Get destination with validation
    destination_id, destination = get_airport_code("Enter destination code (e.g., JRG): ")
    print(f"Destination: {destination} (ID: {destination_id})")
  
    # Get origin with validation
    origin_id, origin = get_airport_code("Enter origin code (e.g., BBI): ")
    print(f"Origin: {origin} (ID: {origin_id})")
    
    # Fetch flight data
    flight_data = get_flight_prices(
        api_key=api_key,
        date=date,
        origin=origin,
        origin_id=origin_id,
        destination=destination,
        destination_id=destination_id
    )
    
    # Process and display flights
    process_flight_data(flight_data)