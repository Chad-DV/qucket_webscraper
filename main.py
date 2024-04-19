import os
import csv
import json
from datetime import datetime
from bs4 import BeautifulSoup
from requests_html import HTMLSession

events = []
session = HTMLSession()

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
        print(f"Error: {e}")
        return None, None
    
def get_location_information(location):
    location_type = location.get('@type')
    if location_type.lower() == 'place':    
        address = location.get('address')
        street_address = address.get('streetAddress').replace(', ','_')
        return  location.get('name') if street_address == ''  else street_address 
    elif location_type.lower() == 'virtuallocation':
        return location.get('url')
    
def write_to_csv(events_list):
    """
    wirtes a list of dictionaries to .csv file in the same directory as this script
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path,'events.csv')
    fieldnames = events_list[0].keys()

    # Open CSV file in write mode
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for event in events_list:
            writer.writerow(event)

    print("CSV file has been created successfully.")

def current_time()->str:
    """
    Returns the current time as string
    """
    now  = str(datetime.today())
    date = now.split(' ')[0]
    time = str(now.split(' ')[1].split('.')[0])
    return f'{date}_{time}'


def get_html_data(url,page_number):
    """
    Fetches HTML data from website & appends to a list
    """
    if page_number>10:
        return
    
    print("Fetching content from page: ", page_number)
    page_url = f"{url}{page_number}/"
    response = session.get(page_url)
    response.html.render()

    soup = BeautifulSoup(response.html.html,'html.parser')
    script_tag = soup.find('script', type='application/ld+json')

    json_data = script_tag.string
    event_data = json.loads(json_data)

    for item in event_data:
        date, time = iso_8601_to_standard_date_time(item.get('startDate'))
        event = {
            "Title":item.get('name').replace(', 'and' ','_'),
            "Location":get_location_information(item.get('location')),
            "Date":date,
            "Time":time
        }
        events.append(event)
    page_number += 1
    get_html_data(url,page_number)

url = "https://www.quicket.co.za/events/"

get_html_data(url,1)
write_to_csv(events)    