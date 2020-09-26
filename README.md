# Hansard-Dashboard
### This project aims to build a data analytics dashboard for Singapore's [Hansard](https://sprs.parl.gov.sg/search/home) (record of all parliamentary debates).

The MVP is a dashboard that is able to provide summary statistics on Member of Parliament attendance, number of questions asked (to ministries and by member), bills debated and passed. 

More advanced analytics would include natural language processing techniques (NLP) such as sentiment analysis or topic modelling.

This project is at the stage of scraping data from the Hansard website. All the text can be accessed with ```hansard-scraper.py```, but the structuring of the database is still a work-in-progress. I am currently working on tagging the speaker's name with their text in a json file.

## Requirements
Python 3.7.5

Selenium 3.141.0

webdriver-manager 3.2.1

## How to use
The main code is in ```hansard-scraper.py```, that runs the webscraper through Chromium using selenium. Search parameters can be set such as search by MP name or No. of parliament. It iterates through all returned search results, saving the text of each parliamentary sitting into a json.
