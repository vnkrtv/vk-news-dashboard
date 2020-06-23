# vk-news-dashboard

[![Build Status](https://travis-ci.com/LeadNess/vk-news-dashboard.svg?branch=master)](https://travis-ci.com/LeadNess/vk-news-dashboard)

### Description

[Simple dashboard](http://leadness.keenetic.name:8050/) implemented on Dash. Provides monitoring VK news groups posts:
- information about group:
  - members count
  - mean views count
  - mean likes count
  - mean comments count
  - mean reposts count
- 2D line plot with likes count for each post
- 2D line plot with comments count for each post
- 2D line plot with views count for each post
- 2D line plot with reposts count for each post
- latest news headlines from selected groups updated every 10 minutes

### Usage 

Clone this repository:
- ```git clone https://github.com/LeadNess/vk-news-dashboard.git```
- ```cd vk-news-dashboard```  

Clone [service](https://github.com/LeadNess/go-vk-news-loader) which provides loading news from VK groups to PostgreSQL:
-  ```git clone https://github.com/LeadNess/go-vk-news-loader.git``` 

Set list of vk groups screen names in go-vk-news-loader/config/groups.json. Default groups.json content:
- ```["meduzaproject", "ria", "kommersant_ru", "tj", "rbc"]```

Run script which builds docker-compose service:
-  ```./deploy/deploy_service```  

Run service:
-  ```docker-compose up```
