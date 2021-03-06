from app import app, config
from flask import render_template, redirect, url_for, session, request, jsonify
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
    freqwords_per_subtitle = {subtitle: website_scraper.find_most_frequent_words(subtitle)[:5] for subtitle in subtitles}
    hyperlinks_per_subtitle = {subtitle: website_scraper.get_hyperlinks(subtitle) for subtitle in subtitles}

    return render_template('scraped.html',
                            scraped_title=scraped_title,
                            subtitles=subtitles,
                            freqwords_per_subtitle=freqwords_per_subtitle,
                            hyperlinks_per_subtitle=hyperlinks_per_subtitle)

@app.route('/<wiki>')
def quick_scraped(wiki):
    global website_scraper
    website_scraper = Scraper(wiki)
    return redirect('/info')


# API Routes

@app.route('/api/v1/wiki', methods=['GET'])
def api_phrase():
    if 'phrase' in request.args:
        phrase = request.args['phrase']
    else:
        return jsonify({'error' : "Wikipedia phrase not found"})

    api_scraper = Scraper(phrase)
    results = {
        'title': api_scraper.get_main_title(),
        'subtitles': api_scraper.get_titles(),
        'freq_words': {subtitle: api_scraper.find_most_frequent_words(subtitle) for subtitle in api_scraper.get_titles()},
        'hyperlinks': {subtitle: api_scraper.get_hyperlinks(subtitle) for subtitle in api_scraper.get_titles()}
    }

    return jsonify(results)


# 404 Handler

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404