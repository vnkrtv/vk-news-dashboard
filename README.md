# vk-news-dashboard

[![Build Status](https://travis-ci.com/LeadNess/vk-news-dashboard.svg?branch=master)](https://travis-ci.com/LeadNess/vk-news-dashboard)

### Description

Simple dashboard implemented on Dash. Provides monitoring VK news groups posts:
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
Run script which builds docker-compose service:
-  ```./deploy/deploy_service```  
Run service:
-  ```docker-compose up```
