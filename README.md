# Zillow Data Engineering End to End Pipeline
Predictive Analytics with Real Estate Data. My goal is to assess which areas will be good real estate investments based off historical and current market data. I started by picking specific county regions with good employment rates and a large population - SF Bay Area (CA) , Seattle (WA), and Boston (MA).

#### Obtaining Data
Initially, I was going to use Zillow's API, however, their API has limited data query and call limits (1000 per day). With a data scraper, I can input a list of zip codes and get details of every listing. Additionally, I can make 3x the amount of calls to the Zillow site.

i) Current For Sale Properties
ii) Recently Sold Properties

Historical Real Estate sales by zip code since 2012

Unemployment by zip code -> mapped by County data

#### Big Data
   1. **Stream**: Zillow data scrape current properties for sale and recently sold properties with daily airflow DAG.
   2. **Store**: Storage for unstructed HTML data for each listing in S3.
   3. **Structure**: Parse HTML data and store in S3. Use Apache Spark to put data into Postgres table.
   4. **Synthesize**: Batch process/transformation with Spark
   5. **Show**: Interactive Tableau website

## Zillow Automated Scraper
![](https://i.imgur.com/E6RI8Hm.gif)

## Zillow Data Architecture
![](https://i.imgur.com/bLuGWMj.png)

# 8 properties for Big Data systems :
#### Robustness and fault Tolerance



#### Low latency reads and updates


#### Scalability



#### Generalization



#### Extensibility


#### Ad hoc queries



#### Minimal maintainance



#### Debuggability

