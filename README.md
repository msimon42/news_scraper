# news_scraper
[![Build Status](https://travis-ci.org/msimon42/news_scraper.svg?branch=master)](https://travis-ci.org/msimon42/news_scraper)
### Link to production site: https://www.news-scraper.com/

News Scraper is an app that allows users to provide an email address and links to their favorite blogs or news sites, and sends an email containing articles from those sites every day.  

### How to use this service 

- Navigate to http://www.news-scraper.com/subscribe and enter your email address, along with links to any pages you would like to recieve articles from. 
- Links should be full URLs separated by commas, with no spaces. `https://www.news.org,https://www.blog.com/news, etc.`
- After submitting the form, check your inbox for a confirmation email. Once you confirm, you will start recieving a newsletter with links to articles from the pages you listed every day at around 6:30AM Mountain Time. 
- The service currently works best with news sites or blogs that contain links to articles, like [here](https://www.slashdot.org) or [here](https://www.bbc.com/news). Pages that have more variety in content may also work, but there would be more potential for bugs. Please submit an issue or contact me directly at dev.msimon@gmail.com if you encounter any problems.


### News Scraper API 

This service exposes an API that allows anyone to retrieve articles saved in the database, or scrape and retrieve articles from any site of their choosing. 

#### Retrieve Articles 

The endpoint to retrieve articles from the database is as follows: `https://www.news-scraper.com/api/v1/articles`

This endpoint expects a post request containing the following information in the body:
      - The earliest publication date of articles you would like to recieve (required; cannot be earlier than 01-01-2020).
      - The latest publication date of articles you would like to recieve (not required; defaults to current day).
      - Any keywords the must be contained in the articles' headlines (not required)
      - Amount of articles you would like to recieve (required; must be integer from 10-100).

A properly formatted request body should look like this:
      
   
      {
        "startDate": "06-05-2020",
        "endDate": "06-25-2020",
        "keywords": "covid,coronavirus",
        "amount": 20
      }  
      
#### Scrape Articles 

The endpoint to scrape articles using News Scraper's scraping engine is as follows: `https://www.news-scraper.com/api/v1/scrape-articles`

This endpoint expects a post request containing a url that you would like to scrape. A properly formatted request body should look like this:

     {
       "url": "https://www.slashdot.org"     
     }
     
     

      
      
 
 
      
