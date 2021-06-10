from app import app, config
from flask import render_template, redirect, url_for, session, request
from app.scraper import Scraper

website_scraper: Scraper = None

@app.route('/', methods=['GET','POST'])
def home():
    global website_scraper
    if request.method == 'POST':
        website_scraper = Scraper(request.form['search'])
        return redirect('/info')
    return render_template('home.html')

@app.route('/info')
def scraped():
    if website_scraper == None:
        return redirect('/')
    scraped_title = website_scraper.get_main_title() + " | Wiki Scraper"
    subtitles = website_scraper.get_titles()
    freqwords_per_subtitle = {subtitle: website_scraper.find_most_frequent_words(subtitle) for subtitle in subtitles}
    return render_template('scraped.html',
                            scraped_title=scraped_title,
                            subtitles=subtitles,
                            freqwords_per_subtitle=freqwords_per_subtitle)