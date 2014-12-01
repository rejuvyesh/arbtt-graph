#!/usr/bin/env python3
#
# File: readArbttStats.py
#
# Created: Monday, December  1 2014 by rejuvyesh <mail@rejuvyesh.com>
# License: GNU GPL 3 <http://www.gnu.org/copyleft/gpl.html>
#

import argparse
import csv
import json
import sys

def toJson(dic, jsonpath):
  """
  
  Arguments:
  - `dic`:
  - `jsonpath`:
  """
  with open(jsonpath, 'w') as f:
    json.dump(dic, f, sort_keys=True)


def toChartJS(daildic, mindic, color, name):
  """
  Arguments:
  - `dic`: Dictionary
  - `color`: Color of each label
  - `jsonpath`: Path of json file
  """
  export = []

  for day in daildic:
    jsonname = name + '-' + day + '.json'
    d = daildic[day]
    try:
      mind = mindic[day]
    except KeyError:
      mind = {}
    data = []
    totaltime = 0
    for index, item in enumerate(d):
      time = list(item.values())[0]['Time']  # hh:mm:ss
      hour, minute, sec = [int(x) for x in time.split(':')]
      mins = hour*60 + minute
      totaltime += mins
      per = float(list(item.values())[0]['Percent'])
      label = list(item.keys())[0]
      data.append({'label': label + ' (' + '{:.2f}'.format(per) + '%)', "value": per, "color": color[label]})

    # Save json for the day
    export.append({'fname': jsonname, 'totalTime': "%d:%02d:00" % (totaltime//60, totaltime%60)})
    toJson(sorted(export, key=lambda x: x['fname']), 'render/loglist.json')
    toJson({'piedata': sorted(data, key=lambda x: x['label']), 'tagdata': mind}, 'render/data/'+jsonname)

def dailyUsage(dailyfile, minutefile, unmatched):
  """
  
  Arguments:
  - `dailyfile`:
  - `minutefile`:
  - `category`:
  """
  tags = set()
  daily = {}

  with open(dailyfile, 'r') as f:
    dailystats = csv.reader(f, delimiter=',')
    next(dailystats)  # Skip headers
    # row = {Day, Tag, Time, Percentage}
    for row in dailystats:
      if 'omitted' in row[1]:
        continue
      elif 'unmatched' in row[1]:
        tag = unmatched
      else:
        tag = row[1].split(':')[1]
      tags.update({tag})
      if row[0] in daily.keys():
        daily[row[0]].append({tag: {'Time': row[2], 'Percent': row[3]}})
      else:
        daily[row[0]] = [{tag:  {'Time': row[2], 'Percent': row[3]}}]

  colors = {}
  d3colors = [
    "#1f77b4", "#aec7e8",
    "#ff7f0e", "#ffbb78",
    "#2ca02c", "#98df8a",
    "#d62728", "#ff9896",
    "#9467bd", "#c5b0d5",
    "#8c564b", "#c49c94",
    "#e377c2", "#f7b6d2",
    "#7f7f7f", "#c7c7c7",
    "#bcbd22", "#dbdb8d",
    "#17becf", "#9edae5"
  ]
  # Assign color to each tag
  for i, t in enumerate(sorted(tags)):
    colors[t] = d3colors[i % len(d3colors)]

  # Load minute data
  minutestats = {}
  with open(minutefile, 'r') as f:
    next(f)
    content = f.readlines()
    for row in content:
      day, value = row.split(' ', 1)
      time, inctag, _, _ = value.split(',')
      if 'unmatched' in inctag:
        tag = unmatched
      else:
        tag = inctag.split(':')[1]
      hour, minute = [int(x) for x in time.split(':')]
      moment = hour*60 + minute
      if day in minutestats.keys():
        if tag in minutestats[day].keys():
          minutestats[day][tag]['minute'].append(moment)
        else:
          minutestats[day][tag] = {'minute': [moment], 'color': colors[tag]}
      else:
        minutestats[day] = {tag: {'minute': [moment], 'color': colors[tag]}}

  toChartJS(daily, minutestats, colors, 'daily')


def main():
  parser = argparse.ArgumentParser(prog='readArbttStats', description='read arbtt stats nad convert them to jsons', add_help=True)
  parser.add_argument('-c', '--category_name', default='misc', help='arbtt unmatched category name')
  parser.add_argument('-d', '--daily_csv', help='CSV of daily data')
  parser.add_argument('-m', '--minute_csv', help='CSV of minute by minute data.')
  
  args = parser.parse_args()

  categoryName = args.category_name
  dailyCsv = args.daily_csv
  minuteCsv = args.minute_csv

  dailyUsage(dailyCsv, minuteCsv, categoryName)

if __name__ == '__main__':
  main()
