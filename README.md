# Zillow Data Engineering End to End Pipeline

### Contents
I. EC2 - initiate a VM with a bootstrap to run essential scripts

II. Scripts - to scrape and parse data. XGBoost Regression

III. Airflow - DAG setup

IV. Spark - Pushing data to Postgres DB

V. Presentation - All project objectives can be found here!

[Click here for the interactive dashboard](https://jerrydatascience.tumblr.com/zillow-interactive)

[Click here for machine learning interactive map](https://jerrydatascience.tumblr.com/zillow-machine-learning)


### Brief Introduction
Predictive Analytics with Real Estate Data. My goal is to assess which areas will be good real estate investments based off historical and current market data. I started by picking specific county regions with good employment rates and a large population - SF Bay Area (CA) , Seattle (WA), and Boston (MA).

### Obtaining Data
Initially, I was going to use Zillow's API, however, their API has limited data query and call limits (1000 per day). With a data scraper, I can input a list of zip codes and get details of every listing. Additionally, I can make 3x the amount of calls to the Zillow site.

i) Current For Sale Properties
ii) Recently Sold Properties

Historical Real Estate sales by zip code since 1996

Unemployment by zip code -> mapped by County data

### Big Data
   1. **Stream**: Zillow data scrape current properties for sale and recently sold properties with daily airflow DAG on EC2.
   2. **Store**: Storage for unstructed HTML data for each listing in S3.
   3. **Structure**: Parse HTML data and store in S3. Use Apache Spark to put data into Postgres table.
   4. **Synthesize**: 1) Filter average house prices by zip code 2) XGBoost Regression on predicted house prices, plotted with a heat map
   5. **Show**: Interactive Tableau website

### Zillow Automated Scraper
![](https://i.imgur.com/E6RI8Hm.gif)

### Zillow Data Architecture
![](https://i.imgur.com/bLuGWMj.png)

### 8 properties of Big Data

#### Robustness and Fault Tolerance
All systems belong to AWS, which is highly robust. In addition, all systems integrates with one another. If the scraping goes down, data itself will be safe in S3. 

#### Low latency reads and updates
Since the real estate sales cycle is relatively slow, there is no need for real time updates.

#### Scalability
A majority of these technologies are fully scalable. S3 and Spark have high scalability. MySQL or SparkSQL might be a better fit than Postgres for scalability. Tableau is also very scalable.

#### Generalization
This data pipeline architecture is easily extendible for other scraping and can be reused.

#### Extensibility
All of the systems in place support the addition of new data sources, features, and models.

#### Ad hoc queries
Postgres and Tableau will be used to do ad hoc queries. 

#### Minimal maintenance
This system is complex, and requires monitoring to make sure everything is running. I attempted to make an e-mail airflow DAG in case of errors. 
#### Debuggability
Data will always be stored in complete form in S3, so bugs can be easily traced out. Ability for data to be restructured and models can be recomputed if something goes wrong.

