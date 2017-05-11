#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import urllib2
import json
import cgi
import cgitb
import urllib
import string

BASE_URL = "http://www.mvg-live.de/ims/dfiStaticAuswahl.svc?haltestelle="
LETTERS = list(string.ascii_lowercase)


def get_soup(url):
  """
  :type url: basestring
  :param url:
  :rtype: bs4.BeautifulSoup
  """

  request = urllib2.build_opener()
  request.addheaders = [("User-agent", "Mozilla/5.0")]
  response = request.open(url)
  page = response.read()

  return BeautifulSoup(page, "html.parser")


def get_stations(letter):
  soup = get_soup(BASE_URL + urllib.quote_plus(letter))

  a_stations = soup.select("table.departureTable ul a")
  s_stations = ""

  for o_station in a_stations:
    s_stations = s_stations + o_station.get_text().replace(u'\xa0', u'').encode('utf8') + "\n"

  return s_stations


def main():
  f = open("stations.txt", "w")

  for letter in LETTERS:
    f.write(get_stations(letter))
    f.write('\n')

  f.close()  # enable debugging


cgitb.enable(display=0, logdir="logs")
main()
