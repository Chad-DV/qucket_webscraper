# quicket_webscraper
Script creates a csv with web scraped data from  https://www.quicket.co.za/events/
will only scrape the 1st 10 pages

## Installation
I had to change the code in pyppeteer's __init__ file to point to a  existing chromium repo version (changed from __chromium_revision__ = '1181205' to -> __chromium_revision__ = '1263111')