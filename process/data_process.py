# coding=utf-8
import csv,os
import datetime,pickle
from process.models import *
from process.helpers import pinyin_hash,check_point
from traffic_prediction.settings import  BASE_DIR

file_dir = os.path.join(BASE_DIR, "../20130304/").replace("\\","/")
file_path = os.path.join(file_dir, "filelist.txt")

tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8)) # 创建时区UTC+8:00,防止构造datetime类时出现warning(强迫症添加)

SOURCE_NAME = "13301104001.csv"
DESTINATION_NAME = "destination.csv"


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

##用来判断文件是文本文件还是二进制文件
## 文本文件为True,二进制文件为False
def isText(s):
    text_characters = "".join(map(chr, range(32, 127))).join("\n\r\t\b")
    _null_trans = str.maketrans("", "",text_characters)
    if "\0" in s:
        return False
    if not s:
        return True
    t = s.translate(_null_trans)
    if float(len(t)) / float(len(s)) > 0.30:
        return False
    return True

def dbSingleFile(roadset, source_name, car_id):
    route_id = -1
    time_index = 0
    lon_index = 1
    lat_index = 2
    file_reader = open(source_name)
    try:
        file_str = file_reader.read(512)  ##通过read()函数获取文件中全部字符串，512表示读取字节的数目
    except:
        #print("hahaha")
        return
    if(isText(file_str)):
        #print("text file")
        fileOpenType = "r"
        para_dict = {"mode":fileOpenType, "newline":""}
    else:
        #print("binary file")
        fileOpenType = "rb"
        para_dict = {"mode":fileOpenType}
        return
    file_reader.close()
    ## Try to think why I pass a dict parameter
    with open(source_name, **para_dict) as src:
        reader = csv.reader(src)
        for row in reader:
            if str(row[0]) == "-1":
                route_id += 1
            else:
                hour = int(row[time_index])//3600
                minute = (int(row[time_index])%3600)//60
                second = int(row[time_index])%60
                date_time = datetime.datetime(year=2017,month=4,day=1,hour=hour,minute=minute ,second=second) ##不加tzinfo会warning,但不是错误

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
    path_pkl_file.close()
    num = 0
    try:
        csv_list = data_file.readlines()  #read()函数读取一个完整的str，readlines函数按行读取，返回值为list
        # print(type(csv_list))  list
        for car_id, csv_name in enumerate(csv_list):
            csv_path = os.path.join(file_dir, csv_name.strip())   ##刚刚报错了，原因是路径末尾出现了\n符号，读取的csv_name末尾含有\n，需要调用strip函数去掉\n
            print(csv_path)
            num += 1
            if(num > 500):
                break
            dbSingleFile(roadset, csv_path, car_id)

    finally:
        data_file.close()
    return


'''
if __name__ =="__main__":
    #solveSingleFile()
    path_pkl_file = "../data/boundary.pkl"
    process(path_pkl_file)
'''



