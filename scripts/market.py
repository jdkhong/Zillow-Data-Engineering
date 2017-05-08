from bs4 import BeautifulSoup
import ast
import time
import pandas as pd
from io import StringIO
import boto3
import boto
import zillow_functions as zl

df = pd.DataFrame({'address': [],
                   'bathrooms': [],
                   'bedrooms': [],
                   'city': [],
                   'days_on_zillow': [],
                   'price': [],
                   'sale_type': [],
                   'state': [],
                   'sqft': [],
                   'url': [],
                   'zip': [],
                   'zpid': []})


conn = boto.connect_s3()
bucket = conn.get_bucket('zillowstreamjk')

# CHANGE BUCKET NAME
for key in bucket.list(prefix='rawdata/market/AZ'):
    sonnets = bucket.get_key(key.key)
    text = sonnets.get_contents_as_string(encoding='utf-8')
    x = ast.literal_eval(text)

    for n in range(len(x)):
        soup = BeautifulSoup(x[n], "lxml")
        new_obs = []

        # List that contains number of beds, baths, and total sqft (and
        # sometimes price as well).
        card_info = zl.get_card_info(soup)

        # Street Address
        new_obs.append(zl.get_street_address(soup))

        # Bathrooms
        new_obs.append(zl.get_bathrooms(card_info))

        # Bedrooms
        new_obs.append(zl.get_bedrooms(card_info))

        # City
        new_obs.append(zl.get_city(soup))

        # Days on the Market/Zillow
        new_obs.append(zl.get_days_on_market(soup))

        # Price
        new_obs.append(zl.get_price(soup, card_info))

        # Sale Type (House for Sale, New Construction, Foreclosure, etc.)
        new_obs.append(zl.get_sale_type(soup))

        # Sqft
        new_obs.append(zl.get_sqft(card_info))

        # State
        new_obs.append(zl.get_state(soup))

        # URL for each house listing
        new_obs.append(zl.get_url(soup))

        # Zipcode
        new_obs.append(zl.get_zipcode(soup))

        # Zipco
        new_obs.append(zl.get_id(soup))

        # Append new_obs to df as a new observation
        if len(new_obs) == len(df.columns):
            df.loc[len(df.index)] = new_obs


# Write df to CSV.
columns = ['address', 'city', 'state', 'zip', 'price', 'sqft', 'bedrooms',
           'bathrooms', 'days_on_zillow', 'sale_type', 'url', 'zpid']

df = df[columns]
localtime = time.localtime()
timeString = time.strftime("%Y%m%d%H%M%S", localtime)
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
# Upload CSV to S3, REMEMBER TO CHANGE KEY NAME
s3_key = 'parsed/market/AZ/' + ''.join(timeString) + ".csv"
s3_resource = boto3.resource('s3')
s3_resource.Object('zillowstreamjk', s3_key).put(Body=csv_buffer.getvalue())