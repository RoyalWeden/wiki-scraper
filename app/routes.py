from app import app, config
from flask import render_template, redirect, url_for, session, request
from app.scraper import Scraper

website_scraper: Scraper = None

@app.route('/', methods=['GET','POST'])
def home():
    global website_scraper
    if request.method == 'POST':
        website_scraper = Scraper(request.form['search'])
        return redirect('/scraped-info')
    return render_template('home.html')

@app.route('/scraped-info')
def scraped():
    return """
    <h1>Main Title:</h1> <p>{}</p>
    <h1>Sub Titles:</h1> <p>{}</p>
    <h1>Frequent Words in 'History' Sub Title:</h1> <p>{}</p>
    """.format(website_scraper.get_main_title(), website_scraper.get_titles(), website_scraper.find_most_frequent_words('History'))