import MySQLdb
import time    
import datetime



def getConn():
    conn=MySQLdb.connect(host='localhost',user='root',passwd='d0ntpu5h',db='stratumproxy',port=3306)
    return conn

def updateDB():
    try:
        conn=getConn()
        
        cur=conn.cursor()

        dt=time.strftime("%Y-%m-%d %H:%M:%S")
        sql="select id,dt from transaction_data"
        cur.execute(sql)
        data=cur.fetchall()


        result=[]

        for item in data:
            d={}
            d["id"]=item[0]
            d["dt"]=item[1]
            result.append(d)

        for d in result:
            #print "old->" + d["dt"].strftime('%Y-%m-%d %H:%M:%S')
            h=d["dt"]+datetime.timedelta(hours=7)
            #print "new->" + h.strftime('%Y-%m-%d %H:%M:%S')

            sql="update transaction_data set dt='%s' where id='%s'" % (h.strftime('%Y-%m-%d %H:%M:%S'),d["id"])
            print sql
            cur.execute(sql)

        conn.commit()
        #print result
        cur.close()
        conn.close()

    except MySQLdb.Error,e:

        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        conn.rollback()



def insertDB():
    s="2099-01-24 21:38:22"
    d=datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
    h=d+datetime.timedelta(hours=7)
    print h.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    updateDB()
    #insertDB()