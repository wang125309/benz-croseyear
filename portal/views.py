# coding=utf8
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from django.conf import settings
import json
import requests
import logging
from plugin import *
import datetime
from django.core.cache import cache
from functools import wraps
import os
import sys
import re
import math
import redis
import thread  
reload(sys)
sys.setdefaultencoding('UTF-8')
lock = thread.allocate_lock()
# Create your views here.
logger = logging.getLogger(__name__)
r = redis.Redis(host="127.0.0.1",port=6379,db=4,password="cx89684518!@#$%")

def checkUploadOn(func):
    def _checkUploadOn(request):
        if r.get("uploadon"):
            return func(request)
        else :
            return JsonResponse({
                "status":"error",
                "reason":"upload not start"
            })
    return _checkUploadOn

def checkTicketsOn(func):
    def _checkTicketsOn(request):
        if r.get("ticketson"):
            return func(request)
        else :
            return JsonResponse({
                "status":"error",
                "reason":"ticket not start"
            })
    return _checkTicketsOn

def needBackLogin(func):
    def _needBackLogin(request):
        if request.sesion.get("backuser"):
            return func(request)
        else:
            return JsonResponse({
                "status":"error",
                "reason":"need login"
            })
    return _needBacklogin
def needLogin(func):
    def _needLogin(request):
        if request.session.get("userid"):
            return func(request)
        else:
            return JsonResponse({
                "status":"error",
                "reason":"need login"
            })
    return _needLogin

def login(request):
    userid = request.GET.get("userid")
    user = User.objects.filter(userid=userid)
    if user:
        request.session['userid'] = userid
        request.session['id'] = user[0].id
        return JsonResponse({
            "status":"success",
        })
    else :
        newuser = User(userid=userid,like1=0,like2=0,src="",tickets1=6,tickets2=6)
        newuser.save()
        request.session['userid'] = userid
        request.session['id'] = newuser.id
        return JsonResponse({
            "status":"success"
        })

@needLogin
def info(request):
    u = User.objects.get(id=request.session.get('id'))
    return JsonResponse({
        "status":"success",
        "data":{
            "id":u.id,
            "userid":u.userid,
            "tickets1":u.tickets1,
            "tickets2":u.tickets2
        }
    })

@needLogin
@checkUploadOn
def uploadFile(request):
    userid = request.session["userid"]
    u = User.objects.get(userid=userid)
    f = request.FILES.get('file')
    path = "data/"
    if not os.path.exists(path):
        os.mkdirs(path)
    ext = str(f).split(".")[-1]
    ext = ext.lower()
    path = 'data/' + str(u.id) + "." + ext
    des = open(path,'wb+')
    for j in f.chunks():
        des.write(j)
    des.close()
    u.src = path
    u.save()
    return JsonResponse({
        "status":"success"    
    })

@needLogin
@checkTicketsOn
def like1(request):
    uid = request.GET.get("uid")
    userid = request.session.get("id")
    u = User.objects.get(id=userid)
    toUser = User.objects.get(id=uid)
    lock.acquire()
    like = Like.objects.filter(userid=request.session['id'],toUserid=uid,type=1)
    if len(like) == 0 and u.tickets1 > 0:
        l = Like(userid=request.session['id'],toUserid=uid,type=1)
        l.save()
        toUser.like1 += 1
        u.tickets1 -= 1
        u.save()
        toUser.save()
        lock.release()
        return JsonResponse({
            "status":"success",
        })
    elif len(like) > 0:
        lock.release()
        return JsonResponse({
            "status":"error",
            "reason":"already send ticket"
        })
    elif u.tickets1 == 0:
        lock.release()
        return JsonResponse({
            "status":"error",
            "reason":"no tickets left"
        })
    else :
        lock.release()
        return JsonResponse({
            "status":"error",
            "reason":"unknown error"
        })

@needLogin
@checkTicketsOn
def like2(request):
    uid = request.GET.get("uid")
    userid = request.session.get("id")
    u = User.objects.get(id=userid)
    toUser = User.objects.get(id=uid)
    lock.acquire()
    like = Like.objects.filter(userid=request.session['id'],toUserid=uid,type=2)
    if len(like) == 0 and u.tickets2 > 0:
        l = Like(userid=request.session['id'],toUserid=uid,type=2)
        l.save()
        toUser.like2 += 1
        u.tickets2 -= 1
        u.save()
        toUser.save()
        lock.release()
        return JsonResponse({
            "status":"success",
        })
    elif len(like) > 0:
        lock.release()
        return JsonResponse({
            "status":"error",
            "reason":"already send ticket"
        })
    elif u.tickets1 == 0:
        lock.release()
        return JsonResponse({
            "status":"error",
            "reason":"no tickets left"
        })
    else :
        lock.release()
        return JsonResponse({
            "status":"error",
            "reason":"unknown error"
        })

def alreadyLogin(request):
    if request.session.get("id"):
        u = User.objects.filter(id=request.session['id'])
        if len(u) > 0:
            return JsonResponse({
                "status":"success"    
            })
        else :
            return JsonResponse({
                "status":"error"
            })
    else : 
        return JsonResponse({
            "status":"error"
        })
def rank1(request):
    u = User.objects.all().order_by("-like1")
    data = []
    total = 0
    map(lambda i:data.append({"id":i.id,"tickets1":i.tickets1,"tickets2":i.tickets2,"src":i.src,"userid":i.userid,"like1":i.like1,"like2":i.like2}),u)
    return JsonResponse({
        "status":"success",
        "data":data,
        "total":total
    })

def rank2(request):
    u = User.objects.all().order_by("-like2")
    total = 0
    data = []
    
    map(lambda i:data.append({"id":i.id,"tickets1":i.tickets1,"tickets2":i.tickets2,"src":i.src,"userid":i.userid,"like1":i.like1,"like2":i.like2}),u)
    return JsonResponse({
        "status":"success",
        "data":data,
        "total":total
    })

def backendLogin(request):
    if request.GET.get("uname") == 'admin' and request.GET.get("upwd") == 'benzAdmin':
        request.session['backuser'] = True
        return JsonResponse({
            "status":"success"    
        })
    else : 
        return JsonResponse({
            "status":"error",
            "reason":"user or password wrong"
        })



def startUpload(request):
    r.set("uploadon","1")
    return JsonResponse({
        "status":"success"
    })

def endUpload(request):
    r.delete("uploadon")
    return JsonResponse({
        "status":"success"
    })

def startTickets1(request):
    r.set("ticketson","1")
    Like.objects.all().delete()
    u = User.objects.all()
    for i in u:
        i.tickets1 = 1
        i.tickets2 = 0
        i.save()
    return JsonResponse({
        "status":"success"
    })

def startTickets2(request):
    r.set("ticketson","1")
    Like.objects.all().delete()
    u = User.objects.all()
    for i in u:
        i.tickets1 = 0
        i.tickets2 = 1
        i.save()
    return JsonResponse({
        "status":"success"
    })

def startTickets(request):
    r.set("ticketson","1")
    return JsonResponse({
        "status":"success"
    })

def endTickets(request):
    r.delete("ticketson")
    return JsonResponse({
        "status":"success"
    })
