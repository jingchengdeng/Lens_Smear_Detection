import csv
# import numpy as np
import math
from geopy.distance import vincenty

def read(file):
    f = open(file)
    data = csv.reader(f)
    return data

def get_latitude(fileName):
    data = read(fileName)
    latitudes = []
    for row in data:
        latitude = row[3]
        latitudes.append(float(latitude))
    return latitudes

def getShapepoint(data, index):
    result = []
    for i in range(len(data)):
        rawData = data[i][-3].split('|')[index].split('/')
        result.append([float(rawData[0]), float(rawData[1])])
    return result

def getXY(data):
    result = []
    for i in range(len(data)):
        row = []
        row.append(float(data[i][3]))
        row.append(float(data[i][4]))
        result.append(row)
    return result

def matchPoint(probe, link, probePoints, linkData):
    id = []
    point = []
    for i in range(len(probe)):
        if i > 0 and probePoints[i][0] == probePoints[i-1][0]:
            id.append(id[-1])
            point.append(point[-1])
            continue
        d = []
        for j in range(len(link)):
            d.append(vincenty((probe[i][0], probe[i][1]), (link[j][0], link[j][1])).meters)
        point.append(d.index(min(d)))
        id.append(int(linkData[point[-1]][0]))
    return id, point

def getDistance(beginPoint, endPoint):
    point = []
    for i in range(len(beginPoint)):
        d = []
        for j in range(len(endPoint)):
            d.append(vincenty((beginPoint[i][0],beginPoint[i][1]), (endPoint[j][0], endPoint[j][1])).meters)
        point.append(d.index(min(d)))
    return point

def getDFR(probe, refNode, index):
    slope = []
    for i in range(len(probe)):
        p2 = refNode[index[i]]
        slope.append(vincenty((probe[i][0], probe[i][1]), (p2[0], p2[1])).meters)
    return slope

def getPerDis(p1, p2):
    pass

def getSlope(p1, probePoints):
    slope = []
    for i in range(len(p1)-1):
        slope.append((int(probePoints[i+1][-3])-int(probePoints[i][-3]))/vincenty((p1[i][0], p1[i][1]), (p1[i+1][0], p1[i+1][1])).meters)
    return slope

if __name__ == "__main__":
    probePoints = [line.split(',') for line in open('./Partition6467ProbePoints.csv')]
    linkData = [line.split(',') for line in open('./Partition6467LinkData.csv')]
    probeXY = getXY(probePoints)
    refNode = getShapepoint(linkData, 0)
    shapePoint = getShapepoint(linkData, -1)
    match, index = matchPoint(probeXY[0:1000], refNode, probePoints, linkData)
    dFR = getDFR(probeXY[0:1000], refNode, index)
    dir = []
    for i in range(len(dFR)-1):
        if dFR[i+1] > dFR[i]:
            dir.append('T')
        else:
            dir.append('F')
    dir.append(dir[-1])
    dFL = []
    for i in range(1000):
        h = linkData[i][-3].split('|')[0].split('/')[-1]
        if h == '':
            dFL.append(0)
        else:
            dFL.append(math.sqrt(dFR[i]**2+float(h)**2))

    slope = getSlope(probeXY[0:1000], probePoints)

    csvFile = file('Partition6467MatchedPoints.csv','wb')
    writer = csv.writer(csvFile)
    writer.writerow(['sampleID', 'dataTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading', 'linkPVID', 'direction', 'distFromRef', 'distFromLink'])
    data = probePoints
    for i in range(1000):
        data[i][-1] = data[i][-1][0:-2]
        data[i].append(str(match[i]))
        data[i].append(dir[i])
        data[i].append(str(dFR[i]))
        data[i].append(str(dFL[i]))
        writer.writerow(data[i])
    csvFile.close()




