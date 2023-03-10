#!/usr/bin/env python3

import feedparser
import re
from datetime import datetime, timedelta
import os

url = feedparser.parse("./blog-03-10-2023.xml")

inputFile = "Machelen_7.5_Km_Higher_Precision.tcx"
inputFile = "Boetfort.tcx"

outputFile = "2014-05.tcx"

f = open(outputFile, "w")
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
        if published.date().month != 5:
            continue
        if published.date().day != 5:
            continue
        print(published.date())
        content = item.content[0]["value"]
        match = re.search(r"(\d+[.,]?\d*)\skm", content)
        distance = float(match.group(1)) * 1000
        if distance == 7500:
            inputFile = "Machelen_7.5_Km_Higher_Precision.tcx"
        elif distance == 10500:
            inputFile = "Boetfort.tcx"
        else:
            print("ERROR in distance:", distance)
            exit(1)
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
        search for the time the distance is larger than our target
        """
        r = open(inputFile, "r")
        timeStamp = 0
        totalTimeSeconds = 0
        for line in r:
            line = line.strip()
            match = re.search(r"^<Time>(\d\d\d\d\-\d\d\-\d\d)T(\d\d):(\d\d):(\d\d)Z</Time>$", line)
            if match is not None:
                timeStamp = (
                    int(match.group(2)) * 3600
                    + int(match.group(3)) * 60
                    + int(match.group(4))
                )
            match = re.search(r"^<DistanceMeters>(\d+(\.\d+)?)</DistanceMeters>$", line)
            if match is not None and timeStamp > 0:
                distanceMeters = float(match.group(1))
                if distanceMeters > distance and totalTimeSeconds == 0:
                    totalDistanceMeters = distanceMeters
                    totalTimeSeconds = timeStamp
        r.close
        r = open(inputFile, "r")
        distanceMeters = 0
        upToTrack = 0
        dataBlock = ""
        lastBlock = 0
        for line in r:
            line = line.strip()
            if lastBlock == 1:
                continue
            if upToTrack == 0:
                match = re.search(r"^<Track>$", line)
                if match is not None:
                    upToTrack = 1
                    continue
            match = re.search(r"^<Trackpoint>$", line)
            if match is not None:
                dataBlock = "<Trackpoint>\n"
                continue
            match = re.search(r"^</Trackpoint>$", line)
            if match is not None:
                dataBlock = dataBlock + "</Trackpoint>" + "\n"
                if distanceMeters < distance:
                    f.write(dataBlock)
                else:
                    if lastBlock == 0:
                        print(dataBlock)
                        #dataBlock = re.sub(str(distanceMeters),str(distance),dataBlock)
                        print(startTime)
                        print(runningTime)
                        endTime = "<Time>%s</Time>\n" % str(
                            (
                                startTime
                                + timedelta(days=0, hours=0, minutes=0, seconds=runningTime)
                            ).isoformat()
                        )
                        print(endTime)
                        #dataBlock = re.sub(str(totalTimeSeconds),str(runningTime),dataBlock)
                        print(dataBlock)
                        f.write(dataBlock)
                    lastBlock = 1
                continue
            match = re.search(r"^</Track>$", line)
            if match is not None:
                upToTrack = 2
                continue
            if upToTrack > 1:
                continue
            match = re.search(r"^<DistanceMeters>(\d+(\.\d+)?)</DistanceMeters>$", line)
            if match is not None:
                distanceMeters = float(match.group(1))
                dataBlock = dataBlock + line + "\n"
                continue
            match = re.search(r"^<Time>(\d\d\d\d\-\d\d\-\d\d)T(\d\d):(\d\d):(\d\d)Z</Time>$", line)
            if match is not None:
                timeStamp = (
                    int(match.group(2)) * 3600
                    + int(match.group(3)) * 60
                    + int(match.group(4))
                )
                timeStamp = timeStamp / totalTimeSeconds * runningTime
                dataBlock = dataBlock + "<Time>%s</Time>\n" % str(
                    (
                        startTime
                        + timedelta(days=0, hours=0, minutes=0, seconds=timeStamp)
                    ).isoformat()
                )
            else:
                if line[0:6] == "<Time>":
                    print("ERROR: ", line)
                    exit(1)
                dataBlock = dataBlock + line + "\n"
        r.close()

        f.write("</Track>" + "\n")
        f.write("</Lap>" + "\n")
        f.write("</Activity>" + "\n")

f.write("</Activities>" + "\n")
f.write("</TrainingCenterDatabase>" + "\n")
f.close()

exit(1)
