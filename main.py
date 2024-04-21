import os
import sys
import csv
import json
import logging
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from requests_html import HTMLSession

ROOT_DIR =os.path.dirname(__file__)
EVENTS_FILE_PATH = os.path.join(ROOT_DIR, 'events.csv')
QUICKET_URL = "https://www.quicket.co.za/events/"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(ROOT_DIR, "error.log"))
    ]
)

def iso_8601_to_standard_date_time(datetime_str):
    """
    Convert a datetime string from ISO 8601 format to a standard date-time format.
    """
    try:
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ")
        date = datetime_obj.strftime("%Y-%m-%d")
        time = datetime_obj.strftime("%H:%M:%S")
        return date, time
    except ValueError as e:
        logging.error(f"Error converting ISO 8601 datetime: {e}")
        return None, None
    
def get_location_information(location):
    location_type = location.get('@type', '').lower()
    if location_type == 'place':
        address = location.get('address')
        street_address = address.get('streetAddress', '').replace(',', '_')
        clean_streetaddress = street_address.replace('"','').replace(',', '_')
        return location.get('name') if street_address == '' else clean_streetaddress
    elif location_type == 'virtuallocation':
        return location.get('url')
    else:
        logging.error(f"Unknown location type: {location_type}")
        return None

def write_to_csv(events_list):
    """
    Writes a list of dictionaries to a .csv file in the same directory as this script.
    """
    try:
        fieldnames = events_list[0].keys()
        with open(EVENTS_FILE_PATH, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(events_list)

        print("CSV file has been created successfully.")
    except IndexError as e:
        logging.error(f"Error events list empty: {e}")
    except Exception as e:
        logging.error(f"Error writing to CSV file: {e}")


def get_html_data(url, page_number):
    """
    Fetches HTML data from a website and appends it to a list.
    """
    if page_number > 10:
        return
    
    page_url = f"{url}{page_number}/"
    try:
        response = session.get(page_url)
        response.html.render()

        if response.status_code != 200:
            logging.error(f"Failed to fetch content from {page_url}. Status code: {response.status_code}")
            return

        soup = BeautifulSoup(response.html.html, 'html.parser')
        script_tag = soup.find('script', type='application/ld+json')

        if script_tag:
            json_data = script_tag.string
            event_data = json.loads(json_data)

            for item in event_data:
                date, time = iso_8601_to_standard_date_time(item.get('startDate'))
                event = {
                    "Title": item.get('name', '').replace(',', ' and').replace(' ', '_'),
                    "Location": get_location_information(item.get('location', {})),
                    "Date": date,
                    "Time": time
                }
                events.append(event)

        get_html_data(url, page_number + 1)

    except requests.RequestException as e:
        logging.error(f"Error fetching content from {page_url}: {e}")
    except Exception as e:
        logging.error(f"Error processing content from {page_url}: {e}")

if __name__ == "__main__":
    session = HTMLSession()
    events = []

    get_html_data(QUICKET_URL, 1)
    if events:
        write_to_csv(events)
