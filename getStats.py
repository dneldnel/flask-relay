import json
import requests
import threading
import time
import MySQLdb
import datetime

#to is the timeout setting
to=100

dcr_balance_url='https://www2.coinmine.pl/dcr/index.php?page=api&action=getanonbalance&wallet_address='
dcr_dashboard_url='https://www2.coinmine.pl/dcr/index.php?page=api&action=getanondashboarddata&wallet_address='
dcr_workers_url='https://www2.coinmine.pl/dcr/index.php?page=api&action=getanonworkers&wallet_address='
dcr_transaction_url='https://www2.coinmine.pl/dcr/index.php?page=api&action=getanontransactions&wallet_address='

lbc_balance_url='https://www2.coinmine.pl/lbc/index.php?page=api&action=getanonbalance&wallet_address='
lbc_dashboard_url='https://www2.coinmine.pl/lbc/index.php?page=api&action=getanondashboarddata&wallet_address='
lbc_workers_url='https://www2.coinmine.pl/lbc/index.php?page=api&action=getanonworkers&wallet_address='
lbc_transaction_url='https://www2.coinmine.pl/lbc/index.php?page=api&action=getanontransactions&wallet_address='

wallat='Dsm8WpVGNSQNx4ZkJHvbBZjH9P5itQj59cC'
url_test=dcr_balance_url+ ""

def getDcrBalance(url):
    content=requests.get(url,timeout=to).content
    hjson = json.loads(content)

    foo=hjson['getanonbalance']['data']
    return foo


#get db conn
def getConn():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='d0ntpu5h',db='stratumproxy',port=3306)
    return conn



#get all address from user_address table
def getAllAddress():
    conn=getConn()
    cur=conn.cursor()
    sql="select * from user_address"
    data=[]
    try:
        cur.execute(sql)
        results=cur.fetchall()
       
        for row in results:
            r={}
            r['address']=row[0]
            r['algo']=row[1]
            r['coin']=row[2]
            data.append(r)

    except MySQLdb.Error,e:

        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
       
    conn.close()
    return data

def getDCRBalanceCoinMine(address):
    r={}
    url=dcr_balance_url+address
    content=requests.get(url,timeout=to).content
    hj = json.loads(content)
    r['address']=address
    r['confirmed']=hj['getanonbalance']['data']['confirmed']
    r['unconfirmed']=hj['getanonbalance']['data']['unconfirmed']
    return r

def getLBCBalanceCoinMine(address):
    r={}
    url=lbc_balance_url+address
    content=requests.get(url,timeout=to).content
    hj = json.loads(content)
    r['address']=address
    r['confirmed']=hj['getanonbalance']['data']['confirmed']
    r['unconfirmed']=hj['getanonbalance']['data']['unconfirmed']
    return r


def getDCRDashBoardCoinMine(address):
    r={}
    url=dcr_dashboard_url+address
    content=requests.get(url,timeout=to).content
    hj = json.loads(content)
    r['address']=address
    r['hashrate']=hj['getanondashboarddata']['data']['personal']['hashrate']
    r['avghashrate']=hj['getanondashboarddata']['data']['personal']['avghashrate']
    r['price']=hj['getanondashboarddata']['data']['pool']['price']
    r['coin']=hj['getanondashboarddata']['data']['pool']['info']['currency']
    r['invalid']=hj['getanondashboarddata']['data']['pool']['shares']['invalid_percent']
    r['hashrate_net']=hj['getanondashboarddata']['data']['network']['hashrate']
    r['block']=hj['getanondashboarddata']['data']['network']['block']
    r['difficulty']=hj['getanondashboarddata']['data']['network']['difficulty']
    r['nextdifficulty']=hj['getanondashboarddata']['data']['network']['nextdifficulty']

    return r

def getLBCDashBoardCoinMine(address):
    r={}
    url=lbc_dashboard_url+address
    content=requests.get(url,timeout=to).content
    hj = json.loads(content)
    r['address']=address
    r['hashrate']=hj['getanondashboarddata']['data']['personal']['hashrate']
    r['avghashrate']=hj['getanondashboarddata']['data']['personal']['avghashrate']
    r['price']=hj['getanondashboarddata']['data']['pool']['price']
    r['coin']=hj['getanondashboarddata']['data']['pool']['info']['currency']
    r['invalid']=hj['getanondashboarddata']['data']['pool']['shares']['invalid_percent']
    r['hashrate_net']=hj['getanondashboarddata']['data']['network']['hashrate']
    r['block']=hj['getanondashboarddata']['data']['network']['block']
    r['difficulty']=hj['getanondashboarddata']['data']['network']['difficulty']
    r['nextdifficulty']=hj['getanondashboarddata']['data']['network']['nextdifficulty']

    return r


def getDCRTransactionCoinMine(address):
    
    url=dcr_transaction_url+address
    content=requests.get(url,timeout=to).content
    hj=json.loads(content)
    return hj['getanontransactions']['data']

def getLBCTransactionCoinMine(address):
    
    url=lbc_transaction_url+address
    content=requests.get(url,timeout=to).content
    hj=json.loads(content)
    return hj['getanontransactions']['data']

def getDCRWorkerCoinMine(address):
    url=dcr_workers_url+address
    content=requests.get(url,timeout=to).content
    hj=json.loads(content)
    return hj['getanonworkers']['data']

def getLBCWorkerCoinMine(address):
    url=lbc_workers_url+address
    content=requests.get(url,timeout=to).content
    hj=json.loads(content)
    return hj['getanonworkers']['data']


#data is the array contains all address info
def fetchAllBalanceData(data):
    ret=[]
    for row in data:
        if(row['coin']=='dcr'):
            #returned address,confirmed,unconfirmed
            r=getDCRBalanceCoinMine(row['address'])
            ret.append(r)
        if(row['coin']=='lbc'):
            #returned address,confirmed,unconfirmed
            r=getLBCBalanceCoinMine(row['address'])
            ret.append(r)
    return ret

#data is the array contains all address info
def fetchAllDashboardData(data):
    ret=[]
    for row in data:
        if(row['coin']=='dcr'):
            #returned address,confirmed,unconfirmed
            r=getDCRDashBoardCoinMine(row['address'])
            ret.append(r)
        if(row['coin']=='lbc'):
            #returned address,confirmed,unconfirmed
            r=getLBCDashBoardCoinMine(row['address'])
            ret.append(r)
    return ret

#data is the array contains all address info
def fetchAllTransactionData(data):
    ret=[]
    for row in data:
        if(row['coin']=='dcr'):
            #returned address,confirmed,unconfirmed
            r=getDCRTransactionCoinMine(row['address'])
            ret.append(r)
        if(row['coin']=='lbc'):
            #returned address,confirmed,unconfirmed
            r=getLBCTransactionCoinMine(row['address'])
            ret.append(r)
    return ret    

#data is the array contains all address info
def fetchAllWorkersData(data):
    ret=[]
    for row in data:
        if(row['coin']=='dcr'):
            #returned address,confirmed,unconfirmed
            r=getDCRWorkerCoinMine(row['address'])
            ret.append(r)
        if(row['coin']=='lbc'):
            #returned address,confirmed,unconfirmed
            r=getLBCWorkerCoinMine(row['address'])
            ret.append(r)
    return ret    

#data is the array contains all address info
def deleteWorkersData(data):
    conn=getConn()
    cur=conn.cursor()
    for row in data:
        sql="delete from worker_info where account ='%s'" % row['address']
        cur.execute(sql)
    conn.commit()
    conn.close() 




#address,confirmed, unconfirmed
def saveBalance(ret):
    
    conn=getConn()
    cur=conn.cursor()
    dt=time.strftime("%Y-%m-%d %H:%M:%S")

    for row in ret:
        print row['address']+':'+row['confirmed']+'/'+row['unconfirmed']
        sql1="select count(*) from user_status where address='%s'" % row['address']
        cur.execute(sql1)
        results=cur.fetchone()
        

        if(results[0] == 0):#new address
            print 'inserting...'
            sql2="insert into user_status values(NULL,'%s','%s','%s','%s')" % (row['address'],row['confirmed'],row['unconfirmed'],dt)
            cur.execute(sql2)
        else:
            print 'updating...'
            sql3= "update user_status set confirmed='%s' , unconfirmed='%s' , dt='%s' where address='%s' " %  (row['confirmed'],row['unconfirmed'],dt, row['address'])
            cur.execute(sql3)
    conn.commit()
    print 'done'
    conn.close()

def saveDashboardData(ret):
    
    conn=getConn()
    cur=conn.cursor()
    dt=time.strftime("%Y-%m-%d %H:%M:%S")

    for row in ret:
        print 'handling '+ row['address'] #+':'+row['hashrate']+'/'+row['avghashrate']+'/'+row['price']
        sql1="select count(*) from dashboard_data where address='%s'" % row['address']
        cur.execute(sql1)
        results=cur.fetchone()

        if(results[0] == 0):#new address
            print 'inserting...'
            sql2="insert into dashboard_data values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"  \
            % (row['address'],row['price'],row['hashrate'],row['avghashrate'],row['coin'],row['invalid'],row['hashrate_net'],row['block'],row['difficulty'],row['nextdifficulty'],dt) 
            cur.execute(sql2)
        else:
            print 'updating...'
            sql3= "update dashboard_data set price='%s' , hashrate='%s' , avghashrate='%s', coin='%s', invalid='%s',hashrate_net='%s', block='%s', difficulty='%s',nextdifficulty='%s', dt='%s' where address='%s' " \
            %  (row['price'],row['hashrate'],row['avghashrate'],row['coin'],row['invalid'],row['hashrate_net'],row['block'],row['difficulty'],row['nextdifficulty'],dt, row['address'])
            cur.execute(sql3)
    conn.commit()
    print 'done'        
    conn.close()

def saveTransactionData(ret):    
    conn=getConn()
    cur=conn.cursor()

    for r in ret:
        
        for row in r:
            sql1="select count(*) from transaction_data where id='%s'" % row['id']
            cur.execute(sql1)
            results=cur.fetchone()

            if(results[0]==0):#db didn't have a transaction data with the same id
                print 'unsaved transaction found! Inserting....'

                d=datetime.datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S")
                h=d+datetime.timedelta(hours=7)
                
                sql2="insert into transaction_data values('%s','%s','%s','%s','%s')" % (row['id'],row['coin_address'],round(float(row['amount']),5),row['txid'],h.strftime('%Y-%m-%d %H:%M:%S'))
                #print sql2
                cur.execute(sql2)
            
    conn.commit()
    print 'done'
    conn.close()



def saveWorkersData(ret):    
    conn=getConn()
    cur=conn.cursor()

    dt=time.strftime("%Y-%m-%d %H:%M:%S")

    print 'Inserting workers....'
    for r in ret:
        for row in r:
            s=row['username'].split('.')

            sql2="insert into worker_info values('%s','%s','%s','%s','%s','%s','%s')" % (s[0],s[1],row['password'],row['shares'],row['hashrate'],row['difficulty'],dt)
            cur.execute(sql2)
            
    conn.commit()
    print 'done'
    conn.close()

def getAddressListByAlgo(algo,coin):
    
    conn=getConn()
    cur=conn.cursor()
    sql="select * from user_address where algo='%s'" % algo

    data=[]
    try:
        cur.execute(sql)
        results=cur.fetchall()
        for row in results:
            r={}
            r['address']=row[0]
            r['algo']=row[1]
            r['coin']=row[2]
            data.append(r)

    except MySQLdb.Error,e:

        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
       
    conn.close()
    return data


def loopBalance():
    try:
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        print '>>>>>start fetching all balance...'
        #users=getAddressListByAlgo('decred','')
        users=getAllAddress()
        data1=fetchAllBalanceData(users)
        saveBalance(data1)
    finally:
        timer=threading.Timer(30, loopBalance)
        timer.start()

def loopDashboardData():
    try:
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        print '>>>>>start fetching all dashboard...'
        #users=getAddressListByAlgo('decred','')
        users=getAllAddress()
        data1=fetchAllDashboardData(users)
        saveDashboardData(data1)
    finally:
        timer=threading.Timer(77, loopDashboardData)
        timer.start()

def loopTransactionData():
    try:
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        print '>>>>>start fetching all transaction...'
        #users=getAddressListByAlgo('decred','')
        users=getAllAddress()
        data1=fetchAllTransactionData(users)
        
        saveTransactionData(data1)
    finally:
        timer=threading.Timer(197, loopTransactionData)
        timer.start()

def loopWorkerData():
    try:
        print time.strftime('%H:%M:%S',time.localtime(time.time()))
        print '>>>>>start fetching all workers info...'
        #users=getAddressListByAlgo('decred','')
        users=getAllAddress()
        deleteWorkersData(users)
        data3=fetchAllWorkersData(users)
        saveWorkersData(data3)
    finally:
        timer=threading.Timer(125, loopWorkerData)
        timer.start()

if __name__== "__main__":
    #getBalance(url_test)
    

    loopBalance()
    loopDashboardData()
    loopTransactionData()
    loopWorkerData()

    #users=getAllAddress()


    # deleteWorkersData(users)
    # data3=fetchAllWorkersData(users)
    # saveWorkersData(data3)

    # data2= fetchAllDashboardData(users)
    # print data2
    # saveDashboardData(data2)

    # data3=fetchAllTransactionData(users)
    # print data3
    # saveTransactionData(data3)

    #
    #data2=fetchAllTransactionData(users)
    

