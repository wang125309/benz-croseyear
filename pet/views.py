# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from django.conf import settings
import json
import requests
import logging
from models import *
import datetime
from django.core.cache import cache
from functools import wraps
import sys
import os
import re
import math
import time
import xlwt
import datetime
reload(sys)
sys.setdefaultencoding('UTF-8')

def export(request):
    taskid = request.GET.get("id")
    u = User.objects.all().order_by("-like")
    fname = "data/data.xls"
    file = xlwt.Workbook()
    table = file.add_sheet('active',cell_overwrite_ok=True)
    table.write(0,0,'id')
    table.write(0,1,u'姓名')
    table.write(0,2,u'头像地址')
    table.write(0,3,u'参加理由')
    table.write(0,4,u'手机号')
    table.write(0,5,u'排名')
    table.write(0,6,u'喜欢')
    line = 1
    for i in u:
        table.write(line,0,i.id)
        table.write(line,1,i.name)
        table.write(line,2,i.avatar)
        table.write(line,3,i.desc)
        table.write(line,4,i.mobile)
        table.write(line,5,line)
        table.write(line,6,i.like)
        line += 1
    file.save(fname)
    return HttpResponseRedirect('/data/data.xls')

def getUserInformation(request):
    uid = request.GET.get("uid")
    date = request.GET.get("date")
    if uid:
        u = User.objects.get(id=uid)
        us = User.objects.all().order_by("-like")
        cnt = 0
        rank = 0
        for i in us:
            cnt += 1
            if i.id == uid:
                rank = cnt
                break
    if date:
        u = User.objects.get(dateline=date)
        us = User.objects.all().order_by("-like")
        cnt = 0
        rank = 0
        for i in us:
            cnt += 1
            if i.dateline == date:
                rank = cnt
                break
    return JsonResponse({
        "status" : "success",
        "desc" : u.desc,
        "avatar" : u.avatar,
        "like" : u.like,
        "rank" : rank,
        "date" : u.dateline
    })


def like(request):
    if request.GET.get("uid"):
        u = User.objects.get(id=request.GET.get("uid"))
    else :
        u = User.objects.get(dateline=request.GET.get("date"))
    u.like += 1
    u.save()

    return JsonResponse({
        "status": "success",
        "like" : u.like
    })
    
def submit(request):
    name = request.POST.get("name")
    mobile = request.POST.get("mobile")
    desc = request.POST.get("desc")
    f = request.FILES.get('file')
    date = request.POST.get("date")
    path = "data/"
    if not os.path.exists(path):
        os.mkdirs(path)
    ext = str(f).split(".")[-1]
    ext = ext.lower()
    path = 'data/' + str(time.time()) + "." + ext
    des = open(path,'wb+')
    for j in f.chunks():
        des.write(j)
    des.close()
    dateline = time.time()
    u = User.objects.filter(mobile=mobile).count()
    if not u:
        user = User(name=name,mobile=mobile,desc=desc,like=0,avatar=path,dateline=date)
        user.save()
        return JsonResponse({
            "status":"success"    
        })
    else :
        return JsonResponse({
            "status":"fail",
            "reason":"您已经参加过了哦"
        })
