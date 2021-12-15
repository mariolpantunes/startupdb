import json
import logging
import requests

from bs4 import BeautifulSoup
from flask import Flask, request, jsonify


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


app = Flask(__name__)


@app.route('/search', methods=['GET'])
def startup_search():
    q = request.args.get('q')
    URL = f'https://www.eu-startups.com/directory/?wpbdp_view=search&kw={q}'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('div', {'class': 'wpbdp-listing'})
    startups = []
    for r in results:
        # title
        div_title = r.find('div', {'class': 'listing-title'})
        title = div_title.find('a').getText()
        link = div_title.find('a')['href']
        
        # details
        div_details = r.find('div', {'class': 'listing-details'})
        details_results = r.find_all('div', {'class': 'value'})
        country =  details_results[0].find('a').getText()
        based_in = details_results[1].getText()
        tags = [x.strip() for x in details_results[2].getText().split(',')]
        year = int(details_results[3].getText())

        # logo
        logo = r.find('img', {'class': 'wpbdp-thumbnail'})['src']

        startup = {'title':title, 'link':link, 'country':country, 'based_in':based_in, 'tags':tags, 'year':year, 'logo':logo}

        logger.info(f'{startup}\n')
        startups.append(startup)
    return jsonify({'startups':startups})


if __name__ == '__main__':
   app.run()
