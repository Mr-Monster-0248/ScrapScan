import requests
import shutil
import os
import cfscrape


test_fin = "https://c.japscan.co/lel/One-Piece-Party/1/09.jpg"

scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
resp = scraper.get(test_fin, stream=True)

print(resp.raw)

local_file = open("test.jpg", 'wb')

# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
resp.raw.decode_content = True

# Copy the response stream raw data to local image file.
shutil.copyfileobj(resp.raw, local_file)

# Remove the image url response object.
del resp