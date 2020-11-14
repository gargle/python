#!/usr/bin/env python3

import feedparser
import re
import datetime

url = feedparser.parse('/tmp/blog-11-14-2020.xml')

totals = {}
for item in url.entries:
    if re.search(r'^(Machelen|Berbroek)', item.title):
    #if item.title.startswith("Machelen"):
        match = re.search(r'\d{4}-\d{2}-\d{2}', item.published)
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        indexym = "%04d/%02d" % (date.year,date.month)
        index   = "%04d" % (date.year)
        content = item.content[0]['value']
        match = re.search(r'(\d+[.,]?\d*)\skm', content)
        distance = float(match.group(1))
        match = re.search(r',\s(\d+[.,]?\d*)\skm\/h\.', content)
        if match is not None:
            speed = float(match.group(1))
        else:
            speed = distance # we maken er een uur lopen van
        if indexym in totals:
            totals[indexym]['km'] = totals[indexym]['km'] + distance
            totals[indexym]['speed'] = totals[indexym]['speed'] + speed
            totals[indexym]['count'] = totals[indexym]['count'] + 1
        else:
            totals[indexym] = { 'km': distance, 'speed': speed, 'count': 1 }
        if index in totals:
            totals[index]['km'] = totals[index]['km'] + distance
            totals[index]['speed'] = totals[index]['speed'] + speed
            totals[index]['count'] = totals[index]['count'] + 1
        else:
            totals[index] = { 'km': distance, 'speed': speed, 'count': 1 }

print("year count distance  km/h.")
for year in sorted(totals):
    if "/" in  year:
        continue
    print("%-7s  %3d   %7.2f %6.2f" % (year,totals[year]['count'],
                                      totals[year]['km'],
                                      totals[year]['speed']/totals[year]['count']))
