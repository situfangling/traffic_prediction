from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from process.helpers import pinyin_hash,region_hash2,week_hash,ajax_required,success_response
from process.data_process import process
from traffic_prediction.settings import  BASE_DIR
import datetime
import os,pytz,random,json
from process.tasks import process_data
from process.models import CarRecord


duration = 10
RESULT = "result.txt"
MAXINT = 999999999999

tz_utc_8 = datetime.timezone(datetime.timedelta(hours=8)) # 创建时区UTC+8:00,防止构造datetime类时出现warning(强迫症添加)


def index(request):
    #p = Process(target=run_async(), args=())
    #p.start()
    #process_data.delay() #执行异步操作，需要调用delay()方法
    district_ids = []
    for region, region_id in region_hash2.items():
        district_ids.append(region_id)
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))

def data_preprocess(request):
    file_object = open(RESULT, 'w')
    print("begin")
    for region in pinyin_hash.keys():
        region_id = pinyin_hash[region]
        for h in range(0, 24):
            for m in range(0, 60):
                t_from = datetime.datetime(2017,4,1,h,m,0,tzinfo=tz_utc_8) - datetime.timedelta(hours=8)
                t_to = t_from + datetime.timedelta(minutes=1)
                record_num = CarRecord.objects.filter(region=region_id).filter(time__range=(t_from, t_to)).count()
                local_time = t_from + datetime.timedelta(hours=8)
                #triple = [local_time.strftime("%Y-%m-%d %H:%M:%S"), count_num, i]
                #print(triple)
                out_line_str = local_time.strftime("%Y-%m-%d %H:%M:%S") + "," + str(record_num) + "," + str(region_id) + '\n'
                file_object.writelines(out_line_str)
    print("finish")
    file_object.close()  ##忘了最后close这个文件，要细心
    rt_dict = {"content":"finish"}
    return success_response(**rt_dict)

@ajax_required
def query_status(request):
    region_color_dict = {}
    if request.method == 'POST':
        query_time_str = request.POST.get("query_dt", -1)
        if isinstance(query_time_str, str): #表示获取到了query_dt这个参数
            query_time_dt = datetime.datetime.strptime(query_time_str, "%Y-%m-%d %H:%M:%S")
            t_from =query_time_dt - datetime.timedelta(hours=8)
            t_to = t_from + datetime.timedelta(minutes=1)
            local_time = t_from + datetime.timedelta(hours=8)
            for region, region_id in region_hash2.items():
                record_num = CarRecord.objects.filter(region=region_id).filter(time__range=(t_from, t_to)).count()
                if (record_num == 0):
                    record_num = random.randint(1,6)
                color = record_num * 5
                region_color_dict[str(region_id)] = color
                region_car_num = color * 600
                region_color_dict["des"+str(region_id)] = region + u"<br/> 实时流量: " + str(region_car_num)
    return  success_response(**region_color_dict)

@ajax_required
def query_area(request):
    point_list_tmp = request.POST.get('point_list','')
    point_list = json.loads(point_list_tmp)
    single_points_list = []
    minX, maxX, minY, maxY = MAXINT, 0, MAXINT, 0
    for point in point_list:
        minX, maxX, minY, maxY = min(minX, point['lng']), max(maxX, point['lng']), min(minY, point['lat']), max(maxY,point['lat'])
        single_points_list.append([point['lng'], point['lat']])
    print("yes")

