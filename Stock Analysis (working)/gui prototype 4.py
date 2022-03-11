###GUI
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from indicators import * ###my functions
import pandas_datareader as pd ###API
import matplotlib.pyplot as plt ###Graph plotter
import datetime as dt #date and time
###File reader
import csv
import os


def setCurrentDate(location):
    with open(location, "w", newline = "") as writefile:
            writer = csv.writer(writefile)
            writer.writerow([dt.date.today()])

def setCurrentRecord(arr, location):
    today = dt.date.today()
    start = today + dt.timedelta(-365)
    start90 = today + dt.timedelta(-90)

    header = ["ticker","previewLoc","close","volatility365"]
    data = []

    for ticker in arr:
        df = pd.DataReader(ticker, "yahoo", start, today)
        dfClose = df["Close"]
        dfClose90 = dfClose[start90:]

        ###image export
        dataEntry = []
        imageLoc = "images/{}90.png".format(ticker)
        close = dfClose[len(dfClose)-1]

        if dfClose90[0] < dfClose90[-1]:
            color = "lime"
        else:
            color = "red"
        
        plt.figure(figsize=(3,1))
        plt.axis("off")
        plt.plot(dfClose90, color = color)
        plt.savefig(imageLoc, bbox_inches="tight", transparent = "True")
        plt.cla()
        ###

        ###volatility calculation (last 365 days)
        vol365 = volatility(dfClose, (len(dfClose)-1), False)[0]
        ###

        ###adding data to row/file
        dataEntry.append(ticker)
        dataEntry.append(imageLoc)
        dataEntry.append(close)
        dataEntry.append(vol365)

        data.append(dataEntry)
        ###
    
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
            outputEntry.append(row[3])

            output.append(outputEntry)
    

    return output

def initialise(arr):#sort record in here
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

def sortedArray(arr, column):
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

        #self.top.displayBtn.config(command=lambda: self.mid.displayScreener(self.displayArr))
        self.top.clearBtn.config(command=self.mid.clearScreener)
    
    def passArr(self, arr):
        self.displayArr = arr
        self.mid.displayArr = arr
        self.mid.displayScreener(arr)
        

class topFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.filterValue = None
        self.filtered = False

        self.label = Label(self, text="Screener")
        self.closeEntry = Entry(self)
        self.displayBtn = Button(self, text="Display")
        self.clearBtn = Button(self, text="Clear")
        #self.filter = Button(self, text="Filter")
      
        self.label.grid(row=0, column = 0, columnspan=3)
        self.closeEntry.grid(row=1, column = 0)
        self.displayBtn.grid(row=1,column = 1)
        self.clearBtn.grid(row=1, column = 2)
        #self.filter.grid(row=2)
    
    def getFilter(self):
        if self.filtered == False:
            self.filterValue = []
            self.filtered = True
        




        self.closeEntry.get()

class middleFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.displayArr = None

        #self.displayArr = self.master.displayArr

        self.header_ticker = Label(self, text="Ticker")
        self.header_ticker.grid(row=0,column=0)

        self.header_preview = Label(self, text = "Last 90 Days")
        self.header_preview.grid(row=0,column=1)

        self.closeFrame = screenerHeader(self, "Close Price", 2)
        self.closeFrame.grid(row=0, column=2)

        self.volatilityFrame = screenerHeader(self, "Volatility", 3)
        self.volatilityFrame.grid(row=0, column=3)


    def displayScreener(self, arr):
        self.clearScreener()
        currentRow = 2

        #for ticker in arr:
            #screenerRow(self, ticker).grid(row = currentRow, columnspan=3)
            #currentRow += 1

        for i in range(len(arr)):
            buttonWindow(self, arr[i][0]).grid(row = currentRow, column = 0)
            Label(self, image = arr[i][1]).grid(row = currentRow, column = 1)
            Label(self, text = "{:.2f}".format(float(arr[i][2]))).grid(row = currentRow, column = 2)
            Label(self, text = "{:.2f}%".format(float(arr[i][3])*100)).grid(row = currentRow, column = 3)

            currentRow += 1
    
    def clearScreener(self):
        for item in self.grid_slaves():
            current = int(item.grid_info()["row"])
            if current > 1:
                item.grid_forget()

class bottomFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.exitBtn = Button(self, text = "Exit", command = root.destroy)
        self.exitBtn.pack(side="right")

class screenerHeader(Frame):
    def __init__(self, master, name, column, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.master = master

        self.displayArr = None
        self.column = column
        self.sortArr = None
        self.sorted = False
        self.logo = ["v","^","-"]
        self.counter = 0

        self.header = Label(self, text=name)
        self.sortBtn = Button(self, text="-", command=self.sortScreener)

        self.header.grid(row=0, column=0)
        self.sortBtn.grid(row=0, column=1)
        
    def sortScreener(self):
        output = None
        index = self.counter % 3

        if self.sorted == False:
            self.displayArr = self.master.displayArr
            self.sortArr = sortedArray(self.displayArr, self.column)
            self.sorted = True

        if index == 0:
            self.counter = 0
            output = self.sortArr
        elif index == 1:
            output = self.sortArr[::-1]
        elif index == 2:
            output = self.displayArr
        
        self.counter += 1
        self.sortBtn.config(text=self.logo[index])
        self.master.displayScreener(output)

class screenerRow(Frame):#not used
    def __init__(self, master, arr, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)

        self.tickerBtn = Button(self, text = arr[0], command=lambda: subWindow(self, arr[0]))
        self.previewImg = Label(self, image = arr[1])
        self.closePrice = Label(self, text = "{:.2f}".format(float(arr[2])))

        self.tickerBtn.grid(row = 0, column=0)
        self.previewImg.grid(row = 0, column=1)
        self.closePrice.grid(row = 0, column=2)

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


##today = dt.datetime.today()
#start = today + dt.timedelta(-365)##to be user input
#end = today
#df = pd.DataReader("TSLA", "yahoo", start, end)
#dfClose = df["Close"] #extracts only 'Close'

###################################################################################
root = Tk()
#root.geometry("500x500")
tickerArr = ["TSLA","MSFT","AAPL"]
displayArr = initialise(tickerArr)

home = mainWindow(root, width=1000, bg="#000000")
home.pack()
home.passArr(displayArr)

print()

root.mainloop()
###################################################################################


###ADDING COLUMNS-> #1. create frame in middleFrame
                    #2. add label in displayScreener
                    #3. add appropiate calculating function and append value in setCurrentRecord
                    #4. add append value in savePlot