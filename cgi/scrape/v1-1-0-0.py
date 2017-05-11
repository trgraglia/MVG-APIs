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

  request = urllib2.build_opener()
  request.addheaders = [("User-agent", "Mozilla/5.0")]
  response = request.open(url)
  page = response.read()

  return BeautifulSoup(page, "html.parser")


def get_minutes(lst, line, destination):
  for i, dic in enumerate(lst):
    if dic["line"] == line and dic["destination"] == destination:
      return i
  return -1


def get_stop(station):
  soup = get_soup(BASE_URL + urllib.quote_plus(station))
  json = {}

  o_station = soup.find("td", class_="headerStationColumn")

  if o_station is not None:
    json["station"] = o_station.get_text()
  else:
    json["error"] = "Station does not exist. Please use the autocomplete to get the correct station name."
    return json

  o_time = soup.find("td", class_="serverTimeColumn")

  if o_time is not None:
    json["time"] = o_time.get_text()

  json_vehicles = []
  json_groups = []

  a_vehicles = soup.select("table.departureView tr")

  for o_vehicle in a_vehicles:
    if o_vehicle.has_attr("class"):
      line = o_vehicle.find("td", class_="lineColumn").get_text()
      destination = o_vehicle.find("td", class_="stationColumn").get_text() \
        .replace(u'\xa0', u'').replace('\n', '').replace('\r', '').replace('\t', '').encode('utf8')
      minutes = o_vehicle.find("td", class_="inMinColumn").get_text()

      json_vehicles.append({
        "line": line,
        "destination": destination,
        "minutes": minutes
      })

      index = get_minutes(json_groups, line, destination)

      if index == -1:
        json_groups.append({
          "line": line,
          "destination": destination,
          "minutes": minutes
        })
      else:
        json_groups[index]["minutes"] = json_groups[index]["minutes"] + " " + minutes

  json["stops"] = json_vehicles
  json["groups"] = json_groups

  return json


def main():
  print "Content-Type: application/json;charset=utf-8"
  print "Access-Control-Allow-Origin: *"
  print

  arg_station = cgi.FieldStorage().getvalue("station").decode("utf-8").encode("windows-1252")

  print json.dumps(get_stop(arg_station))


# enable debugging
cgitb.enable(display=0, logdir="logs")
main()
