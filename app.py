from flask import Flask, render_template, request
from scraper import scrape_flipkart

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        try:
            query = request.form['content'].replace(" ", "")
            reviews = scrape_flipkart(query)
            return render_template('results.html', reviews=reviews)
        except Exception as e:
            print(e)
            return 'Something went wrong'
    else:
        return render_template('search.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")
