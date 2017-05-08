# -*- coding: utf-8 -*-
import time
import zillow_sold_functions as zsl
from bs4 import BeautifulSoup
import boto
import pandas as pd
import json

# List of zip codes
df = pd.read_csv('~/Programming/zillow/work_zip_codes1.csv')

# CHANGE THE S3 FOLDER NAME!!! ended on 45 of 57
# state = df[df['zip'] == 95138]
temp = df.ix[:, 'zip'].tolist()
#temp = df.ix[:, 'zip'].tolist()

# Initialize the webdriver.
driver = zsl.init_driver("/anaconda/bin/chromedriver")

# Go to www.zillow.com/homes
zsl.navigate_to_website(driver, "https://www.zillow.com/homes/recently_sold")


def scrape_data(zc):
    st = zc
    print(st)
    # Get total number of search terms.
    numSearchTerms = len(st)

    # Start the scraping.
    conn = boto.connect_s3()
    bucket = conn.get_bucket('zillowstreamjk')

    for k in range(numSearchTerms):
        # Define search term (must be str object).
        search_term = st[k]

        # Enter search term and execute search.
        if zsl.enter_search_term(driver, search_term):
            print("Entering search term number " + str(k + 1) +
                  " out of " + str(numSearchTerms))
        else:
            print("Search term " + str(k + 1) +
                  " failed, moving onto next search term\n***")
            continue

        # Check to see if any results were returned from the search.
        # If there were none, move onto the next search.
        if zsl.results_test(driver):
            print("Search " + str(search_term) +
                  " returned zero results. Moving onto the next search\n***")
            continue

        # Pull the html for each page of search results. Zillow caps results at
        # 20 pages, each page can contain 26 home listings, thus the cap on home
        # listings per search is 520.
        rawdata = zsl.get_html(driver)
        print(str(len(rawdata)) + " pages of listings found")
        # listings = zsl.get_listings(rawdata)
        # Take the extracted HTML and split it up by individual home listings.
        listings = zsl.get_listings(rawdata)

        k = boto.s3.key.Key(bucket)
        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S", localtime)
        k.key = 'rawdata/sold/general/' + ''.join(timeString)
        k.content_type = 'text/html'
        k.set_contents_from_string(str(listings), policy='public-read')

#
# for key, value in enumerate(zipcodes):
#     scrape_data(value)
scrape_data(temp)

# Close the webdriver connection.
zsl.close_connection(driver)
