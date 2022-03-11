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
        self.master = master
        self.master.title("Stock Analysis Assistant")

        #self.topFrame.grid_columnconfigure(0,weight=1)
        #self.topFrame.grid_columnconfigure(1,weight=1)
        #self.topFrame.grid_columnconfigure(2,weight=1)

        #self.middleFrame.grid_columnconfigure(0, weight=1)
        #self.middleFrame.grid_columnconfigure(1, weight=1)
        #self.middleFrame.grid_columnconfigure(2, weight=1)

        #self.bottomFrame.grid_columnconfigure(0, weight=1)

        ##########frame create and pack
        self.topFrame = Frame(self, width = 500)
        self.middleFrame = Frame(self, width = 500)
        self.bottomFrame = Frame(self, width = 500)

        self.topFrame.pack(fill=X , padx=3, pady = 3)
        self.middleFrame.pack(fill=X , padx=3, pady = 3)
        self.bottomFrame.pack(fill=X)
        ##########

        ##########topFrame widgets
        self.label_1 = Label(self.topFrame, text="Screener")
        self.entryBox = Entry(self.topFrame)
        self.displayBtn = Button(self.topFrame, text="Display", command=self.displayScreener)
        self.clearBtn = Button(self.topFrame, text="Clear", command=self.clearScreener)

        self.label_1.grid(row=0, columnspan = 3)
        self.entryBox.grid(row=1, column = 0)
        self.displayBtn.grid(row=1,column = 1)
        self.clearBtn.grid(row=1, column = 2)
        ##########

        ##########middleFrame widgets
        self.header_ticker = Label(self.middleFrame, text="Ticker")
        self.header_preview = Label(self.middleFrame, text = "Last 90 Days")
        self.header_close = Label(self.middleFrame, text = "Close Price")

        self.header_ticker.grid(row=0,column=0)
        self.header_preview.grid(row=0,column=1)
        self.header_close.grid(row=0, column=2)
        ##########

        ##########bottomframe widgets
        self.exitBtn = Button(self.bottomFrame, text = 'Exit', command = master.destroy)
        self.exitBtn.pack(side="right")
        ##########
    
    def displayScreener(self):
        global displayArr
        arr = displayArr
        currentRow = 1
        for i in range(len(arr)):
            ticker = arr[i][0]
            rowButton(self.middleFrame, ticker).grid(row = currentRow, column = 0)
            self.image = Label(self.middleFrame, image = arr[i][1])
            self.close = Label(self.middleFrame, text = arr[i][2])

            self.image.grid(row = currentRow, column = 1)
            self.close.grid(row = currentRow, column = 2)
            
            currentRow += 1
    
    def clearScreener(self):
        for item in self.middleFrame.grid_slaves():
            current = int(item.grid_info()["row"])
            if current > 0:
                item.grid_forget()







class rowButton(Button):

    def __init__(self, ticker):
        Button.__init__()
        self.config(command=lambda: subWindow(ticker))

        


    
class subWindow(Toplevel):

    def __init__(self, ticker):
        Toplevel.__init__(self)
        self.ticker = ticker
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

###################################################################################
root = Tk()
#root.geometry("500x500")
tickerArr = ["TSLA","MSFT","AAPL"]
displayArr = initialise(tickerArr)

home = mainWindow(root, width=500, bg="#000000")
home.pack()

root.mainloop()
###################################################################################