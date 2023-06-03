from flask import Flask, render_template, request
import csv
from logger import setup_logger
from scraper import scrape_flipkart
from exceptions import AppException

app = Flask(__name__)
logger = setup_logger()

@app.route("/")
def front_end():
    return render_template("search.html")

@app.route('/search_results', methods=['POST'])
def search_results():
    try:
        query = request.form['query']
        logger.info(f"Received query: {query}")
        reviews = scrape_flipkart(query)

        if reviews is None:
            logger.error(f"No reviews found for query: {query}")
            return render_template('error.html', error_message="No reviews found.")

        # Read the CSV data
        with open('reviews.csv', 'r') as f:
            reader = csv.DictReader(f)
            reviews = list(reader)

        return render_template('results.html', reviews=reviews)
    except AppException as e:
        logger.error(f"Error: {str(e)}")
        return render_template('error.html', error_message=str(e))

if __name__=="__main__":
    app.run(host="0.0.0.0") 
