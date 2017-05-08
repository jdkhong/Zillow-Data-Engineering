from bs4 import BeautifulSoup
import ast
import time
import pandas as pd
from io import StringIO
import boto3
import boto
import zillow_sold_functions as zsl

df = pd.DataFrame({'address': [],
                   'bathrooms': [],
                   'bedrooms': [],
                   'city': [],
                   'sale_type': [],
                   'state': [],
                   'sqft': [],
                   'url': [],
                   'zip': [],
                   'zpid':[]})


conn = boto.connect_s3()
bucket = conn.get_bucket('zillowstreamjk')

# CHANGE BUCKET NAME
for key in bucket.list(prefix='rawdata/sold/AZ'):
    sonnets = bucket.get_key(key.key)
    text = sonnets.get_contents_as_string(encoding='utf-8')
    x = ast.literal_eval(text)

    for n in range(len(x)):
        soup = BeautifulSoup(x[n], "lxml")
        new_obs = []

        # List that contains number of beds, baths, and total sqft (and
        # sometimes price as well).
        card_info = zsl.get_card_info(soup)

        # Street Address
        new_obs.append(zsl.get_street_address(soup))

        # Bathrooms
        new_obs.append(zsl.get_bathrooms(card_info))

        # Bedrooms
        new_obs.append(zsl.get_bedrooms(card_info))

        # City
        new_obs.append(zsl.get_city(soup))


        # Sale Type (House for Sale, New Construction, Foreclosure, etc.)
        new_obs.append(zsl.get_sale_type(soup))

        # Sqft
        new_obs.append(zsl.get_sqft(card_info))

        # State
        new_obs.append(zsl.get_state(soup))

        # URL for each house listing
        new_obs.append(zsl.get_url(soup))

        # Zipcode
        new_obs.append(zsl.get_zipcode(soup))

        # Zipcode
        new_obs.append(zsl.get_id(soup))

        # Append new_obs to df as a new observation
        if len(new_obs) == len(df.columns):
            df.loc[len(df.index)] = new_obs


# Write df to CSV.
columns = ['address', 'city', 'state', 'zip', 'sqft', 'bedrooms',
               'bathrooms', 'sale_type', 'url', 'zpid']

df = df[columns]
localtime = time.localtime()
timeString = time.strftime("%Y%m%d%H%M%S", localtime)
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
# Upload CSV to S3, REMEMBER TO CHANGE KEY NAME
s3_key = 'parsed/sold/AZ/' + ''.join(timeString) + ".csv"
s3_resource = boto3.resource('s3')
s3_resource.Object('zillowstreamjk', s3_key).put(Body=csv_buffer.getvalue())