#!/usr/bin/python

import feedparser
import re
import datetime

url = feedparser.parse('/tmp/blog-12-20-2018.xml')

totals = {}
for item in url.entries:
    if item.title.encode('utf-8').startswith('Machelen'):
        match = re.search(r'\d{4}-\d{2}-\d{2}', item.published.encode('utf-8'))
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        indexym = "%04d/%02d" % (date.year,date.month)
        index   = "%04d" % (date.year)
        content = item.content[0]['value'].encode('utf-8')
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

for year in sorted(totals):
    if "/" in  year:
        continue
    print("%-7s %3d %7.2f %7.2f" % (year,totals[year]['count'],
                                    totals[year]['km'],
                                    totals[year]['speed']/totals[year]['count']))
