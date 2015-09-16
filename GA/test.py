__author__ = 'milanashara'
import gaextractor
from datetime import date, datetime, timedelta
authentication = gaextractor.Authentication()
#print authentication
extractor = gaextractor.Extractor(authentication)
#print extractor
#print extractor.listprofiles()
print extractor.set_all_app_traffic_profile_id()
#print extractor.accountid

date_  = datetime.today()
date_ = date_ - timedelta(days=2)
date_= date_.strftime("%Y-%m-%d")
#print date_
metrics = ['ga:screenviews', 'ga:uniqueScreenViews']
dimensions = ['ga:screenName']
filters = ['ga:screenName=@/day-view/']
data = extractor.extractdata(metrics=metrics,dimensions=dimensions,filters=filters,start_date=date_,end_date=date_)
extractor.to_csv()
extractor.to_json()
totalResults =  data['totalResults']
i=1

while(i < totalResults):
    data = extractor.extractdata(metrics=metrics,dimensions=dimensions,filters=filters,start_date=date_,end_date=date_,start_index=i)
    print data
    i += 1000


#print extractor.extractdata(['ga:visits'])