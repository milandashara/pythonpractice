__author__ = 'milanashara'
from datetime import datetime, timedelta, date
from dateutil import parser
import time
import threading
# a =datetime.datetime.utcnow() - datetime.timedelta(days=2)
# b =datetime.datetime.utcnow() - datetime.timedelta(days=2)
# print (str(a.date()))
# print a.date().isoformat()
# print a.strftime('%Y-%m-%d')
# test={}
# if not  test:
#     print "milan"
# test[0]=0

# start = time.time()
#
# time.sleep(10)  # or do something more productive
#
# done = time.time()
# elapsed = int(done - start)
# print(elapsed)


# sov_update_time=None
# if  sov_update_time:
#     print "none"
#
# def foo():
#    print(time.ctime())
#    threading.Timer(10, foo).start()
# foo()
#
# print "milan"
# date_ =datetime.utcnow().date()
# date1 = datetime.utcnow().date()
# print  date1
# print date_==date1

curr_date=datetime.utcnow().date()-timedelta(days=2)
curr_date=curr_date-timedelta(days=1)

date_ =  parser.parse("2015-08-23")
print date_.date()
print datetime.strptime("2015-08-23",'%Y-%m-%d').date()
print type(date_)
print curr_date
print date_.date().strftime('%Y-%m-%d')
date.today()
print(

    type(date.fromtimestamp(
        int("1441161404")
    ).strftime('%Y-%m-%d'))
)
print datetime.fromtimestamp( int("1441843123")).date()