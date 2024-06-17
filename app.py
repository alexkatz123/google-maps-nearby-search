import csv
import googlemaps
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Replace with your Google Maps API key
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

# Initialize the Google Maps client
gmaps = googlemaps.Client(key=API_KEY)

def get_places(location, activity_type, radius):
    places_details = []
    next_page_token = None

    while True:
        if next_page_token:
            places_result = gmaps.places_nearby(location=location, radius=radius, keyword=activity_type, page_token=next_page_token)
        else:
            places_result = gmaps.places_nearby(location=location, radius=radius, keyword=activity_type)

        for place in places_result['results']:
            place_id = place['place_id']
            details = gmaps.place(place_id=place_id)
            details_result = details['result']

            # Extract website URL if available
            website = details_result.get('website', 'N/A')

            place_info = {
                'Name': details_result.get('name', 'N/A'),
                'Address': details_result.get('formatted_address', 'N/A'),
                'Travel Time': 'N/A',
                'Contact Email': 'N/A',  # Placeholder for contact email
                'Contact Number': details_result.get('formatted_phone_number', 'N/A'),
                'Website': website,
                'Google Maps Link': f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            }
            places_details.append(place_info)

        next_page_token = places_result.get('next_page_token')
        if not next_page_token:
            break

    return places_details

def get_contact_email(website_url):
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Example: extract email from a contact page, using CSS class or other pattern
        email = soup.select_one('a[href^="mailto:"]').get('href').replace('mailto:', '') if soup.select_one('a[href^="mailto:"]') else 'N/A'
        return email
    except Exception as e:
        print(f"Error extracting email from {website_url}: {e}")
        return 'N/A'

def get_travel_times(origin, places):
    destinations = [place['Address'] for place in places]
    travel_times = []

    for chunk in chunk_list(destinations, 25):  # Chunk size set to 25 to stay within limits
        travel_info = gmaps.distance_matrix(origins=[origin], destinations=chunk, mode='driving')
        travel_times.extend(travel_info['rows'][0]['elements'])

    for i, element in enumerate(travel_times):
        if element['status'] == 'OK':
            travel_time = element['duration']['text']
            travel_seconds = element['duration']['value']
        else:
            travel_time = 'N/A'
            travel_seconds = float('inf')
        places[i]['Travel Time'] = travel_time
        places[i]['Travel Seconds'] = travel_seconds

    filtered_places = [place for place in places if place['Travel Seconds'] <= 7200]
    for place in filtered_places:
        del place['Travel Seconds']

    return filtered_places

def write_to_csv(places_details, activity_type):
    headers = ['Name', 'Address', 'Travel Time', 'Contact Email', 'Contact Number', 'Website', 'Google Maps Link']
    filename = f"{activity_type}.csv"

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for place in places_details:
            writer.writerow(place)

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal *= -1
    return decimal

def convert_dms_to_decimal(dms_str):
    dms_str = dms_str.replace('°', ' ').replace("'", ' ').replace('"', ' ')
    parts = dms_str.split()
    latitude = dms_to_decimal(float(parts[0]), float(parts[1]), float(parts[2]), parts[3])
    longitude = dms_to_decimal(float(parts[4]), float(parts[5]), float(parts[6]), parts[7])
    return f"{latitude},{longitude}"

def get_coordinates(location):
    try:
        geocode_result = gmaps.geocode(location)
        lat_lng = geocode_result[0]['geometry']['location']
        return f"{lat_lng['lat']},{lat_lng['lng']}"
    except Exception as e:
        print(f"Error geocoding location '{location}': {e}")
        return None

def main():
    origin = input("Enter your starting location (latitude,longitude or DMS format or postcode): ")
    if not (',' in origin or '°' in origin or "'" in origin):
        origin = get_coordinates(origin)
    elif '°' in origin or "'" in origin:
        origin = convert_dms_to_decimal(origin)

    location = input("Enter the search center location (latitude,longitude or DMS format or postcode): ")
    if not (',' in location or '°' in location or "'" in location):
        location = get_coordinates(location)
    elif '°' in location or "'" in location:
        location = convert_dms_to_decimal(location)

    if not origin or not location:
        print("Invalid location input. Exiting.")
        return

    activity_type = input("Enter the activity type (e.g., swimming): ")

    search_radius = 194000  # in meters

    places_details = get_places(location, activity_type, search_radius)
    
    # Retrieve contact emails from business websites
    for place in places_details:
        if place['Website'] != 'N/A':
            place['Contact Email'] = get_contact_email(place['Website'])

    places_within_2_hours = get_travel_times(origin, places_details)
    write_to_csv(places_within_2_hours, activity_type)

    print(f"Data written to {activity_type}.csv")

if __name__ == '__main__':
    main()

