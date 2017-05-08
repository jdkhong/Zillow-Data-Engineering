# -*- coding: utf-8 -*-
import time
import zillow_functions as zl
from bs4 import BeautifulSoup
import boto
import pandas as pd


# List of zip codes
df = pd.read_csv('~/Programming/zillow/work_zip_codes1.csv')

# CHANGE THE S3 FOLDER NAME!!!
# state = df[df['zip'] == 95138]
temp = df.ix[:, 'zip'].tolist()
# zipcodes = [temp[(i + 1) * 20: (i + 2) * 20] for i in range(int(len(temp) / 20))]


# Initialize the webdriver.
driver = zl.init_driver("/anaconda/bin/chromedriver")

# Go to www.zillow.com/homes
zl.navigate_to_website(driver, "http://www.zillow.com/homes")

# Click the "buy" button.
zl.click_buy_button(driver)


def scrape_data(zc):
    st = zc

    conn = boto.connect_s3()
    bucket = conn.get_bucket('zillowstreamjk')

    # Create 11 variables from the scrapped HTML data.
    # These variables will make up the final output dataframe.
    # df = pd.DataFrame({'address': [],
    #                    'bathrooms': [],
    #                    'bedrooms': [],
    #                    'city': [],
    #                    'days_on_zillow': [],
    #                    'price': [],
    #                    'sale_type': [],
    #                    'state': [],
    #                    'sqft': [],
    #                    'url': [],
    #                    'zip': []})

    # Get total number of search terms.
    numSearchTerms = len(st)

    # Start the scraping.

    for k in range(numSearchTerms):
        # Define search term (must be str object).
        search_term = st[k]

        # Enter search term and execute search.
        if zl.enter_search_term(driver, search_term):
            print("Entering search term number " + str(k + 1) +
                  " out of " + str(numSearchTerms))
        else:
            print("Search term " + str(k + 1) +
                  " failed, moving onto next search term\n***")
            continue

        # Check to see if any results were returned from the search.
        # If there were none, move onto the next search.
        if zl.results_test(driver):
            print("Search " + str(search_term) +
                  " returned zero results. Moving onto the next search\n***")
            continue

        # Pull the html for each page of search results. Zillow caps results at
        # 20 pages, each page can contain 26 home listings, thus the cap on home
        # listings per search is 520.
        rawdata = zl.get_html(driver)
        print(str(len(rawdata)) + " pages of listings found")
        listings = zl.get_listings(rawdata)
        # Take the extracted HTML and split it up by individual home listings.

        k = boto.s3.key.Key(bucket)
        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S", localtime)
        k.key = 'market/general/LA' + ''.join(timeString)
        k.content_type = 'text/html'
        k.set_contents_from_string(str(listings), policy='public-read')


# for key, value in enumerate(zipcodes):
#     scrape_data(value)
scrape_data(temp)
# scrape_data(['94105'])

# Close the webdriver connection.
zl.close_connection(driver)


# For each home listing, extract the 11 variables that will populate that
# specific observation within the output dataframe.

# for n in range(len(listings)):
#     soup = BeautifulSoup(listings[n], "html5lib")
#     new_obs = []
#
#     # List that contains number of beds, baths, and total sqft (and
#     # sometimes price as well).
#     card_info = zl.get_card_info(soup)
#
#     # Street Address
#     new_obs.append(zl.get_street_address(soup))
#
#     # Bathrooms
#     new_obs.append(zl.get_bathrooms(card_info))
#
#     # Bedrooms
#     new_obs.append(zl.get_bedrooms(card_info))
#
#     # City
#     new_obs.append(zl.get_city(soup))
#
#     # Days on the Market/Zillow
#     new_obs.append(zl.get_days_on_market(soup))
#
#     # Price
#     new_obs.append(zl.get_price(soup, card_info))
#
#     # Sale Type (House for Sale, New Construction, Foreclosure, etc.)
#     new_obs.append(zl.get_sale_type(soup))
#
#     # Sqft
#     new_obs.append(zl.get_sqft(card_info))
#
#     # State
#     new_obs.append(zl.get_state(soup))
#
#     # URL for each house listing
#     new_obs.append(zl.get_url(soup))
#
#
#     # Zipcode
#     new_obs.append(zl.get_zipcode(soup))
#
#     # Append new_obs to df as a new observation
#     if len(new_obs) == len(df.columns):
#         df.loc[len(df.index)] = new_obs


# # Write df to CSV.
# columns = ['address', 'city', 'state', 'zip', 'price', 'sqft', 'bedrooms',
#            'bathrooms', 'days_on_zillow', 'sale_type', 'url']
#
# df = df[columns]
# dt = time.strftime("%Y-%m-%d") + "_" + time.strftime("%H%M%S")
# filename = str(dt) + ".csv"
# df.to_csv(filename, index=False)
