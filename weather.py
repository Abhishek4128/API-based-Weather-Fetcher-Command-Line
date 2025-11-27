import argparse
import json
import os
import sys
import time
from dotenv import load_dotenv
import requests
# Define the core components of our API request as constants.
# Using uppercase variable names is a convention to indicate that these values
# are constants and should not be changed during the program's execution.
load_dotenv()
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CACHE_FILE = "cache.json"
CACHE_DURATION_SECONDS = 600

def get_weather_data(city, api_key, units="metric"):
  if os.path.exists(CACHE_FILE):
      with open(CACHE_FILE, 'r') as f:
        try:
            cache_data = json.load(f)
            if city.lower() in cache_data:
                city_cache = cache_data[city.lower()]
                cached_timestamp = city_cache.get("timestamp", 0)
                
                if time.time() - cached_timestamp < CACHE_DURATION_SECONDS:
                    print(f"DEBUG: Cache hit for '{city}'. Using cached data.")
                    return city_cache["data"] # Use the cache
                else:
                    print(f"DEBUG: Cache for '{city}' is stale. Fetching new data.")
        except json.JSONDecodeError:
                # If the JSON is invalid or the file is empty, we treat the cache as empty.
                print("DEBUG: Cache file is empty or corrupted.")
  print(f"DEBUG: Cache miss or stale data. Making a new API call for '{city}'.")  
  request_url = f"{BASE_URL}?q={city}&appid={api_key}&units={units}"

  try:
# Use the requests library to send an HTTP GET request to the constructed URL.
# The server's response is captured in a Response object, which we name 'response'.
   response = requests.get(request_url)
   response.raise_for_status()

# Check the status code of the response.
# A status code of 200 means the request was successful ('OK').
    # If the request was successful, print a confirmation message.
    # We will soon replace this with the code to process the actual weather data.
   data = response.json()
   weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
    }
   full_cache = {}
   if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            try:
                full_cache = json.load(f)
            except json.JSONDecodeError:
                    pass # Start with an empty cache if file is invalid
        
   full_cache[city.lower()] = {
        "data": weather_info,
        "timestamp": time.time()
    }
        
   with open(CACHE_FILE, 'w') as f:
        json.dump(full_cache, f, indent=4)
   print(f"DEBUG: Saved new data for '{city}' to cache.")
   
   return weather_info

  except requests.exceptions.HTTPError as http_err:
    # This block will be executed for any 4xx or 5xx HTTP status codes.
    if http_err.response.status_code == 401:
        print("Error: Invalid API Key. Please check your .env file.")
    elif http_err.response.status_code == 404:
        print(f"Error: City '{city}' not found. Please check the spelling.")
    else:
        # For all other HTTP errors, print the default error message.
        print(f"An HTTP error occurred: {http_err}")
    return None

  except requests.exceptions.RequestException as e:
    # This will catch any network-related errors (e.g., no internet, DNS failure).
    print(f"Network error: Could not connect to the weather service.")
    print(f"Details: {e}")
    return None 
    # Exit the script with a non-zero status code to indicate an error.
def display_weather_data(data,units):
   unit_symbol = "°C" if units == "metric" else "°F"
   print() 
   print(f"Weather in {data['city']}:")
   print("-" * 20) 
   print(f"Temperature: {data['temperature']}{unit_symbol}")
   print(f"Humidity: {data['humidity']}%")
   print(f"Conditions: {data['description'].capitalize()}\n")

def main():
   parser = argparse.ArgumentParser(description="Get the current weather for a specific city.")
   parser.add_argument("city", help="The name of the city to get the weather for.")
   parser.add_argument(
        "--units",
        choices=["metric", "imperial"],
        default="metric",
        help="The units for temperature (metric=Celsius, imperial=Fahrenheit). Default: metric",
    )
   args = parser.parse_args()
   api_key = os.getenv("OPENWEATHER_API_KEY")
   if not api_key:
        print("Error: OPENWEATHER_API_KEY not found.")
        print("Please create a .env file and add your API key to it.")
        sys.exit(1) 

   weather_data = get_weather_data(args.city, api_key, args.units)

# --- NEW LOGIC TO HANDLE THE FUNCTION'S RETURN VALUE ---
# Check if the function returned valid data before trying to print it.
   if weather_data:
      display_weather_data(weather_data, args.units)

if __name__ == "__main__":
    main()