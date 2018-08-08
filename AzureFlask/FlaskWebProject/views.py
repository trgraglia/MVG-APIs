"""
Routes and views for the flask application.
"""

from flask import render_template
from FlaskWebProject import app
from flask import Flask
from flask import Response
import urllib2


@app.route('/')
def index():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='MVG API',
        message='Endpoints:<ul><li>/_api/query/query_str</li><li>/_api/station/station_id</li></ul>',
    )


@app.route('/_api/query/<query_str>', methods=['GET'])
def get_query(query_str):
    url = "https://www.mvg.de/fahrinfo/api/location/queryWeb?q=" + query_str
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    request = urllib2.build_opener()
    request.addheaders = [
        ('User-agent', user_agent),
        ('Accept', 'application/json, text/javascript, */*; q=0.01'),
        ('X-MVG-Authorization-Key', '5af1beca494712ed38d313714d4caff6'),
        ('Content-Type', 'application/json; charset=UTF-8')
    ]
    response = request.open(url)
    page = response.read()

    resp = Response(page)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json;charset=utf-8'
    resp.headers['Cache-Control'] = 'no-cache'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '-1'
    return resp


@app.route('/_api/station/<station_id>', methods=['GET'])
def get_station(station_id):
    url = "https://www.mvg.de/fahrinfo/api/departure/" + station_id + "?footway=0"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    request = urllib2.build_opener()
    request.addheaders = [
        ('User-agent', user_agent),
        ('Accept', 'application/json, text/javascript, */*; q=0.01'),
        ('X-MVG-Authorization-Key', '5af1beca494712ed38d313714d4caff6'),
        ('Content-Type', 'application/json; charset=UTF-8')
    ]
    response = request.open(url)
    page = response.read()

    resp = Response(page)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json;charset=utf-8'
    resp.headers['Cache-Control'] = 'no-cache'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '-1'
    return resp
