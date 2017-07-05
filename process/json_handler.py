# coding: utf-8

from os.path import normpath,join
from traffic_prediction.settings import BASE_DIR
import os,json

OPTION_ROOT_DIR=normpath(join(BASE_DIR,'static','option'))  ## normpath: 规范path字符串形式

def generate_option_template(title=True,tooltip=True,dataZoom=True,legend=True,toolbox=True,grid=True,xAxis=True,yAxis=True,series=True):
    option={}
    if title:
        option["title"]={}
    if tooltip:
        option["tooltip"]={}
    if dataZoom:
        option["dataZoom"]={}
    if legend:
        option["legend"]={}
    if toolbox:
        option["toolbox"]={}
    if grid:
        option["grid"]={}
    if xAxis:
        option["xAxis"]={}
    if yAxis:
        option["yAxis"]={}
    if series:
        option["series"]={}
    return option

def get_json_template_from(file_path):
    fp=open(file_path,"r")
    json_str = json.loads(json.dumps(fp.read()))
    json_obj = json.loads(json_str)
    fp.close()
    return json_obj

def generate_series_dict(legend_name, plot_type, **series_dict):
    ret_arr = []
    item = {}
    item["name"] = legend_name
    item["type"] = plot_type
    item["data"] = series_dict["car_num"]
    mark_point = {}
    mark_point["data"] = [{"type": "max", "name": "最大值"}]
    item["markPoint"] = mark_point
    ret_arr.append(item)

    return ret_arr


def put_data_into_json(option_arg,out_file_path,title="title",legend_names=[],xAxisData=[],seriesDictList=[]):
    option=option_arg
    option["title"]["text"]=title
    option["legend"]["data"]=legend_names
    if len(xAxisData):
        option["xAxis"][0]["data"]=xAxisData
    option["series"]=seriesDictList

    option_file=open(out_file_path,"w")
    print ("now writing option file")
    option_str=json.dumps(option, sort_keys=True, indent=4)
    option_file.write(option_str)
    option_file.close()
    print ("option file writed!")


def generate_option(json_file_name,plot_type,**points_info_dict):
    option_origin_path = OPTION_ROOT_DIR + os.sep + "option1_origin.json"
    option = get_json_template_from(option_origin_path)
    out_option_file_path = OPTION_ROOT_DIR + os.sep + json_file_name
    title_name = "区域车流量与时间的关系"
    datelist_data = points_info_dict["date_list"]
    legend_name = ["车辆数目"]
    seriesDictList = generate_series_dict(legend_name, plot_type, **points_info_dict)
    put_data_into_json(option, out_option_file_path, title=title_name, legend_names=legend_name,
                       xAxisData=datelist_data, seriesDictList=seriesDictList)