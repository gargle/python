#!/usr/bin/env python3

import feedparser
import re
from datetime import datetime, timedelta
import os

url = feedparser.parse("./blog-02-24-2023.xml")

f = open("2014-12.tcx", "w")
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
        if published.date().year != 2014:
            continue
        if published.date().month != 12:
            continue
        content = item.content[0]["value"]
        match = re.search(r"https?:\/\/www\.plotaroute\.com\/route\/(\d+)", content)
        #print(published.date(), match.group(1))
        match = re.search(r"(\d+[.,]?\d*)\skm", content)
        distance = float(match.group(1)) * 1000
        match = re.search(r",\s(\d+)h(\d+)m(\d+)s?,", content)
        if match is not None:
            runningTime = (
                int(match.group(1)) * 3600
                + int(match.group(2)) * 60
                + int(match.group(3))
            )
        else:
            match = re.search(r",\s(\d+)m(\d+)s?,", content)
            if match is not None:
                runningTime = int(match.group(1)) * 60 + int(match.group(2))
            else:
                runningTime = 60
        endTime = published - timedelta(days=0, hours=0, minutes=30)
        startTime = endTime - timedelta(hours=0, minutes=0, seconds=runningTime)
        f.write('<Activity Sport="running">' + "\n")
        f.write("<Id>" + str(startTime.isoformat()) + "</Id>" + "\n")
        f.write('<Lap StartTime="' + str(startTime.isoformat()) + '">' + "\n")
        f.write("<TotalTimeSeconds>" + str(runningTime) + "</TotalTimeSeconds>" + "\n")
        f.write("<DistanceMeters>" + str(distance) + "</DistanceMeters>" + "\n")
        f.write("<TriggerMethod>Manual</TriggerMethod>" + "\n")
        f.write("<Track>" + "\n")
        """
        f.write("<Trackpoint>" + "\n")
        f.write("<Time>" + str(startTime.isoformat()) + "</Time>" + "\n")
        f.write("<DistanceMeters>0</DistanceMeters>" + "\n")
        f.write("</Trackpoint>" + "\n")
        f.write("<Trackpoint>" + "\n")
        f.write("<Time>" + str(endTime.isoformat()) + "</Time>" + "\n")
        f.write("<DistanceMeters>" + str(distance) + "</DistanceMeters>" + "\n")
        f.write("</Trackpoint>" + "\n")
        """
        r = open("Machelen_7.5_Km.tcx", "r")
        totalTimeSeconds = 0
        fetch = 0
        for line in r:
            line = line.strip()
            if fetch == 0:
                if totalTimeSeconds == 0:
                    match = re.search(r"^<TotalTimeSeconds>(\d+\.\d+)</TotalTimeSeconds>$", line)
                    if match is None:
                        continue
                    else:
                        totalTimeSeconds = float(match.group(1))
                match = re.search(r"^<Trackpoint>$", line)
                if match is not None:
                    f.write("<Trackpoint>" + "\n")
                    fetch = 1
                    continue
                else:
                    continue
            match = re.search(r"^</Track>$", line)
            if match is not None:
                fetch = 2
                continue
            if fetch == 2:
                continue
            match = re.search(r"^<Time>2023-03-08T(\d\d):(\d\d):(\d\d)Z</Time>$", line)
            if match is not None:
                timeStamp = (
                    int(match.group(1)) * 3600
                    + int(match.group(2)) * 60
                    + int(match.group(3))
                )
                if (timeStamp > runningTime):
                    print("WARN, timestamp (%d) > runningTime (%d)" % (timeStamp, runningTime))
                    #timeStamp = runningTime
                timeStamp = timeStamp / totalTimeSeconds * runningTime
                f.write(
                    "<Time>%s</Time>"
                    % str(
                        (
                            startTime
                            + timedelta(days=0, hours=0, minutes=0, seconds=timeStamp)
                        ).isoformat()
                    )
                )
            else:
                if line[0:6] == "<Time>":
                    print("ERROR: ", line)
                    exit(1)
                f.write(line)
        r.close()
        
        f.write("</Track>" + "\n")
        f.write("</Lap>" + "\n")
        f.write("</Activity>" + "\n")

f.write("</Activities>" + "\n")
f.write("</TrainingCenterDatabase>" + "\n")
f.close()

exit(1)
