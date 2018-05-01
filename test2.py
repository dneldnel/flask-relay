import json
import requests
import threading
import time
import datetime
import commands

start_time=datetime.datetime.now()

def otherloop():
    print 'doing other stuff...'
    global start_time
    start_time = start_time + datetime.timedelta(seconds=36)
    timer=threading.Timer(36, calculate())
    timer.start()

def calculate():
    #dt=time.strftime("%Y-%m-%d %H:%M:%S")
    dt=time.strftime("%Y-%m-%d %H:%M:%S")

    elapse = (datetime.datetime.now()-start_time).seconds
    print 'starttime=',start_time.minute,start_time.second
    print 'elapsed seconds:',elapse

    global timer
    if(elapse>15):
        print 'cancel timer'
        timer.cancel()
        print 'doing some stuff for 36 secs'
        global start_time
        start_time=datetime.datetime.now()+ datetime.timedelta(seconds=36)

        timer=threading.Timer(36,calculate)
        timer.start()
    else:
        print 'loop again'
        timer=threading.Timer(3, calculate)
        timer.start()

if __name__== "__main__":
    calculate()