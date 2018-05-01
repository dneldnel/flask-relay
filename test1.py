
import json
import requests
import threading
import time
import commands
import MySQLdb
import datetime

##################################################
#URL for getting statistics
url='http://whattomine.com/coins.json'
#starting algo
mining='lbry'
#starting time
start_time=datetime.datetime.now()
#seconds for mining fee
mining_fee_secs=360
#seconds for checkup interval
checkup_secs=30
#seconds for loop interval
interval=30

###################################################

#Find the biggest among 3 number
def biggest(a,b,c):
    if a>b:
        maxnum=a
    else:
        maxnum=b

    if c>maxnum:
        maxnum=c
    return maxnum

#Get MySQL connection
def getConn():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='d0ntpu5h',db='stratumproxy',port=3306)
    return conn

def addToHistroyDB(v):
    
    try:
        conn=getConn()
        cur=conn.cursor()
        cur.execute("insert into switch_history values(NULL,%s,%s,%s)",v)
        conn.commit()
        cur.close()
        conn.close()

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
        conn.close()

def addToCompareDB(lbc,dcr,sia,pasc):
    dt=time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="insert into profit_compare values(NULL,'%s','%s','%s','%s','%s','%s','%s')" \
        % (str(lbc),str(dcr),str(sia),str(pasc),'0','0',dt)
        cur.execute(sql)
        print "Insert DB successful"
        
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
        conn.close() 

def calculate():
    try:

        content=requests.get(url,timeout=100).content

        hjson = json.loads(content)

        lbry_wtm_hash=315
        lbry_btcrev= hjson['coins']['LBRY']['btc_revenue'] 
        lbry_btc_g=float(lbry_btcrev) / lbry_wtm_hash *1000
        lbry_profit= float(lbry_btcrev) / lbry_wtm_hash *40000

        dcr_wtm_hash=5910
        dcr_btcrev= hjson['coins']['Decred']['btc_revenue'] 
        dcr_btc_g=float(dcr_btcrev) / dcr_wtm_hash *1000
        dcr_profit= float(dcr_btcrev) / dcr_wtm_hash * 160000

        sia_wtm_hash=3450
        sia_btcrev= hjson['coins']['Sia']['btc_revenue'] 
        sia_btc_g=float(sia_btcrev) / sia_wtm_hash * 1000
        sia_profit= float(sia_btcrev) / sia_wtm_hash * 80000

        pasc_wtm_hash=2100
        pasc_btcrev= hjson['coins']['Pascalcoin']['btc_revenue'] 
        pasc_btc_g=float(pasc_btcrev) / pasc_wtm_hash * 1000
        pasc_profit= float(pasc_btcrev) / pasc_wtm_hash * 40000

        addToCompareDB(lbry_btc_g,dcr_btc_g,sia_btc_g,pasc_btc_g)

        dict={lbry_profit:'lbry',sia_profit:'sia',dcr_profit:'dcr'}

        print ''
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        print "Current lbry daily BTC income=", lbry_profit
        print "Current dcr daily BTC income=",dcr_profit
        print "Current sia daily BTC income=", sia_profit
        print "Current pasc daily BTC income=", pasc_profit

        #print "Max=", biggest(lbry_profit,dcr_profit,sia_profit)

        w=[lbry_profit,dcr_profit,sia_profit]

        a1=max(w)
        w.remove(a1)
        a2=max(w)

        #Ratio of 1st/2nd
        c=a1/a2
        print "1st:2nd=",c
        if(c>1.05):
            d=dict.get(a1)
            print "Ratio >1.05, 1st is:",d
            global mining
            if(d is mining):
                print 'No need to change'
            else:
                mining=d
                cfg=mining+'.cfg'
                cmd='cp /etc/haproxy/'+cfg+' /etc/haproxy/haproxy.cfg && service haproxy restart'
                print "Change algo using ",cfg
                (status, output)=commands.getstatusoutput(cmd)
                print output
                dt=time.strftime("%Y-%m-%d %H:%M:%S")
                value=[mining,mining,dt]
                addToHistroyDB(value)
        global start_time
        global timer

        elapse = (datetime.datetime.now()-start_time).seconds
        print 'Client mining for ',elapse
        if(elapse > 3240):
            print 'Client mined over 3240 sec, going to mine for us 360 sec'
            #timer.cancel()
            cmd='cp /etc/haproxy/' + mining +'-fee.cfg /etc/haproxy/haproxy.cfg && service haproxy restart'
            print "Change to mining fee using fee.cfg"
            (status, output)=commands.getstatusoutput(cmd)
            print output
            start_time=datetime.datetime.now()+ datetime.timedelta(seconds=mining_fee_secs)

            dt=time.strftime("%Y-%m-%d %H:%M:%S")
            value=['fee',mining,dt]
            addToHistroyDB(value)

            interval=mining_fee_secs
           # timer=threading.Timer(mining_fee_secs,calculate)
           # timer.start() #if time passed for 3240 sec, mine for us 360 sec
        elif elapse<5:
            cfg=mining+'.cfg'
            cmd='cp /etc/haproxy/'+cfg+' /etc/haproxy/haproxy.cfg && service haproxy restart'
            print "back from fee to client mode"
            print "Change algo using ",cfg
            (status, output)=commands.getstatusoutput(cmd)
            print output

            dt=time.strftime("%Y-%m-%d %H:%M:%S")
            value=[mining,mining,dt]
            addToHistroyDB(value)

            interval=checkup_secs
            #timer=threading.Timer(30, calculate)
            #timer.start()
        else:
            interval=checkup_secs
            #timer=threading.Timer(30, calculate)
            #timer.start()
    except:
        print 'Error happened!'
        interval=checkup_secs
        #timer=threading.Timer(30, calculate)
        #timer.start()
    finally:
        print 'sleep for '+str(interval)
        timer=threading.Timer(interval, calculate)
        timer.start()


if __name__== "__main__":
    calculate()



