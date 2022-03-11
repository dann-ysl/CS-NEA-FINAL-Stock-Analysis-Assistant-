import math

# old Simple Moving Average (SMA) - Calculates an average over last 'period' amount of days, and repeats it for the series of dates inputted. O(n^2), this function is for evidence purposes, but never actually used
def SMA(arr, period):
  length = len(arr)
  if length >= period:
    
    total = length - period + 1
    output = [0 for x in range(total)]
  
    for i in range(total):
      initial = 0
      
      for j in range(period):
        initial += arr[i + j]
      
      output[i] = initial/period
  
    return output
  else:
    print ("Unable to calculate SMA")

# add dates to 1D arrays (used by SMA), takes responsibility of adding dates, so SMA can output 1D (without date) or 2D (with date) arrays
def dateArray(orgArr, outArr):#orgArr: original array, outArr: output array
    output = [[0,0] for x in range(len(outArr))]
    offset = len(orgArr) - len(outArr) #calculates the offset needed to offset the starting position of the first date to be added
    dateIndex = (orgArr.index).tolist() #extracts the dates of the table (the one indexed by the dates)

    for i in range(len(outArr)): #loops for length of the input array (outArr) as that is how many dates need to be added
        output[i][0] = dateIndex[i + offset] #copies the date to the 1st column
        output[i][1] = outArr[i] #copies the date to the 2nd column
    
    return output

# fastSMA, quicker version of SMA by removing nested 'for' loops. O(n)
def fastSMA(arr, period, dateAdd):
    length = len(arr)

    if length >= period: #if the period > length, there would not be enough values in the array for the function to take an average
        total = length - period + 1 #determine length of the output array
        output = [0 for x in range(total)]

        #this section of code calculates the first rngTotal, and uses it to calculate the first SMA value
        rngTotal = 0
        for j in range(period): #FOR loop to sum up the first "period" number of values
            rngTotal += arr[j]

        output[0] = rngTotal/period #calculates the first average and hence the first SMA value
    
        for k in range(total - 1): #iterates through the rest of the array, subtracting the first value off the running total, and adding the next value
            rngTotal += arr[period + k] - arr[k]
            output[k+1] = rngTotal/period #calculate mean by dividing the sum by the period

        if dateAdd == True: #if dateAdd is true, it pairs up the corresponding date with the SMA value
            return (dateArray(arr, output)) #calls dateArray to pair up dates
        else:
            return output
    else:
        print ("Unable to calculate SMA")

# Exponential Moving Average (EMA) - Same as SMA, but instead is a weighted average method, with more recent days receiving higher weights
def EMA(arr, period, dateAdd):
    length = len(arr)
 
    if length >= period: #if the period > length, there would not be enough values in the array for the function to take an average
        total = length - period + 1 #determine length of the output array
        output = [0 for x in range(total)]
       
        #internal averaging: instead of calling SMA()[0] (which takes a long time as it calculates the whole array) we do 1 single calculation of the average
        initial = 0
        for j in range(period): #sums up first "period"th values
            initial += arr[j]
 
        output[0] = initial/period #takes average and stores it as our first EMA value
 
        #actual calculation
        c = 2/(period + 1) #constant, c used instead, as k is used as FOR loop counter
        for k in range(total - 1):
            #formula: EMAtoday = PRICEtoday*C + EMAyesterday*(1-C)
            output[k + 1] = (arr[period + k]*c) + ((output[k])*(1-c))
 
        if dateAdd == True:
            return (dateArray(arr, output))
        else:
            return output
 
    else:
        print ("Unable to calculate EMA")

#standard deviation - STDDEV calculates the standard deviations of the values in the
def STDDEV(arr, period, dateAdd):
    length = len(arr)
    if length >= period: #if the period > length, there would be not enough values in the array for the function to take an average
        avgArr = fastSMA(arr, period, False) #calls the SMA function to create an array of averages for the algorithm to work with
        total = length - period + 1 #length of the output array
        output = [0 for x in range(total)]

        for i in range(total):
            sumSD = 0
        
            for j in range(period): #FOR loop to obtain mean value, then keeps adding the squared difference of the mean and the value in the window
                mean = avgArr[i]
                sumSD += (arr[i+j] - mean) ** 2
        
            output[i] = math.sqrt(sumSD / period) #square roots the the sum over the period, and appends the result
        
        if dateAdd == True: #pairs dates with corresponding STDDEV values, if dateAdd == True
            return (dateArray(arr, output))
        else:
            return output

    else:
        print("Unable to calculate standard deviation")

# Volatility or Standard Deviation of logaritmic returns
def VOLATILITY(arr, period, dateAdd): 
    total = len(arr) - 1 #length of the output array
    output = [0 for x in range(total)]

    for i in range(total): #calculate the logarithmic return of every day
        output[i] = math.log(arr[i+1]/arr[i])
    
    output = STDDEV(output, period, False) #calls STDDEV to get array of volatility values

    if dateAdd == True: #pairs dates with corresponding VOLATILITY values, if dateAdd == True
        return (dateArray(arr, output))
    else:
        return output

# Volatility or Standard Deviation of logaritmic returns. This function is here for evidence uurposes, not actually
def slowVolatility(arr, period):
  total = len(arr) - 1
  lnArr = [0 for x in range(total)]

  for i in range(total):
    lnArr[i] = math.log(arr[i+1]/arr[i])
  
  avgArr = fastSMA(lnArr, period, False)
  output = [[0,0] for x in range(len(avgArr))]

  index = (arr.index).tolist()
  for i in range(len(avgArr)):
    output[i][0] = index[i + period]

  for i in range(len(avgArr)):
    sumSD = 0
    
    for j in range(period):
      mean = avgArr[i]
      sumSD += (lnArr[i+j] - mean) ** 2
    
    output[i][1] = math.sqrt(sumSD / period)
  
  return output

# MACD - It calculates 12EMA, 26EMA, MACD(12EMA - 26EMA), Signal(9EMA of MACD), Histogram(MACD - Signal)
def MACD(arr, dateAdd, a = 12, b = 26, c = 9): #a: fast, b: slow, c: signal
    length = len(arr)
    if length >= (b + c - 1): # checks if the length of the input array is more than the (“signal” + “slow”), otherwise the EMA function will not work for either the slowArray calculation or the signalArray calculation

        fastArr = EMA(arr, a, False) #calls EMA period 12 of the input array
        slowArr = EMA(arr, b, False) #calls EMA period 26 of the input array
        totalA = len(slowArr)
        offsetA = len(fastArr) - totalA #calculate the first offset so values from fastArray and slowArray that are subtracted, are from the same day
        diffArr = [0 for x in range(totalA)]

        for i in range(totalA):
            diffArr[i] = fastArr[i + offsetA] - slowArr[i] #subtract values of the same day

        sigArr = EMA(diffArr, c, False) #calls EMA period 9 on the MACDArray
        totalB = len(sigArr)
        offsetB = len(diffArr) - totalB #calculate the second offset so values from MACDArray and signalArray that are subtracted, are from the same day
        histArr = [0 for x in range(totalB)] 

        for j in range(totalB):
            histArr[j] = diffArr[j + offsetB] - sigArr[j] #subtract values of the same day

        if dateAdd == True: #pairs up every array here with their corresponding dates
            fastArr = dateArray(arr, fastArr)
            slowArr = dateArray(arr, slowArr)
            diffArr = dateArray(arr, diffArr)
            sigArr = dateArray(arr, sigArr)
            histArr = dateArray(arr, histArr)

        return [fastArr, slowArr, diffArr, sigArr, histArr]
    else:
        print("Unable to calculate MACD")

# Relative Strength Index calculates whether a stock is overbought, oversold, or neither
def RSI(arr, dateAdd):
    length = len(arr)
    if length >= 15: #cannot calculate RSI for arrays with length 14 or less, as the coming SMA functions require 14 values, and because we are calculating changes beforehand, we need 1 more value, making 15
        total = length - 1
        upArr = [0 for x in range(total)]
        downArr = [0 for x in range(total)]
        for i in range(total):
            change = arr[i+1] - arr[i] #calculate change of consecutive values in the array

            if change >= 0: #if the change is positive, we append the change to the array of positive changes (upArr), and append 0 to downArr
                upArr[i] = change
                downArr[i] = 0
            else: #if the change is negative, we append the absolute value of change to the array of negative changes (upArr), and append 0 to upArr
                upArr[i] = 0
                downArr[i] = abs(change)

        upAvgArr = fastSMA(upArr, 14, False) #gets the averages of the upAvgArr with period 14
        downAvgArr = fastSMA(downArr, 14, False) #gets the averages of the downAvgArr with period 14
        lengthB = len(upAvgArr) #gets the length of the upAvgArr so we can determine the size of the output array 
        output = [0 for x in range(lengthB)]
        
        for j in range(lengthB):
            output[j] = 100 - 100/(1+(upAvgArr[j]/downAvgArr[j])) #the RSI formula calculation

        if dateAdd == True: #pairs dates with corresponding RSI values, if dateAdd == True
            return (dateArray(arr, output))
        else:
            return output
    else:
        print("Cannot calculate RSI")

#Calculates percentage changes from value to value
def PCT(arr, dateAdd): 
    length = len(arr)
    if length > 1: #cannot calculate percentage change for an array with one value or less, because we need at least two values
        total = length - 1 #length of output array is always going to be one less than the input array, as we can’t calculate the percentage for the first day as we no value for the day before that
        output = [0 for x in range(total)]
        for i in range(total):
            output[i] = 100*(arr[i+1] - arr[i]) / abs(arr[i]) #calculating percentage change

        if dateAdd == True: #pairs dates with corresponding PCT values, if dateAdd == True
            return (dateArray(arr, output))
        else:
            return output
    else:
        print("Unable to calculate percentage change")

#calculates market capitalisation: price times shares
def MKTCAP(price, shares):
    return (price*shares)

# calculates earnings per share, by dividing the total profit, by the number of shares
def EPS(profit, shares):
    return (profit/shares)

#calculates prices per earnings, by calculating earnings per share (calling EPS), and dividing profit by the EPS
def PER(price, profit, shares):
    eps = EPS(profit, shares)
    return (price/eps)

#returns an evaluative metric based on the indicators SMA, EMA, RSI and MACD, to generate a buy, sell or neutral signal
def techEval(arr):
    counter = 0
    SMA10 = fastSMA(arr[-10:],10,False) #gets the past 10 day average
    SMA50 = fastSMA(arr[-50:],50,False) #gets the past 50 day average
    SMA100 = fastSMA(arr[-100:],100,False) #gets the past 100 day average
    EMA10 = EMA(arr,10,False) #gets the EMA value of period 10 for today
    EMA50 = EMA(arr,50,False) #gets the EMA value of period 50 for today
    EMA100 = EMA(arr,100,False) #gets the EMA value of period 100 for today
    RSICalc = RSI(arr[-15:],False) #gets todays RSI value
    MACDCalc = MACD(arr,False) #calculates the MACD

    #For the averages, if the current average value is below today's closing price, it indicates that the price is above and is going up, and vice versa
    #If the average is below today's price, then a buy signal is generated by adding 0.5 to the counter, otherwise a sell signal is generated
    #The weightings of the signals is half of that of RSI and MACD, as sometimes these signals are not accurate (especially during times of high volatility)
    closePrice = arr[-1] #last value of the array (which is the historical closing prices array)
    
    if SMA10[0] < closePrice:
        counter += 0.5
    else:
        counter += -0.5
    if SMA50[0] < closePrice:
        counter += 0.5
    else:
        counter += -0.5
    if SMA100[0] < closePrice:
        counter += 0.5
    else:
        counter += -0.5
    if EMA10[-1] < closePrice:
        counter += 0.5
    else:
        counter += -0.5
    if EMA50[-1] < closePrice:
        counter += 0.5
    else:
        counter += -0.5
    if EMA100[-1] < closePrice:
        counter += 0.5
    else:
        counter += -0.5

    #if RSI is below 25, then it indicates that the stock is oversold, meaning it is undervalued, therefore it has the possibility of gaining value. Therefore we add a buy signal by adding one to the counter
    #if RSI is above 75, then it indicates that the stock is overbought, meaning it is overvalued, therefore it has the possibility of losing value. Therefore we add a sell signal by subtracting one off the counter
    if RSICalc[0] < 25:
        counter += 1
    elif RSICalc[0] > 75:
        counter += -1

    #if today's MACD value is above today's signal value, then it indicates a positive trend, so we add a buy signal by adding one to the counter
    #if today's MACD value is below today's signal value, then it indicates a negative trend, so we add a sell signal by subtracting one off the counter
    if MACDCalc[2][-1] > MACDCalc[3][-1]:
        counter += 1
    else:
        counter += -1

    return counter