#!/usr/bin/env python3

import feedparser
import re
from datetime import datetime, timedelta
import os

url = feedparser.parse("./blog-02-15-2023.xml")

f = open("all.tcx", "w")
f.write(
            '<?xml version="1.0" encoding="UTF-8"?><TrainingCenterDatabase xsi:schemaLocation="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2 http://www.garmin.com/xmlschemas/TrainingCenterDatabasev2.xsd" xmlns="http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:ns3="http://www.garmin.com/xmlschemas/ActivityExtension/v2">'
)
f.write("\n")
f.write("<Activities>" + "\n")

for item in url.entries:
    if re.search(r"^(Machelen|Berbroek)", item.title):
        # item.published is our endtime
        published = datetime.fromisoformat(item.published)
        match = re.search(r"\d{4}-\d{2}-\d{2}", item.published)
        if published.date().year < 2019 or published.date().year > 2019:
            continue
        #if published.date().month < 2:
        #    continue
        print(published.date())
        content = item.content[0]["value"]
        match = re.search(r"(\d+[.,]?\d*)\skm", content)
        distance = float(match.group(1)) * 1000
        match = re.search(r",\s(\d+)h(\d+)m(\d+)s,", content)
        if match is not None:
            runningTime = (
                int(match.group(1)) * 3600
                + int(match.group(2)) * 60
                + int(match.group(3))
            )
        else:
            match = re.search(r",\s(\d+)m(\d+)s,", content)
            if match is not None:
                runningTime = int(match.group(1)) * 60 + int(match.group(2))
            else:
                print("ERROR")
                print(item.published)
                print(content)
                exit(1)
        endTime = published - timedelta(days=0, hours=0, minutes=30)
        startTime = endTime - timedelta(hours=0, minutes=0, seconds=runningTime)
        f.write('<Activity Sport="running">' + "\n")
        f.write("<Id>" + str(startTime.isoformat()) + "</Id>" + "\n")
        f.write('<Lap StartTime="' + str(startTime.isoformat()) + '">' + "\n")
        f.write("<TotalTimeSeconds>" + str(runningTime) + "</TotalTimeSeconds>" + "\n")
        f.write("<DistanceMeters>" + str(distance) + "</DistanceMeters>" + "\n")
        f.write("<TriggerMethod>Manual</TriggerMethod>" + "\n")
        f.write("<Track>" + "\n")
        f.write("<Trackpoint>" + "\n")
        f.write("<Time>" + str(startTime.isoformat()) + "</Time>" + "\n")
        f.write("<DistanceMeters>0</DistanceMeters>" + "\n")
        f.write("</Trackpoint>" + "\n")
        f.write("<Trackpoint>" + "\n")
        f.write("<Time>" + str(endTime.isoformat()) + "</Time>" + "\n")
        f.write("<DistanceMeters>" + str(distance) + "</DistanceMeters>" + "\n")
        f.write("</Trackpoint>" + "\n")
        f.write("</Track>" + "\n")
        f.write("</Lap>" + "\n")
        f.write("</Activity>" + "\n")

f.write("</Activities>" + "\n")
f.write("</TrainingCenterDatabase>" + "\n")
f.close()

exit(1)
