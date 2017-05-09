# Zillow Data Engineering End to End Pipeline
Predictive Analytics with Real Estate Data. My goal is to assess which areas will be good real estate investments based off historical and current market data. I started by picking specific county regions with good employment rates and a large population - SF Bay Area (CA) , Seattle (WA), and Boston (MA).

#### Obtaining Data
Initially, I was going to use Zillow's API, however, their API has limited data query and call limits (1000 per day). With a data scraper, I can input a list of zip codes and get details of every listing. Additionally, I can make 3x the amount of calls to the Zillow site.

i) Current For Sale Properties
ii) Recently Sold Properties

Historical Real Estate sales by zip code since 2012

Unemployment by zip code -> mapped by County data

#### Big Data
   1. **Stream**: Zillow data scrape current properties for sale and recently sold properties with daily airflow DAG on EC2.
   2. **Store**: Storage for unstructed HTML data for each listing in S3.
   3. **Structure**: Parse HTML data and store in S3. Use Apache Spark to put data into Postgres table.
   4. **Synthesize**: 1) Filter average house prices by zip code 2) XGBoost Regression on predicted house prices, plotted with a heat map
   5. **Show**: Interactive Tableau website

## Zillow Automated Scraper
![](https://i.imgur.com/E6RI8Hm.gif)

## Zillow Data Architecture
![](https://i.imgur.com/bLuGWMj.png)

# 8 properties for Big Data systems :
#### Robustness and fault Tolerance
All systems belong to AWS, which is highly robust. In addition, all systems integrates with one another. If the data scraping goes down, short-term functionality will be lost on the front-end, but the data itself will be safe in S3. One cause of concern is the possibility that Zillow stops the scraping. A resolution to this would be to work with the less efficient Zillow API.

#### Low latency reads and updates
Since the real estate sales cycle is relatively slow, there is no need for real time updates. 

#### Scalability
A majority of these technologies are fully scalable.
S3 and Spark have high scalability. 
In terms of a RDBMS, MySQL or SparkSQL might be a better fit than Postgres for better scalability.
Tableau is also very scalable as it can be directly to servers, RDBMS, Spark, and multiple data sources.

#### Generalization
This data pipeline architecture is easily extendible for any scraping and can be reused for a lot of applications.

#### Extensibility


#### Ad hoc queries
Postgres and Tableau will be used to do ad hoc queries. Both are very good at those types of tasks.

#### Minimal maintainance



#### Debuggability

