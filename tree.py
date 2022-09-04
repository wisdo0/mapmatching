import shapefile

import csv

from rtree import index

dirname = 'F:/carpool_item/Beijing/xydata/AllData.csv'

rtreename = 'F:/carpool_item/Beijing/xydata/Rtree'

fileNames = {'城市快速路': 'F:/carpool_item/Beijing/城市快速路_polyline.shp',\
    '高速': 'F:/carpool_item/Beijing/高速_polyline.shp',\
    '国道': 'F:/carpool_item/Beijing/国道_polyline.shp',\
    '九级路': 'F:/carpool_item/Beijing/九级路_polyline.shp',\

    '省道': 'F:/carpool_item/Beijing/省道_polyline.shp',\

    '县道': 'F:/carpool_item/Beijing/县道_polyline.shp',\

    '乡镇村道': 'F:/carpool_item/Beijing/乡镇村道_polyline.shp'}

#处理每种路网

#write csvfile name

csvFile = open(dirname,'w',newline = '')

writer = csv.writer(csvFile)

name = ['id','roadkind','roadname','bbox','points','other']

writer.writerow(name)

#build Rtree

fileIdx = index.Rtree(rtreename)

id = 0

for key,value in fileNames.items():

#read shapefile
    sf = shapefile.Reader(value)

    shapeRecords = sf.shapeRecords()

#continue write csvfile and bulid rtree

    for shapeRecord in shapeRecords:

        temp = [str(id),str(key),shapeRecord.record[1],str(shapeRecord.shape.bbox),str(shapeRecord.shape.points)]

        fileIdx.insert(id,shapeRecord.shape.bbox)

        id += 1

        writer.writerow(temp)

csvFile.close()



from rtree import index

import csv

import pickle

backName = 'F:/carpool_item/Beijing/xydata/'

rtreename = 'F:/carpool_item/Beijing/xydata/Rtree'

pickleName =  'F:/carpool_item/Beijing/xydata/AllData_pickle.txt'

fileIdx = index.Rtree(rtreename)

while 1:

    # autitude = float(input('please input autitude: '))

    # longitude = float(input('please input longitude: '))

    autitude = 116.3974750042

    longitude = 39.9087239839

    if autitude == 0:

        print('exit...')

        break

    xmin = autitude - 0.004

    xmax = autitude + 0.004

    ymin = longitude - 0.004

    ymax = longitude + 0.004

    IdxData = list(fileIdx.intersection((xmin,ymin,xmax,ymax)))

    print(len(IdxData))

    print(IdxData)

#write csvFile

    csvName = backName + str(autitude) + '_' + str(longitude) + '.csv'

    csvFileW = open(csvName,'w',newline = '')

    writer = csv.writer(csvFileW)

    writer.writerow(['adress','autitude','longitude','phone'])

    file = open(pickleName,'rb')

    reader = pickle.load(file)

    file.close()

    for id in IdxData:

        adress = reader[id + 1][2]

        points = list(eval(str(reader[id + 1][4])))

        for point in points:

            autitude = point[0]

            longitude = point[1]

            temp = [adress,str(autitude),str(longitude),str(id)]

            writer.writerow(temp)

    csvFileW.close()

    break
