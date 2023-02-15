#!/usr/bin/env python3

import feedparser
import re
import datetime
import os

url = feedparser.parse('/tmp/blog-02-11-2023.xml')

totals = {}
for item in url.entries:
    if re.search(r'^(Machelen|Berbroek)', item.title):
        # item.published is our endtime
        match = re.search(r'\d{4}-\d{2}-\d{2}', item.published)
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        content = item.content[0]['value']
        match = re.search(r'(\d+[.,]?\d*)\skm', content)
        distance = float(match.group(1))
        match = re.search(r'[,=]\s(\d+h)?(\d+m)(\d+)s?,', content)
        if match is not None:
            print(match.group(1),match.group(2),match.group(3))
        else:
            print("")
            print(date)
            print(content)
            match = re.search(r'7\.5\skm,\s0h4\?m\?\?,\s', content)
            if match is None:
                match = re.search(r',\s0h47m\?\?,', content)
                if match is None:
                    match = re.search(r',\s4\.5\sgelopen,\s4\.25\sgewandeld', content)
                    if match is None:
                        match = re.search(r'\sgeen\sprecieze\stijd', content)
                        if match is None:
                            match = re.search(r'10\.5\skm,\s57m09s\s\(', content)
                            if match is None:
                                match = re.search(r'10\.5\skm,\s58m15s\s\(', content)
                                if match is None:
                                    match = re.search(r'10\.5\skm,\s57m28s\s\(', content)
                                    if match is None:
                                        match = re.search(r'\s0h53m17s\.', content)
                                        if match is None:
                                            match = re.search(r'\s0h54m34s\.', content)
                                            if match is None:
                                                print("ERROR")
                                                exit(1)
        print(distance)
        filename = "run-%s.tcx" % (date)
        print(filename)
        if os.path.isfile(filename):
            print(filename,"exists already!")
            exit(1)
        f = open(filename, "w")
        f.close()

exit(1)

print(
            """
          <?xml version="1.0" encoding="UTF-8"?><TrainingCenterDatabase xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd" xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2">
            <Activities>
              <Activity Sport="running">
      <Id>2022-01-01T12:45:08.506000+02:00</Id>
      <Lap StartTime="2022-01-01T12:45:08.506000+02:00">
        <TotalTimeSeconds>4260</TotalTimeSeconds>
        <DistanceMeters>12200</DistanceMeters>
        <TriggerMethod>Manual</TriggerMethod>
        <Track>
          <Trackpoint>
            <Time>2022-01-01T12:45:08.506000+02:00</Time>
            <DistanceMeters>0</DistanceMeters>
          </Trackpoint>
          <Trackpoint>
            <Time>2022-01-01T13:56:08.506000+02:00</Time>
            <DistanceMeters>12200</DistanceMeters>
          </Trackpoint>
        </Track>
      </Lap>
    </Activity>
            </Activities>
          </TrainingCenterDatabase>
            """
            )

