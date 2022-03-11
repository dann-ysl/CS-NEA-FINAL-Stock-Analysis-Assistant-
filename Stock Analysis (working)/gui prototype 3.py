from tkinter import *
import pandas_datareader as pd
import matplotlib.pyplot as plt
import datetime as dt
import csv
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class mainWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        #self.master = master
        master.title("Stock Analysis Assistant")

        self.top = topFrame(self)
        self.mid = middleFrame(self)
        self.bot = bottomFrame(self)

        self.top.pack(fill=X , padx=3, pady = 3)
        self.mid.pack(fill=X , padx=3, pady = 3)
        self.bot.pack(fill=X)

        self.top.displayBtn.config(command=self.mid.displayScreener)
        self.top.clearBtn.config(command=self.mid.clearScreener)

    def passArr(self, arr):
        self.mid.displayArr = arr


class topFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.label = Label(self, text="Screener")
        self.entryBox = Entry(self)
        self.displayBtn = Button(self, text="Display")
        self.clearBtn = Button(self, text="Clear")
      
        self.label.grid(row=0, column = 0, columnspan=3)
        self.entryBox.grid(row=1, column = 0)
        self.displayBtn.grid(row=1,column = 1)
        self.clearBtn.grid(row=1, column = 2)

class middleFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.displayArr = None

        #self.displayBtn = Button(self, text="Display", command=self.displayScreener)
        #self.clearBtn = Button(self, text="Clear", command=self.clearScreener)
        self.header_ticker = Label(self, text="Ticker")
        self.header_preview = Label(self, text = "Last 90 Days")
        self.header_close = Label(self, text = "Close Price")

        #self.displayBtn.grid(row=0,column = 0)
        #self.clearBtn.grid(row=0, column = 1)
        self.header_ticker.grid(row=1,column=0)
        self.header_preview.grid(row=1,column=1)
        self.header_close.grid(row=1, column=2)

    def displayScreener(self):
        arr = self.displayArr
        currentRow = 2
        for i in range(len(arr)):
            buttonWindow(self, arr[i][0]).grid(row = currentRow, column = 0)
            Label(self, image = arr[i][1]).grid(row = currentRow, column = 1)
            Label(self, text = "{:.2f}".format(float(arr[i][2]))).grid(row = currentRow, column = 2)

            currentRow += 1
    
    def clearScreener(self):
        for item in self.grid_slaves():
            current = int(item.grid_info()["row"])
            if current > 1:
                item.grid_forget()
    
    def sortScreener(self):
        arr = self.displayArr


class bottomFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.exitBtn = Button(self, text = 'Exit', command = root.destroy)
        self.exitBtn.pack(side="right")

class buttonWindow(Button):
    def __init__(self, master, name, *args, **kwargs):
        Button.__init__(self, master, *args, **kwargs)
        self.config(text = name, command=lambda: subWindow(self, name))

class subWindow(Toplevel):
    def __init__(self, master, ticker):
        Toplevel.__init__(self, master)
        #self.ticker = ticker
        self.title("{}".format(ticker))
        
        today = dt.date.today()
        start = today + dt.timedelta(-90)
        df = pd.DataReader(ticker, "yahoo", start, today)
        dfClose = df["Close"]

        fig = Figure(figsize=(5,5), dpi = 100)
        stockPlot = fig.add_subplot(1,1,1)
        stockPlot.plot(dfClose)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.quitBtn = Button(self, text="Quit", command=self.destroy)
        self.quitBtn.pack()


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

        if lastDate[0] != str(dt.date.today()):
            setCurrentDate(currentDate)
            setCurrentRecord(arr, currentRecord)
        
    else:#will never be executed once the file has been created
        setCurrentDate(currentDate)
        setCurrentRecord(arr, currentRecord)

    return(savePlot(currentRecord))

def sortRecord(arr, column):
    length = len(arr)
    output = [0 for x in range(length)]
    sortArr = [[0,0] for x in range(length)]

    for i in range(length):#extract values from column
        sortArr[i][0] = i
        sortArr[i][1] = arr[i][column]
    
    sortArr = mergeSortIndex(sortArr)
    for j in range(length):
        index = sortArr[j][0]
        output[j] = arr[index]

    return output
    
def mergeSortIndex(arr):

    length = len(arr)
    if length > 1:
        if length % 2 == 0:
            mid = int(length/2)
        else:
            mid = int((length - 1)/2)

        leftArr = mergeSortIndex(arr[0:mid])
        rightArr = mergeSortIndex(arr[mid:length])

        i = 0
        j = 0
        k = 0

        l = len(leftArr)
        r = len(rightArr)
        output = [0 for x in range(l+r)]

        while (i < l) and (j < r):
            if leftArr[i][1] < rightArr[j][1]:
                output[k] = leftArr[i]
                i += 1
            else:
                output[k] = rightArr[j]
                j += 1
            
            k += 1
        
        while i < l:
            output[k] = leftArr[i]
            i += 1
            k += 1
        
        while j < r:
            output[k] = rightArr[j]
            j += 1
            k += 1

        return output
    
    else:
        return arr


###################################################################################
root = Tk()
#root.geometry("500x500")
tickerArr = ["TSLA","MSFT","AAPL"]
displayArr = initialise(tickerArr)

home = mainWindow(root, width=500, bg="#000000")
home.pack()
home.passArr(displayArr)

root.mainloop()
###################################################################################