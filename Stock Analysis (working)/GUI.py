###GUI module
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

###self-built modules
from indicators import * 
from sortsearch import *

###API
import yfinance as yf

###date and time Python module
import datetime as dt

###File reader module
import csv
import os

def setCurrentDate(location): #gets the current date and writes it to the location
    with open(location, "w", newline = "") as writefile:
            writer = csv.writer(writefile)
            writer.writerow([dt.date.today()])

def setCurrentRecord(arr, location): #gets an array of tickers, and iterates through them, adding their respective information to a row in the csv file, whose location is a parameter of the function
    today = dt.date.today()
    start = today + dt.timedelta(-365)

    header = ["ticker","previewLoc","eval","closePrice","change","pctChange","vol","mktCap","volatility365","RSI"]
    data = []

    for ticker in arr:
        dataEntry = []
        df = yf.download(ticker, start, today)
        shares = yf.Ticker(ticker)
        dfClose = df["Close"]
        dfClose90 = dfClose[-90:]

        ###image export - creates a new directory which is specific to the ticker, determines whether the first value of the "90 days close prices" is bigger than or smaller than today's close price
        imageLoc = "images/{}90.png".format(ticker)
        if dfClose90[0] < dfClose90[-1]: #if it has decreased overall, then the graph line is colour is red, otherwise it is green
            color = "lime"
        else:
            color = "red"
        
        plt.figure(figsize=(3,1))
        plt.axis("off")
        plt.plot(dfClose90, color = color)
        plt.savefig(imageLoc, bbox_inches="tight", transparent = "True") #saves plot to separate image
        plt.cla()

        ###technical evaluation - calls techEval() to get buy, sell or neutral metric
        evalValue = techEval(dfClose)

        ###closePrice - close price
        close = dfClose[-1]

        ###change - measures change in price from yesterday
        change = dfClose[-1] - dfClose[-2]

        ###pctChange - measure percentage change in price from yesterday by calling PCT()
        pctChange = (PCT(dfClose[-2:],False))[0]

        ###volume - gets the amount of shares traded today
        volume = df["Volume"][-1]

        ###mktCap - calculates market capitalisation by getting the outstanding shares and today's close price and input into MKTCAP()
        mktCap = MKTCAP(dfClose[-1], shares.info["sharesOutstanding"])

        ###volatility (last calendar year) -  calls VOLATILITY() on the array of close prices and multiplies it by 100 to get it in terms of percentage
        # the reason we do (len(dfClose)-1) instead of 365, is because there isn't exactly 365 values in the array (as the market is not open on weekends and holidays)
        vol365 = (VOLATILITY(dfClose, (len(dfClose)-1), False)[0])*100
        
        ###RSI - calculates RSI by calling RSI(), we only need to pass in the last 15 values, as that is the minimum amount required for the RSI calculation to work
        RSICalc = (RSI(dfClose[-15:], False))[0]

        ###adding data to row in the array/file in the record
        dataEntry.append(ticker)
        dataEntry.append(imageLoc)
        dataEntry.append(evalValue)
        dataEntry.append(close)
        dataEntry.append(change)
        dataEntry.append(pctChange)
        dataEntry.append(volume)
        dataEntry.append(mktCap)
        dataEntry.append(vol365)
        dataEntry.append(RSICalc)

        data.append(dataEntry)
    
    with open(location, "w", newline = "") as writefile:
        writer = csv.writer(writefile)
        writer.writerow(header)
        writer.writerows(data)

def savePlot(location): #turns the flat file database, into a 2D array where our program can interpret it
    output = []

    with open(location , "r") as readfile:
        reader = csv.reader(readfile)
        next(reader)
        for row in reader:
            outputEntry = []
            img = PhotoImage(file = row[1])

            outputEntry.append(row[0])
            outputEntry.append(img)
            outputEntry.append(float(row[2]))
            outputEntry.append(float(row[3]))
            outputEntry.append(float(row[4]))
            outputEntry.append(float(row[5]))
            outputEntry.append(float(row[6]))
            outputEntry.append(float(row[7]))
            outputEntry.append(float(row[8]))
            outputEntry.append(float(row[9]))

            output.append(outputEntry)
    
    return output

def initialise(arr): #checks if the program is up to date, otherwise it will update the contents of the flat file
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
    
def isRealNumber(value): #checks if the parameter is a real number or not (includes negatives and decimals)
    try:
        float(value)
    except ValueError:
        return False
    
    return True

def reverseArray(arr): #reverse the array
    length = len(arr)
    output = [0 for x in range(length)]

    for i in range(length):
        output[i] = arr[length - 1 - i]

    return output

def transpose(arr): #transposes a 2D array
    xlength = len(arr)
    ylength = len(arr[0])
    output = [[0 for x in range(xlength)] for y in range(ylength)]

    for i in range(xlength):

        for j in range(ylength):
            output[j][i] = arr[i][j]

    return output

def formatMKTCAP(mktCap): #string formatting for display the large values of market capitalisation
    if mktCap >= 1000: #checks if bigger than or equal to 1000
        if mktCap >= 1000000: #checks if bigger than or equal to 1 million
            if mktCap >= 1000000000: #checks if bigger than or equal to 1 billion
                if mktCap >= 1000000000000: #checks if bigger than or equal to 1 trillion
                    return (str("{:.4f}".format(mktCap/1000000000000))+"T") #divides number by a trillion and append a “T”
                return (str("{:.4f}".format(mktCap/1000000000))+"B") #divides number by a billion and append a “B”
            return (str("{:.4f}".format(mktCap/1000000))+"M") #divides number by a million and append a “M”
        return (str("{:.4f}".format(mktCap/1000))+"k") #divides number by a thousand and append a “k”
    return (str("{:.4f}".format(mktCap))) #just returns market capitalisation

class mainWindow(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        master.title("Stock Analysis Assistant")

        self.top = topFrame(self)
        self.mid = middleFrame(self)
        self.bot = bottomFrame(self)

        self.top.pack(fill=X , padx=3, pady = 3)
        self.mid.pack(fill=X , padx=3, pady = 3)
        self.bot.pack(fill=X)

        self.top.displayBtn.config(command=lambda: self.mid.displayScreener(self.top.getFilter()))
    
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
        self.displayBtn = Button(self, text="Display")
        self.clearBtn = Button(self, text="Clear", command=self.clear)
      
        self.label.grid(row=0, column = 0, columnspan=3)
        self.displayBtn.grid(row=1,column = 0)
        self.clearBtn.grid(row=1, column = 1)

        self.closeEntry = filterEntry(self, "Close Price")
        self.closeEntry.grid(row=2, column=0, sticky="e")

        self.changeEntry = filterEntry(self, "Change")
        self.changeEntry.grid(row=2, column=1, sticky="e")

        self.PCTchangeEntry = filterEntry(self, "Change%")
        self.PCTchangeEntry.grid(row=2, column=2, sticky="e")

        self.volumeEntry = filterEntry(self, "Volume")
        self.volumeEntry.grid(row=3, column=0, sticky="e")

        self.mktCapEntry = filterEntry(self, "Market Cap")
        self.mktCapEntry.grid(row=3, column=1, sticky="e")

        self.volatilityEntry = filterEntry(self, "Volatility")
        self.volatilityEntry.grid(row=3, column=2, sticky="e")

        self.RSIEntry = filterEntry(self, "RSI")
        self.RSIEntry.grid(row=4, column=0, sticky="e")
    
    def getFilter(self):
        self.filterValue = []
        
        closeEntry = self.numericalCheck(self.closeEntry.entryLB.get(), self.closeEntry.entryUB.get(), "Close Price")
        if closeEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(closeEntry)

        changeEntry = self.numericalCheck(self.changeEntry.entryLB.get(), self.changeEntry.entryUB.get(), "Change")
        if changeEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(changeEntry)

        PCTchangeEntry = self.numericalCheck(self.PCTchangeEntry.entryLB.get(), self.PCTchangeEntry.entryUB.get(), "Change%")
        if PCTchangeEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(PCTchangeEntry)

        volumeEntry = self.numericalCheck(self.volumeEntry.entryLB.get(), self.volumeEntry.entryUB.get(), "Volume")
        if volumeEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(volumeEntry)
        
        mktCapEntry = self.numericalCheck(self.mktCapEntry.entryLB.get(), self.mktCapEntry.entryUB.get(), "Market Cap")
        if mktCapEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(mktCapEntry)

        volatilityEntry = self.numericalCheck(self.volatilityEntry.entryLB.get(), self.volatilityEntry.entryUB.get(), "Volatility")
        if volatilityEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(volatilityEntry)

        RSIEntry = self.numericalCheck(self.RSIEntry.entryLB.get(), self.RSIEntry.entryUB.get(), "RSI")
        if RSIEntry == "n":
            return self.reset()
        else:
            self.filterValue.append(RSIEntry)

        self.filterArr = search(self.master.displayArr, self.filterValue)
        self.master.mid.displayArr = self.filterArr
        return self.filterArr
    
    def reset(self):
        self.master.mid.displayArr = self.master.displayArr
        self.master.mid.techEval.sorted = False
        self.master.mid.closeFrame.sorted = False
        self.master.mid.changeFrame.sorted = False
        self.master.mid.PCTchangeFrame.sorted = False
        self.master.mid.volumeFrame.sorted = False
        self.master.mid.mktCapFrame.sorted = False
        self.master.mid.volatilityFrame.sorted = False
        self.master.mid.RSIFrame.sorted = False
        return self.master.displayArr
    
    def clear(self):
        self.closeEntry.entryLB.delete(0, END)
        self.closeEntry.entryUB.delete(0, END)
        self.changeEntry.entryLB.delete(0, END)
        self.changeEntry.entryUB.delete(0, END)
        self.PCTchangeEntry.entryLB.delete(0, END)
        self.PCTchangeEntry.entryUB.delete(0, END)
        self.volumeEntry.entryLB.delete(0, END)
        self.volumeEntry.entryUB.delete(0, END)
        self.mktCapEntry.entryLB.delete(0, END)
        self.mktCapEntry.entryUB.delete(0, END)
        self.volatilityEntry.entryLB.delete(0, END)
        self.volatilityEntry.entryUB.delete(0, END)
        self.RSIEntry.entryLB.delete(0, END)
        self.RSIEntry.entryUB.delete(0, END)
    
    def numericalCheck(self, entryLB, entryUB, name):
        if entryLB == "" and entryUB == "": #if both entries are blank
            return (["",""])
        elif entryLB == "": #defaults the lower bound to a negative integer that should be the maximum negative value to catch all the values from the bottom of the category
            entryLB = -1000000000000000
        elif entryUB == "": #defaults the upper bound to a positive integer that should be the maximum positive value to catch all the values from the top of the category
            entryUB = 1000000000000000

        if (isRealNumber(entryLB) == True) and (isRealNumber(entryUB) == True): #then checks if they are numbers
            if float(entryLB) > float(entryUB): #returns an error message if the lower bound is higher than the upper bound
                messagebox.showerror("Error","Lower bound for {} is higher than the upper bound".format(name))
                return "n"
        else: #returns an error message if the values are non-numerical
            messagebox.showerror("Error","{} has an entry with a non-numerical value".format(name))
            return "n"
            
        return ([float(entryLB), float(entryUB)])
     
class middleFrame(Frame):
    def __init__(self, master, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.displayArr = None

        self.header_ticker = Label(self, text="Ticker")
        self.header_ticker.grid(row=0,column=0)

        self.header_preview = Label(self, text = "Last 90 Days")
        self.header_preview.grid(row=0,column=1)

        self.techEval = screenerHeader(self, "Technical Evaluation", 2)
        self.techEval.grid(row=0,column=2)

        self.closeFrame = screenerHeader(self, "Close Price", 3)
        self.closeFrame.grid(row=0, column=3)

        self.changeFrame = screenerHeader(self, "Change", 4)
        self.changeFrame.grid(row=0, column=4)

        self.PCTchangeFrame = screenerHeader(self, "Change%", 5)
        self.PCTchangeFrame.grid(row=0, column=5)

        self.volumeFrame = screenerHeader(self, "Volume", 6)
        self.volumeFrame.grid(row=0, column=6)

        self.mktCapFrame = screenerHeader(self, "Market Cap", 7)
        self.mktCapFrame.grid(row=0, column=7)
        
        self.volatilityFrame = screenerHeader(self, "Volatility", 8)
        self.volatilityFrame.grid(row=0, column=8)

        self.RSIFrame = screenerHeader(self, "RSI", 9) 
        self.RSIFrame.grid(row=0, column=9)

    def displayScreener(self, arr):
        self.clearScreener()
        currentRow = 2

        for i in range(len(arr)):
            signal = arr[i][2]

            # takes the technical evaluative metric and checks if it is <= -2, which will give a sell signal (red), checks if it is >= 2, which will give a buy signal (green), otherwise it will give a null signal
            if signal <= -2:
                signal = "Sell"
                colourA = "red"
            elif signal >= 2:
                signal = "Buy"
                colourA = "green"
            else:
                signal = "Nothing"
                colourA = "black"

            #checks if the change in price is positive or negative and applies the corresponding colour to represent the signed number
            if float(arr[i][4]) >= 0:
                colourB = "green"
            else:
                colourB = "red"
            
            buttonWindow(self, arr[i][0]).grid(row = currentRow, column = 0)
            Label(self, image = arr[i][1]).grid(row = currentRow, column = 1)
            Label(self, text = signal, fg = colourA).grid(row = currentRow, column = 2)
            Label(self, text = "{:.2f}".format(float(arr[i][3]))).grid(row = currentRow, column = 3)
            Label(self, text = "{:.2f}".format(float(arr[i][4])), fg = colourB).grid(row = currentRow, column = 4)
            Label(self, text = "{:.2f}%".format(float(arr[i][5])), fg = colourB).grid(row = currentRow, column = 5)
            Label(self, text = "{:,}".format(int(arr[i][6]))).grid(row = currentRow, column = 6)
            Label(self, text = formatMKTCAP(float(arr[i][7]))).grid(row = currentRow, column = 7)
            Label(self, text = "{:.2f}%".format(float(arr[i][8]))).grid(row = currentRow, column = 8)
            Label(self, text = "{:.2f}".format(float(arr[i][9]))).grid(row = currentRow, column = 9)

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

class filterEntry(Frame):
    def __init__(self, master, name, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
        self.label = Label(self, text=name)
        self.entryLB = Entry(self, width=10)
        self.sep = Label(self, text = "-")
        self.entryUB = Entry(self, width=10)

        self.label.grid(row=0, column=0)
        self.entryLB.grid(row=0, column=1)
        self.sep.grid(row=0, column=2)
        self.entryUB.grid(row=0, column=3)

class screenerHeader(Frame):
    def __init__(self, master, name, column, *args, **kwargs):# column,
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
            self.sortArr = sortColumn(self.displayArr, self.column)
            self.sorted = True

        if index == 0:
            self.counter = 0
            output = self.sortArr
        elif index == 1:
            output = reverseArray(self.sortArr)
        elif index == 2:
            output = self.displayArr
        
        self.counter += 1
        self.sortBtn.config(text=self.logo[index])
        self.master.displayScreener(output)

class buttonWindow(Button):
    def __init__(self, master, name, *args, **kwargs):
        Button.__init__(self, master, *args, **kwargs)
        self.config(text = name, command=lambda: subWindow(self, name))

class subWindow(Toplevel):
    def __init__(self, master, ticker):
        Toplevel.__init__(self, master)
        self.title("{}".format(ticker))

        self.SMAButton = Button(self, text="SMA", command=self.SMAPlot)
        self.SMAEntry = Entry(self)
        self.SMAButton.grid(row=0,column=0)
        self.SMAEntry.grid(row=0,column=1)

        self.EMAButton = Button(self, text="EMA", command=self.EMAPlot)
        self.EMAEntry = Entry(self)
        self.EMAButton.grid(row=1,column=0)
        self.EMAEntry.grid(row=1,column=1)

        self.volatilityButton = Button(self, text="Volatility", command=self.volatilityPlot)
        self.volatilityEntry = Entry(self)
        self.volatilityButton.grid(row=2,column=0)
        self.volatilityEntry.grid(row=2,column=1)

        self.MACDButton = Button(self, text="MACD", command=self.MACDPlot)
        self.MACDButton.grid(row=3,column=0)

        self.RSIButton = Button(self, text="RSI", command=self.RSIPlot)
        self.RSIButton.grid(row=4,column=0)

        self.clearBtn = Button(self, text="Clear Graph", command=self.initialPlot)
        self.clearBtn.grid(row=5, columnspan=3)
        
        today = dt.date.today()
        start = today + dt.timedelta(-365)
        df = yf.download(ticker, start, today)
        self.dfClose = df["Close"]
        self.dfVolume = df["Volume"]
        self.length = len(self.dfClose)

        self.fig = Figure(figsize=(10,10), dpi = 100)
        self.initialPlot()

        self.quitBtn = Button(self, text="Quit", command=self.destroy)
        self.quitBtn.grid(row=7,columnspan=3,sticky="e")

    def initialPlot(self):
        self.fig.clf()
        
        self.fig = Figure(figsize=(7,7), dpi = 100)
        self.stockPlot = self.fig.add_subplot(4,1,(1,2))
        self.volumePlot = self.fig.add_subplot(4,1,3)
        self.extraPlot = self.fig.add_subplot(4,1,4)
        self.stockPlot.plot(self.dfClose)
        self.volumePlot.bar((self.dfVolume.index).tolist(), self.dfVolume)
        self.fig.align_xlabels([self.stockPlot, self.volumePlot, self.extraPlot])


        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=6,columnspan=2)

    def SMAPlot(self):
        period = self.SMAEntry.get()
        if (period.isdigit() == True) and int(period) > 0:
            period = int(period)

            SMAArray = fastSMA(self.dfClose, period, True)
            SMAArray = transpose(SMAArray)

            self.stockPlot.plot(SMAArray[0],SMAArray[1])

            self.canvas.draw()
        else:
            messagebox.showerror("Error","Enter an integer bigger than zero")

    def EMAPlot(self):
        period = self.EMAEntry.get()
        if (period.isdigit() == True) and int(period) > 0:
            period = int(period)

            if period > (self.length / 2):
                messagebox.showwarning("Warning","It is advisable to use an EMA period which is less than half the number of datapoints (dates) on the graph. \nDoing so will allow the EMA to converge more accurately \nNumber of datapoints: {} \nYour input for period: {}".format(self.length, period))

            EMAArray = EMA(self.dfClose, period, True)
            EMAArray = transpose(EMAArray)

            self.stockPlot.plot(EMAArray[0],EMAArray[1])

            self.canvas.draw()
        else:
            messagebox.showerror("Error","Enter an integer bigger than zero")

    def volatilityPlot(self):
        period = self.volatilityEntry.get()
        if (period.isdigit() == True) and int(period) > 0:
            period = int(period)

            if period < 5:
                messagebox.showwarning("Warning","It is advisable to use a value bigger than or equal to 5.\nAny value lower would realistically be too short of a window to observe.")

            volatilityArray = VOLATILITY(self.dfClose, period, True)
            volatilityArray = transpose(volatilityArray)

            self.extraPlot.cla()
            self.extraPlot.plot(volatilityArray[0],volatilityArray[1])
            self.fig.align_xlabels([self.stockPlot, self.volumePlot, self.extraPlot])

            self.canvas.draw()
        else:
            messagebox.showerror("Error","Enter an integer bigger than zero")

    def MACDPlot(self):
        MACD_Array = MACD(self.dfClose, True)
        fastArray = MACD_Array[0]
        slowArray = MACD_Array[1]
        MACDArray = MACD_Array[2]
        sigArray = MACD_Array[3]
        histArray = MACD_Array[4]

        fastArray = transpose(fastArray)
        slowArray = transpose(slowArray)
        MACDArray = transpose(MACDArray)
        sigArray = transpose(sigArray)
        histArray = transpose(histArray)

        self.stockPlot.plot(fastArray[0], fastArray[1])
        self.stockPlot.plot(slowArray[0], slowArray[1])

        self.extraPlot.cla()
        self.extraPlot.plot(MACDArray[0], MACDArray[1])
        self.extraPlot.plot(sigArray[0], sigArray[1])
        self.extraPlot.bar(histArray[0], histArray[1])
        self.extraPlot.axhline(y=0, color="grey")

        self.canvas.draw()

    def RSIPlot(self):
        RSIArray = RSI(self.dfClose, True)

        RSIArray = transpose(RSIArray)

        self.extraPlot.cla()
        self.extraPlot.plot(RSIArray[0], RSIArray[1], color="purple")
        self.extraPlot.axhline(y=25, color="red")
        self.extraPlot.axhline(y=75, color="red")

        self.canvas.draw()


###################################################################################
root = Tk()

tickerArr = ["TSLA","MSFT","AAPL","GOOG","AMZN","NVDA","FB","JPM","CSCO","AZN"]
displayArr = initialise(tickerArr)

home = mainWindow(root, width=1000, bg="#000000")
home.pack()
home.passArr(displayArr)

root.mainloop()
###################################################################################


###ADDING COLUMNS-> #1. __init__ of topFrame: create new filterEntry() class
                    #2. getFilter() of topFrame: add numericalCheck() method to check newly created filterEntry() object
                    #3. add column to reset() and clear() of topFrame
                    #4. __init__ of middleFrame: create new screenerHeader() class
                    #5. displayScreener() of middleFrame: create new label with appropriate string formatting
                    #6. setCurrentRecord(): add appropriate calculating function for column and append
                    #7. savePlot(): append 1+ column