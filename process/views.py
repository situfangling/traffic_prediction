from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from process.helpers import pinyin_hash,week_hash,ajax_required,success_response
from process.data_process import process
from traffic_prediction.settings import  BASE_DIR
import datetime
import os
from process.tasks import process_data

duration = 10


def index(request):
    #p = Process(target=run_async(), args=())
    #p.start()
    process_data.delay()
    return render_to_response('index.html', locals(), context_instance=RequestContext(request))