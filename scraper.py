from flask import request
import requests
from bs4 import BeautifulSoup
from logger import setup_logger
from exceptions import AppException
import csv

logger = setup_logger()

def get_search_page(search_string):
    url = "https://www.flipkart.com/search?q=" + search_string
    try:
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")
    except Exception as e:
        logger.error("Failed to retrieve search page: {}".format(str(e)))
        raise AppException("Failed to retrieve search page: {}".format(str(e)))

def get_product_reviews(product_page):
    product_html = BeautifulSoup(product_page.content, "html.parser")
    return product_html.find_all('div', {'class': "_16PBlm"})

def extract_review_info(commentbox):
    review = {}
    try:
        review['Name'] = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
    except:
        review['Name'] = None
    try:
        review['Rating'] = commentbox.div.div.div.div.text
    except:
        review['Rating'] = 'No Rating'
    try:
        review['CommentHead'] = commentbox.div.div.div.p.text
    except:
        review['CommentHead'] = 'No Comment Heading'
    try:
        comtag = commentbox.div.div.find_all('div', {'class': ''})
        review['Comment'] = comtag[0].div.text
    except:
        review['Comment'] = None
    return review

def scrape_flipkart(query):
    try:
        logger.info("Getting search page for query: " + query)
        flipkart_html = get_search_page(query)
        if flipkart_html is None:
            logger.error('Received None from get_search_page()')
            return None

        logger.info("Finding product boxes")
        bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
        del bigboxes[0:3]
        box = bigboxes[0]
        if box is None:
            logger.error('Unable to find product box')
            return None

        logger.info("Retrieving product page")
        product_link = box.div.div.div.a['href']
        if product_link is None:
            logger.error('Unable to find product link')
            return None
        productLink = "https://www.flipkart.com" + product_link
        prodRes = requests.get(productLink)

        logger.info("Getting product reviews")
        commentboxes = get_product_reviews(prodRes)
        if commentboxes is None:
            logger.error('Unable to find comment boxes')
            return None

        logger.info("Extracting review info")
        reviews = [extract_review_info(commentbox) for commentbox in commentboxes]

        logger.info(f'Successfully extracted {len(reviews)} reviews')
        with open('reviews.csv', 'w', newline='', encoding = 'utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=reviews[0].keys())
            writer.writeheader()
            for review in reviews:
                writer.writerow(review)

        logger.info(f'Successfully wrote {len(reviews)} reviews to CSV file')
        return reviews

    except Exception as e:
        logger.error(f"Error during scraping: {str(e)}")
        raise AppException(f"Failed to scrape Flipkart: {str(e)}")
