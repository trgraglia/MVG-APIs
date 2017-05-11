#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import json
import cgi
import cgitb


def get_query(query):
  url = "https://www.mvg.de/fahrinfo/api/location/query?q=" + query
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

  print page


def get_station(station):
  url = "https://www.mvg.de/fahrinfo/api/departure/" + station
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

  print page


def main():
  print "Content-Type: application/json;charset=utf-8"
  print "Access-Control-Allow-Origin: *"
  print "Cache-Control: no-cache"
  print "Pragma: no-cache"
  print "Expires: -1"
  print

  arg_query = cgi.FieldStorage().getvalue("query", "").decode("utf-8").encode("windows-1252")
  arg_station = cgi.FieldStorage().getvalue("station", "").decode("utf-8").encode("windows-1252")
  
  if arg_query == "ALL":
    get_query("")
  elif arg_query != "":
    get_query(arg_query)
  elif arg_station != "":
    get_station(arg_station)  


# enable debugging
cgitb.enable(display=0, logdir="logs")
main()
