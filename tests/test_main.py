from .. import main
from datetime import datetime


def test_iso_8601_to_standard_date_time_type():
    assert type(main.iso_8601_to_standard_date_time("2024-04-19T00:00:00Z")) is tuple
    
def test_iso_8601_to_standard_date_time():
    date,time = main.iso_8601_to_standard_date_time("2024-04-19T00:00:00Z")
    assert date == "2024-04-19"
    assert time == "00:00:00"

def test_valid_iso_8601_to_standard_date_formats():
    datetime_formats = [
        "2024-04-19T00:00:00Z",       
        "2024-04-19T23:59:59Z",       
    ]
    
    for datetime_str in datetime_formats:
        date, time = main.iso_8601_to_standard_date_time(datetime_str)
        assert date is not None
        assert time is not None

def test_iso_8601_to_standard_date_invalid_format():
    datetime_formats = [       
        "2024-04-19T00:00:00",        
        "2024-04-19 00:00:00",        
        "2024/04/19 00:00:00",        
        "04-19-2024T00:00:00Z",       
        "2024-04-19T23:59:59+05:00",
        "X",
        "04-19-2024",
        "2024/04/19"

    ]
    for datetime_str in datetime_formats: 
        date, time = main.iso_8601_to_standard_date_time(datetime_str)
        assert date is None
        assert time is None



def test_get_location_information_valid_street_address():
    location_data = {
        "@type": "Place",
        "name": "Fernkloof Nature Reserve",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Hermanus, 7200, 7200, Hermanus, Western Cape, South Africa",
            "addressLocality": "Hermanus",
            "postalCode": "7200",
            "addressRegion": "Western Cape",
            "addressCountry": "South Africa"
            }
        }

    output = main.get_location_information(location_data)
    street_address = location_data["address"]["streetAddress"].replace(",","_")
    assert output == street_address

def test_get_location_information_blank_street_address():
    location_data = {
        "@type": "Place",
        "name": "Fernkloof Nature Reserve",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "",
            "addressLocality": "Hermanus",
            "postalCode": "7200",
            "addressRegion": "Western Cape",
            "addressCountry": "South Africa"
            }
        }

    output = main.get_location_information(location_data)
    street_address = location_data["name"].replace(",","_")
    assert output == street_address

def test_get_location_information_empty_dict():
    location_data = {}
    output = main.get_location_information(location_data)
    assert output is None