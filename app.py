import requests
import sys

def get_location_by_zip(zip_code):
    """
    Fetches city and state information for a given ZIP code using the zipopotam.us API.
    """
    url = f"http://api.zippopotam.us/us/{zip_code}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            city = data['places'][0]['place name']
            state = data['places'][0]['state']
            return city, state
        else:
            print(f"Error: Unable to fetch data for ZIP code {zip_code}. Status code: {response.status_code}")
            return None, None
    except requests.RequestException as e:
        print(f"Error: An exception occurred while fetching data: {e}")
        return None, None

def get_temperature(city, state):
    """
    Fetches the current temperature for a given city and state using the wttr.in API.
    Returns the temperature in Celsius.
    """
    url = f"https://wttr.in/{city}+{state}?format=%t"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Response comes in format like "-1°C" or "+72°F"
            temperature_str = response.text.strip()
            if temperature_str.endswith("°C"):
                return temperature_str[:-2].strip()  # Remove the unit (°C)
            elif temperature_str.endswith("°F"):
                # Convert Fahrenheit to Celsius
                temperature = (float(temperature_str[:-2].strip()) - 32) * 5/9
                return str(round(temperature))
            else:
                print(f"Unexpected temperature format: {temperature_str}")
                return None
        else:
            print(f"Error: Unable to fetch temperature for {city}, {state}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error: An exception occurred while fetching temperature: {e}")
        return None

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python app.py <ZIP_CODE>")
    sys.exit(1)

  zip_code = sys.argv[1]

  city, state = get_location_by_zip(zip_code)

  if city and state:
    print(f"The ZIP code {zip_code} corresponds to {city}, {state}.")
    temperature = get_temperature(city, state)
    if temperature is not None:
      print(f"The current temperature in {city}, {state} is {temperature}°C.")
    else:
      print("Failed to retrieve temperature information.")
  else:
    print("Failed to retrieve location information.")
