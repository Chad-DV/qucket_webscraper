# quicket_webscraper
Script creates a csv with web scraped data from  https://www.quicket.co.za/events/
will only scrape the 1st 10 pages

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Future-Features](#future-features)

## Installation
- clone repository.
- create a virtual enviroment.
- install all requirements in requirements.txt

## Usage
- run main.py
- a one time download of chromium will start if this fails point to a different cromium revision. (instructiions below)

- navigate to .venv/Lib/pyppeteer/__init__.py
- change the chromium revision to a different version
- (changed from __chromium_revision__ = '1181205' to -> __chromium_revision__ = '1263111')
- revison 1181205 is no longer hosted online and will dot be downloadable

## Future-Features
- employ some rate-limiting featurs