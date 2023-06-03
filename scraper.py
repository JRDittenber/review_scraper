import requests
from bs4 import BeautifulSoup

def get_search_page(search_string):
    url = "https://www.flipkart.com/search?q=" + search_string
    response = requests.get(url)
    return BeautifulSoup(response.content, "html.parser")

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
    # Get the search page
    flipkart_html = get_search_page(query)
    
    # Find the product boxes
    bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
    box = bigboxes[0]

    # Get the product link and retrieve the product page
    productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
    prodRes = requests.get(productLink)

    # Get the reviews from the product page
    commentboxes = get_product_reviews(prodRes)

    # Extract the review information
    reviews = [extract_review_info(commentbox) for commentbox in commentboxes]

    return reviews
