#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import urllib2
import json
import cgi
import cgitb
import urllib

BASE_URL = "http://www.mvg-live.de/ims/dfiStaticAuswahl.svc?haltestelle="


def get_soup(url):
  """
  :type url: basestring
  :param url:
  :rtype: bs4.BeautifulSoup
  """
  opener = urllib2.build_opener()
  opener.addheaders = [("User-agent", "Mozilla/5.0")]
  response = opener.open(url)
  page = response.read()
  o_soup = BeautifulSoup(page, "html.parser")
  return o_soup


def get_stop(station):
  soup = get_soup(BASE_URL + urllib.quote_plus(station))
  data = {}

  o_server_station = soup.find("td", class_="headerStationColumn")
  o_server_time = soup.find("td", class_="serverTimeColumn")

  server_station = ""
  server_time = ""

  if o_server_station is not None:
    server_station = o_server_station.get_text()

  if o_server_time is not None:
    server_time = o_server_time.get_text()

  server_stops = []

  rows = soup.select("table.departureView tr")

  for row in rows:
    if row.has_attr("class"):
      stop = {
        "line": row.find("td", class_="lineColumn").get_text(),
        "destination": row.find("td", class_="stationColumn").get_text()
          .replace(u'\xa0', u'').replace('\n', '').replace('\r', '').replace('\t', '').encode('utf8'),
        "minutes": row.find("td", class_="inMinColumn").get_text()
      }
      server_stops.append(stop)

  data["stops"] = server_stops
  data["station"] = server_station
  data["time"] = server_time
  return data


def main():
  print "Content-Type: application/json;charset=utf-8"
  print "Access-Control-Allow-Origin: *"
  print

  form = cgi.FieldStorage()
  station = form.getvalue("station", default="Petuelring")
  station = station.decode("utf-8").encode("windows-1252")

  data = get_stop(station)
  print json.dumps(data)


# enable debugging
cgitb.enable(display=0, logdir="logs")
main()
