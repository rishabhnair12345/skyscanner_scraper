✈️ Skyscanner Flight Price Tracker
A simple Python-based command-line tool to fetch one-way flight prices between two airports using the Skyscanner API (via RapidAPI). Useful for monitoring price trends or searching for the cheapest available flights on a specific date.

📌 Project Overview
This project demonstrates:

✅ Fetching flight data via RapidAPI (Skyscanner)

✅ Loading airport location IDs dynamically from a config file

✅ Parsing and displaying flight prices in a user-friendly format

✅ Writing raw flight data to a local JSON file for debugging

✅ Basic input validation with user prompts

🛠️ Features
🔎 Search for one-way flights between two airports by IATA codes (e.g., HYD to JRG)

🏷️ See the cheapest flight price available

🛫 View airline names and their minimum prices

🗂️ Save raw API response to flight_data.json for analysis or debugging

🧪 Sample Output
bash
Copy
Edit
Enter the date (yyyy-mm-dd): 2025-04-18
Enter destination code (e.g., JRG): JRG
Enter origin code (e.g., BBI): HYD

Flight data retrieved successfully!

✈️ Available Airlines & Prices:
Airline: IndiGo, Min Price: 4500
Airline: SpiceJet, Min Price: 4750

💰 Cheapest Flight Price: ₹4500
📁 Project Structure
graphql
Copy
Edit
skyscanner_scraper/
│
├── run_api.py                 # Main script to run the CLI tool
├── location_ids.properties    # Maps airport codes (e.g., HYD, JRG) to location IDs
├── flight_data.json           # Saved API response (created after each run)
├── README.md                  # You're here!
⚙️ Setup Instructions
1. 🔑 Get Your API Key
Sign up at RapidAPI

Subscribe to the Skyscanner API

Get your x-rapidapi-key

2. 📦 Install Dependencies
bash
Copy
Edit
pip install requests
3. 🗺️ Set Up Airport Location IDs
Create a file named location_ids.properties in the same folder with content like:

ini
Copy
Edit
HYD = 128668073
JRG = 200548629
DEL = 27539733
4. ▶️ Run the Script
bash
Copy
Edit
python run_api.py

📝 Notes
The script writes the full JSON API response to flight_data.json after each run.

IATA codes (e.g., HYD, JRG) must be present in the location_ids.properties file.

The API is rate-limited on the free tier — use it cautiously or upgrade your plan.

📌 TODO / Improvements
 Add support for round-trip searches

 Email notification when price drops below threshold

 Deploy to cloud and run on a schedule

 Integrate with Telegram bot or Slack

🧑‍💻 Author
Crafted with 💻 by Rishabh Nair

