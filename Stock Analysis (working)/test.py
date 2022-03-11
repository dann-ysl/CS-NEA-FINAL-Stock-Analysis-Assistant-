import yfinance as yf
import datetime as dt

today = dt.date.today()
start = today + dt.timedelta(-100)
end = today

a = yf.download("AZN", start, today)

print(a)