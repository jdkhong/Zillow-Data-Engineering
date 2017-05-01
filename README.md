# Zillow Data Engineering End to End Pipeline
Predictive Analytics with Real Estate Data. My goal is to assess which areas will be good investments based off historical. I started by picking 5 specific county regions with good employment rates and a large population - SF Bay Area (CA) , King County (WA), (MA), (MN), (TX).

#### Obtaining Data
Scrape Zillow's Real Estate Data
i) Current For Sale Properties
ii) Recently Sold Properties

Historical Real Estate sales by zip code since 2012

Unemployment by zip code -> mapped by County data

#### Big Data
   1. **Stream**: A way to continuously query data from a website or API (at least one, but preferably two sources of data)
   2. **Store**: Storage for all unstructured data in its entirety
   3. **Structure**: Separate storage for structured data in 3NF (similar to how we stored raw tweets in s3 and structured tables in postgres)
   4. **Synthesize**: Some sort of batch process/transformation with Spark
   5. **Show**: A way to communicate the results of your pipeline such as a static website or flask app

2. Take a look at each of the 8 desired properties of a big data system and answer the following two questions:
    1. How does my system have this property?
    2. How does my system fall short and how could it be improved?

## Zillow Automated Scraper
![](https://i.imgur.com/E6RI8Hm.gif)

## Zillow Data Architecture
![](https://i.imgur.com/bLuGWMj.png)
