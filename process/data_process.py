# coding=utf-8
import csv
import datetime,pickle
from process.models import *
from process.helpers import pinyin_hash,check_point

SOURCE_NAME = "13301104001.csv"
DESTINATION_NAME = "destination.csv"
file_dir = "../../20130304/"
file_path = file_dir + "filelist.txt"


def solveSingleFile():
    row_list = []
    route_id = -1
    with open(SOURCE_NAME, 'r',newline='') as src:
        reader = csv.reader(src)
        for row in reader:
            if str(row[0]) == "-1":
                route_id += 1
            else:
                myRow = [route_id,row[0],row[1],row[2]]
                row_list.append(myRow)


    with open(DESTINATION_NAME, 'w',newline='') as des:
        writer = csv.writer(des)
        for row in row_list:
            print(str(row))
            writer.writerow(row)
    return

def dbSingleFile(roadset, source_name, car_id):
    route_id = -1
    time_index = 0
    lon_index = 1
    lat_index = 2
    with open(source_name, 'r', newline='') as src:
        reader = csv.reader(src)
        for row in reader:
            if str(row[0]) == "-1":
                route_id += 1
            else:
                hour = int(row[time_index])//3600
                minute = (int(row[time_index])%3600)//60
                second = int(row[time_index])%60
                date_time = datetime.datetime(year=2017,month=4,day=1,hour=hour,minute=minute ,second=second)
                lon = float(row[lon_index])
                lat = float(row[lat_index])
                for j in range(len(roadset)):
                    # print("roadset="+roadset[j]["name"]+", minX="+str(roadset[j]['minX'])+",maxX=" +str(roadset[j]['maxX'])+",minY="+str(roadset[j]['minY'])+',maxY='+str(roadset[j]['maxY']))
                    if roadset[j]["name"] in pinyin_hash.keys():
                        if (not (roadset[j]['minX'] <= lon and lon <= roadset[j]['maxX'] and roadset[j][
                            'minY'] <= lat and lat <= roadset[j]['maxY'])):
                            continue
                        # print("YES")
                        data_set = roadset[j]["data"]
                        flag = check_point(data_set, lon, lat)
                        if flag:
                            region = pinyin_hash[roadset[j]["name"]]
                            carRecord = CarRecord(car_id=car_id, route_id=route_id, time=date_time, longitude=lon, latitude=lat, region=region)
                            carRecord.save()
                            break
                ## transform seconds to datetime type


def process(path_pkl_path):
    data_file = open(file_path)
    path_pkl_file = open(path_pkl_path, "rb")
    roadset = pickle.load(path_pkl_file)
    try:
        csv_list = data_file.read()
        for car_id, csv_name in enumerate(csv_list):
            csv_path = file_dir + csv_name
            dbSingleFile(roadset, csv_path, car_id)

    finally:
        data_file.close()
    return



if __name__ =="__main__":
    #solveSingleFile()
    path_pkl_file = "../data/boundary.pkl"
    process(path_pkl_file)


