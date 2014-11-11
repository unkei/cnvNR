#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

gpsTimeList = []
gpsLatList = []
gpsLonList = []
subSection = None
rows = None

def parseNeoRun(stream):
# [[Training]]
# [TrainingResult]
#   TrainingName/Kind, StartDat/Time, ...
# [TrainingData]
#   LapCount, Calorie, PaceAve, ...
# [GraphData]
#   Log/HrInterval, GraphAltitude, GraphSpeed, ...
# [GPSData]
#   GpsTime, GpsLatitude, GpsLongitude, GpsAltitude, ...
# [LapData]
#   LapNo, EndPoint, LapTime, LapDistance, ...
# [TrainingSettingData]
#   UIVersion, FwVersion

    parseTraining(stream)
    exportGpx()

def parseTraining(stream):
    for row in stream:
        training = re.match(r'\[\[Training\]\]', row)
        if training is not None:
            parseSection(stream)

def parseSection(stream):
    global subSection
    global rows
    section = None
    for row in stream:
        section = re.match(r'\[.*\]', row)
        if section is not None:
            appendGpsData(subSection, rows)
            parseType = section.group(0)
            subSection = None
            rows = None
        elif parseType == '[TrainingResult]':
            parseTrainingResult(row)
        elif parseType == '[TrainingData]':
            parseTrainingData(row)
        elif parseType == '[GraphData]':
            parseGraphData(row)
        elif parseType == '[GPSData]':
            parseGPSData(row)
        elif parseType == '[LapData]':
            parseLapData(row)
        elif parseType == '[TrainingSettingData]':
            parseTrainingSettingData(row)


def parseTrainingResult(row):
    return

def parseTrainingData(row):
    return

def parseGraphData(row):
    return

def parseGPSData(row):
    global subSection
    global rows
    #print 'parseGPSData'
    cols = row.split(',')
    if len(cols) > 1:
        appendGpsData(subSection, rows)
        subSection = cols[0]
        rows = cols[1].strip()
    else:
        rows = rows + row.strip()

def appendGpsData(gpsDataType, rows):
    global gpsTimeList, gpsLatList, gpsLonList
    if rows is not None:
        if gpsDataType == 'GpsTime':
            gpsTimeList = rows.split(';')
        elif gpsDataType == 'GpsLatitude':
            for lat in rows.split(';'):
                gpsLatList.append(float(lat) / 1000000)
        elif gpsDataType == 'GpsLongitude':
            for lat in rows.split(';'):
                gpsLonList.append(float(lat) / 1000000)

def parseLapData(row):
    return

def parseTrainingSettingData(row):
    return

def exportGpx():
    printGpxHeader('workaout 5')
    #printGpxTrackPoint(35.664853, 139.527059, 54, '2014-11-08T01:20:23Z', 0, 0)
    for i, gpsTime in enumerate(gpsTimeList):
        printGpxTrackPoint(gpsLatList[i], gpsLonList[i], 54, gpsTime, 0, 0)
    printGpxFooter()

def printGpxHeader(name):
    print '<?xml version="1.0" encoding="UTF-8"?>'
    print '<gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd" version="1.1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1">'
    print ' <trk>'
    print '  <name>' + name + '</name>'
    print '  <desc />'
    print '  <trkseg>'

def printGpxTrackPoint(lat, lon, ele, time, hr, cad):
    print '   <trkpt lat="%.6f" lon="%.6f">' % (lat, lon)
    print '    <ele>%d</ele>' % ele
    print '    <time>%s</time>' % time
    print '    <extensions>'
    print '     <gpxtpx:TrackPointExtension>'
    print '      <gpxtpx:hr>%d</gpxtpx:hr>' % hr
    print '      <gpxtpx:cad>%d</gpxtpx:cad>' % cad
    print '     </gpxtpx:TrackPointExtension>'
    print '    </extensions>'
    print '   </trkpt>'

def printGpxFooter():
    print '  </trkseg>'
    print ' </trk>'
    print '</gpx>'


if __name__ == '__main__':
    neoRunReader = open('neorun.csv', 'rb')
    parseNeoRun(neoRunReader)

