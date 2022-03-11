from tkinter import *
import pandas_datareader as pd
import matplotlib.pyplot as plt
import datetime as dt
import csv
import os

def displayScreener(arr):
    currentRow = 1
    for i in range(len(arr)):
        stock = Button(screenerFrame, text = arr[i][0])
        image = Label(screenerFrame, image = arr[i][1])
        close = Label(screenerFrame, text = arr[i][2])

        stock.grid(row = currentRow, column = 0)
        image.grid(row = currentRow, column = 1)
        close.grid(row = currentRow, column = 2)
        currentRow += 1
    
def clearScreener():
    for item in screenerFrame.grid_slaves():
        current = int(screenerFrame.grid_info()["row"])
        if current > 0:
            item.grid_forget()

def setCurrentDate(location):
    with open(location, "w", newline = "") as writefile:
            writer = csv.writer(writefile)
            writer.writerow([dt.date.today()])

def setCurrentRecord(arr, location):
    today = dt.date.today()
    start = today + dt.timedelta(-90)

    header = ["ticker","previewLoc","close"]
    data = []

    for ticker in arr:
        df = pd.DataReader(ticker, "yahoo", start, today)
        dfClose = df["Close"]

        dataEntry = []
        imageLoc = "images/{}90.png".format(ticker)
        close = dfClose[len(dfClose)-1]

        if dfClose[0] < dfClose[len(dfClose)-1]:
            color = "lime"
        else:
            color = "red"
        
        plt.figure(figsize=(3,1))
        plt.axis("off")
        plt.plot(dfClose, color = color)
        plt.savefig(imageLoc, bbox_inches="tight", transparent = "True")
        plt.cla()

        dataEntry.append(ticker)
        dataEntry.append(imageLoc)
        dataEntry.append(close)

        data.append(dataEntry)
    
    with open(location, "w", newline = "") as writefile:
        writer = csv.writer(writefile)
        writer.writerow(header)
        writer.writerows(data)

def savePlot(location):
    output = []

    with open(location , "r") as readfile:
        reader = csv.reader(readfile)
        next(reader)
        for row in reader:
            outputEntry = []
            img = PhotoImage(file = row[1])

            outputEntry.append(row[0])
            outputEntry.append(img)
            outputEntry.append(row[2])

            output.append(outputEntry)
    
    return output

def initialise(arr):
    currentDate = "recordCache/currentDate.csv"
    currentRecord = "recordCache/currentRecord.csv"

    if os.path.exists(currentDate):
        with open(currentDate, "r") as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                lastDate = row
        print("yhyh")
        print (lastDate[0])
        print (dt.date.today())
        if lastDate[0] != dt.date.today():
            setCurrentDate(currentDate)
            setCurrentRecord(arr, currentRecord)
            print("currently resetting")
        
    else:#will never be executed once the file has been created
        setCurrentDate(currentDate)
        setCurrentRecord(arr, currentRecord)

    return(savePlot(currentRecord))

###################################################################################
root = Tk()

root.title("Stock Analysis Assistant")

tickerArr = ["TSLA","MSFT","AAPL"]
displayArr = initialise(tickerArr)

topFrame = Frame(root)
screenerFrame = Frame(root)

topFrame.grid(row=0)
screenerFrame.grid(row=1)

label_1 = Label(topFrame, text = "Screener")
entryBox = Entry(topFrame)
displayBtn = Button(topFrame, text = "Display", command = lambda: displayScreener(displayArr))
clearBtn = Button(topFrame, text = 'Clear', command = clearScreener)
header_ticker = Label(screenerFrame, text="Ticker")
header_90DaysPreview = Label(screenerFrame, text = "Last 90 Days")
header_closePrice = Label(screenerFrame, text = "Close Price")

label_1.grid(row=0, columnspan = 3)
entryBox.grid(row=1, column = 0)
displayBtn.grid(row=1,column = 1)
clearBtn.grid(row=1, column = 2)
header_ticker.grid(row=0,column=0)
header_90DaysPreview.grid(row=0,column=1)
header_closePrice.grid(row=0, column=2)


root.mainloop()
###################################################################################