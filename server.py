from flask import Flask, render_template
from flask import jsonify
import MySQLdb
import os

app = Flask(__name__, static_folder='static', static_url_path='')
app.config['mysql_server']='localhost'
app.config['mysql_port']=3306
app.config['mysql_user']='root'
app.config['mysql_pass']='d0ntpu5h'
app.config['db']='stratumproxy'

mysqlinfo = {'USER':'root', 'PSWD':'d0ntpu5h', 'HOST':'localhost', 'PORT':3306}
#conn=MySQLdb.connect(host=Loginfo['HOST'],user=Loginfo['USER'],passwd=Loginfo['PSWD'],port=Loginfo['PORT'],charset='utf8')


def getConn():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='d0ntpu5h',db='stratumproxy',port=3306)
    return conn

def getBalance(address):
    column_list = []   
    result={}
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="select address,confirmed,unconfirmed,dt from user_status where address='%s'" % address
        cur.execute(sql)
        data=cur.fetchone()
        fields=cur.description
        cur.close()
        conn.close()

        for i in fields:
            column_list.append(i[0])
        
        result[column_list[0]]=data[0]
        result[column_list[1]]=str(data[1])
        result[column_list[2]]=str(data[2])
        result[column_list[3]]=str(data[3])

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result


def getDashboard(address):
    column_list = []   
    result={}
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="select address,hashrate,avghashrate,coin,invalid,hashrate_net,block,difficulty,nextdifficulty,dt from dashboard_data where address='%s'" % address
        cur.execute(sql)
        data=cur.fetchone()
        fields=cur.description
        cur.close()
        conn.close()

        for i in fields:
            column_list.append(i[0])
        
        result[column_list[0]]=data[0]
        result[column_list[1]]=str(data[1])
        result[column_list[2]]=str(data[2])
        result[column_list[3]]=str(data[3])
        result[column_list[4]]=str(data[4])
        result[column_list[5]]=str(data[5])
        result[column_list[6]]=str(data[6])
        result[column_list[7]]=str(data[7])
        result[column_list[8]]=str(data[8])
        result[column_list[9]]=str(data[9])

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result   


def getTransactions(address):
    column_list = []   
    result=[]
    
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="select address,amount,txid,dt from transaction_data where address='%s' ORDER by dt DESC LIMIT 20" % address
        cur.execute(sql)
        data=cur.fetchall()
        fields=cur.description
        cur.close()
        conn.close()

        for i in fields:
            column_list.append(i[0])
        
        for j in data:
            tran={}
            tran[column_list[0]]=j[0]
            tran[column_list[1]]=str(j[1])
            tran[column_list[2]]=j[2]
            tran[column_list[3]]=str(j[3])
            result.append(tran)

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result

def getWorkers(address):
    column_list = []   
    result=[]
    
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="select account,worker,password,hashrate,diff from worker_info where account='%s'" % address
        cur.execute(sql)
        data=cur.fetchall()
        fields=cur.description
        cur.close()
        conn.close()

        for i in fields:
            column_list.append(i[0])
        
        for j in data:
            tran={}
            tran[column_list[0]]=j[0]
            tran[column_list[1]]=j[1]
            tran[column_list[2]]=j[2]
            tran[column_list[3]]=str(j[3])
            tran[column_list[4]]=str(j[4])
            result.append(tran)

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result

def getIncome(address):
    
    result=[]
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="select DATE_FORMAT(dt,'%%Y/%%m/%%d') date,sum(amount) sum from transaction_data where address='%s' group by date ORDER by date DESC limit 5" % address
        cur.execute(sql)
        data=cur.fetchall()
        fields=cur.description
        cur.close()
        conn.close()

        for j in data:
            item={}
            item['date']=j[0]
            item['coins']=str(j[1])
            result.append(item)

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result


def getgbprofitperg():
    column_list = []   
    result={}
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="select lbry,dcr,blake2b,pascal,blake256r8,blake256r14,dt from profit_compare order by dt desc limit 1"
        cur.execute(sql)
        data=cur.fetchone()
        

        fields=cur.description
        cur.close()
        conn.close()

        for i in fields:
            column_list.append(i[0])
        
        print column_list
        
        result[column_list[0]]=str(data[0])
        result[column_list[1]]=str(data[1])
        result[column_list[2]]=str(data[2])
        result[column_list[3]]=str(data[3])
        result[column_list[4]]=str(data[4])
        result[column_list[5]]=str(data[5])
        result[column_list[6]]=str(data[6])

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result

def getX10CurrentProfit():
        with open('revs.json','r',encoding='utf-8') as f:
            #f.write(json.dumps(revs))
            c = f.read()
            print c


def getChartDataH(address):
     
    result=[]
    try:
        conn=getConn()
        cur=conn.cursor()

        sql="SELECT amount,dt FROM transaction_data WHERE dt >= NOW() - interval 1 DAY and address = '%s'" % address
        cur.execute(sql)
        data=cur.fetchall()

        cur.close()
        conn.close()

        for i in data:   
            d={}     
            d["amount"]=i[0]
            d["dt"]=i[1]
            result.append(d)

    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()
    return result



@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<address>')
def data(address):
    income=getIncome(address)
    datah=getChartDataH(address)
    print datah
    #print income
    return render_template('data.html',address=address,income=income,datah=datah)

@app.route('/balance/<address>')
def balance(address):
    result=getBalance(address)
    #print result
   
    return jsonify(result) 


@app.route('/dashboard/<address>')
def dashboard(address):
    result=getDashboard(address)
    #print result

    return jsonify(result) 

@app.route('/transactions/<address>')
def transactions(address):
    result=getTransactions(address)

    return jsonify(result) 

@app.route('/workers/<address>')
def workers(address):
    result=getWorkers(address)

    return jsonify(result) 

@app.route('/api/gbprofitperg')
def gbprofitperg():
    result=getgbprofitperg()
    #print result

    return jsonify(result) 

@app.route('/api/x10currentprofit')
def x10CurrentProfit():
    getX10CurrentProfit()


@app.route('/income/<address>')
def income(address):
    result=getIncome(address)
    #print result
   
    return jsonify(result) 


if __name__ == '__main__':
    
    app.run(
        host='0.0.0.0',
        port=8081,
        debug=True
        )