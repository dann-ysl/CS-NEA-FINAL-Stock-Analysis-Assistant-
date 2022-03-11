import datetime as dt
import quandl as qd

today = dt.datetime.today()
start = today + dt.timedelta(-100)
end = today
stock = qd.get('WIKI/TSLA', 
                  start_date="2020-01-01", 
                  end_date="2022-01-01", 
                  api_key="3N_CHhCV5yxe22HP-S3M")
print(stock)

##does not work!