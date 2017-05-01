# Zillow Data Engineering End to End Pipeline
Predictive Analytics with Real Estate Data. My goal is to assess which areas will be good investments based off historical. I started by picking 5 specific county regions with good employment rates and a large population - SF Bay Area (CA) , King County (WA), (MA), (MN), (TX).

#### Obtaining Data
Scrape Zillow's Real Estate Data
i) Current For Sale Properties
ii) Recently Sold Properties

Historical Real Estate sales by zip code since 2012

Unemployment by zip code -> mapped by County data

#### Big Data
   1. **Stream**: Zillow Data Scraping with daily crontab schedule.
   2. **Store**: Storage for unstructed HTML data for each listing.
   3. **Structure**: Separate storage for structured data for each listing in pandas dataframe and Postrgres database.
   4. **Synthesize**: Batch process/transformation with Spark
   5. **Show**: Interactive Tableau website

## Zillow Automated Scraper
![](https://i.imgur.com/E6RI8Hm.gif)

## Zillow Data Architecture
![](https://i.imgur.com/bLuGWMj.png)
