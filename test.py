from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Create an HTML session
session = HTMLSession()

# URL of the web page you want to scrape
url = 'https://www.quicket.co.za/events/'

# Send a GET request and render the page
response = session.get(url)

# Render JavaScript and wait for the page to be fully loaded
response.html.render()

soup = BeautifulSoup(response.html.html,'html.parser')
script_tag = soup.find('script', type='application/ld+json')
print(script_tag.string)
quit()
# Extract data using CSS selectors or XPath expressions
# For example, to extract text from all <h1> tags:
headings = response.html.find('script', type='application/ld+json')
for heading in headings:
    print(heading.text)

# Close the session
session.close()