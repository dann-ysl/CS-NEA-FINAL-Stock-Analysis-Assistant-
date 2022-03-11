#merge sorts the values and returns the original indices along with the sorted value
def mergeSortIndex(arr):

    length = len(arr) #taking the length of how many rows there are in the array
    if length > 1: #Checks if the length is greater than 1, if not, the list contains just one element meaning it is ready to be sorted
        #SPLITTING PROCESS
        if length % 2 == 0: #This if statement checks if the length is an odd number or even number so that we get an integer value for the midpoint “mid”
            mid = int(length/2)
        else:
            mid = int((length - 1)/2)

        #This piece of code splits the array in half by splicing the array and calls the function recursively where the stop case is the length of the array being one
        leftArr = mergeSortIndex(arr[0:mid])
        rightArr = mergeSortIndex(arr[mid:length])

        #MERGING PROCESS
        #These variables are counters that help sort the values in the split arrays
        i = 0
        j = 0
        k = 0

        l = len(leftArr)
        r = len(rightArr)
        output = [0 for x in range(l+r)]

        while (i < l) and (j < r): #/stops when i reaches l, as there are no more values left in the left array to be sorted, likewise for when j reaches r.
            if leftArr[i][1] < rightArr[j][1]: #compares the values in the second column, as that is where the values are stored. If the value in leftArray is less than the value in the rightArray, it will place the value in the leftArray first in our new output array
                output[k] = leftArr[i] #copies the original row over
                i += 1 #1 is added to i, as we have already compared the “i”th value, so we compare the next value in the leftArray
            else:
                output[k] = rightArr[j] #copies the original row over
                j += 1 #1 is added to j, as we have already compared the “j”th value, so we compare the next value in the rightArray
            
            k += 1 #1 is added to k, so that we have a new spot in the output array which is blank and we can add to
        
        while i < l: #this WHILE loop is here to catch and sort all the very last values which have been unsorted, when the above WHILE loop stopped
            output[k] = leftArr[i] #copies the original row over
            i += 1
            k += 1
        
        while j < r: #same purpose as the above WHILE loop
            output[k] = rightArr[j] #copies the original row over
            j += 1
            k += 1

        return output #returns a sorted array, if it returns an array that is part of the original array, it returns it to the function that called it, in the call stack. If this was the final function in the call stack, the function will return the whole sorted array.
    
    else:
        return arr #returns the array of size 1, splitting is fully done at this stage

#sortColumn sorts a 2D array, based on the values in the column specified in the parameter
def sortColumn(arr, column):
    length = len(arr) #length of rows

    output = [0 for x in range(length)]
    sortArr = [[0,0] for x in range(length)]

    for i in range(length):#extracts the values from the column to a new intermediary array, where each value (column 2) is assigned its original index (column 1)
        sortArr[i][0] = i #assign original index
        sortArr[i][1] = arr[i][column] #copy value from specified column

    indexArr = mergeSortIndex(sortArr) #performs merge sort on the array of values, it will return an array sorted by value, where we only need the original index assigned to that value, so that we can sort the rows

    for j in range(length):
        index = indexArr[j][0] #takes the original index of the sorted array (indexArr)
        output[j] = arr[index] #copies the index'th row to the new output array
    
    return output

#takes in the input array (should be one-dimensional) and lb, which is the lower bound value, and ub, the upper bound value
def linearSearchRange(arr, lb, ub):

    output = [0,0] #2 item array, 1st item storing index of lower bound, 2nd storing index of upper bound
    length = len(arr)
    leftCounter = 0 #leftCounter stores the index of the input array value that we are checking against the lower bound “lb”
    leftCheck = False #boolean variable that is True when value being checked is greater than or equal to the lower bound "lb"
    rightCounter = (length - 1) #rightCounter stores the index of the input array value that we are checking against the upper bound “ub”. It initialises with the very last index of the input array
    rightCheck = False #boolean variable that is True when value being checked is lower than or equal to the upper bound "ub"
  
    while leftCheck == False: #when this WHILE loop finds a value which is more than or equal to the lower bound “lb”, the WHILE loop will not run anymore and it will store the index of the that value in output[0]
        if leftCounter < length: #leftCounter has to be less than the length, otherwise we would be comparing values that don’t exist
            if float(lb) <= float(arr[leftCounter]): #checking to see if the current value is more than the lower bound
                output[0] = leftCounter #stores the index of the lowest possible value in the array which is bigger than the lower bound
                leftCheck = True #exits the while loop
            else:
                leftCounter += 1 #1 is added to leftCounter, so in the next WHILE loop, we check the next value in the array
        else: #if the leftCounter does overtake the whole length of the array, it should stop and return the leftCounter
            output[0] = leftCounter
            leftCheck = True
 
    while rightCheck == False: #when this WHILE loop finds a value which is less than or equal to the upper bound “ub”, the WHILE loop will not run anymore and it will store the index of the that value in output[1]
        if rightCounter >= 0: #rightCounter can not be negative, otherwise it would be searching for negative indices, which don’t exist
            if float(ub) >= float(arr[rightCounter]): #checking to see if the current value is less than the upper bound
                output[1] = rightCounter #stores the index of the highest possible value in the array which is lower than the upper bound
                rightCheck = True #exits the while loop
            else:
                rightCounter += -1 #1 is subtracted off leftCounter, so in the next WHILE loop, we check the previous value in the array
        else: #if the rightCounter goes past zero, it can't fetch a negative index from an array, so the while loop should stop when it reaches zero
            output[1] = -1
            rightCheck = True

    return output

#searches and returns a list of stocks from the input array, which meets the criteria of the filterArray
def search(arr, filterValue):

    for i in range(len(filterValue)): #FOR loop will initially deal with the whole input array, but as it iterates again, it will do so with a smaller (filtered) array, so the FOR loop gets faster and faster every iteration, as there are less values in the filtered array to process
        if filterValue[i][0] != "" and filterValue[i][1] != "": #if the certain value in the filter array is blank, it indicates that we don’t need to filter it by that category filter, so it skips and goes to next iteration, checking if the next values are blank as well
            length = len(arr) #gets rows of the array, so we know how many values to copy over
            sortArr = sortColumn(arr, (i+3)) #calls the sort by column method, so we get an array that is sorted by the column specified. This is so we perform the linear search range function, as it is sorted
            valueArr = [0 for x in range(length)]
            for j in range(length): #copies every value from the specified column to an intermediary array called “valueArr”
                valueArr[j] = sortArr[j][i+3]

            indexArr = linearSearchRange(valueArr, filterValue[i][0], filterValue[i][1]) #calls linearSearchRange to find indices of lower bound and upper bound value to filter the original record by the specific column
            arr = sortArr[indexArr[0]:(indexArr[1]+1)] #copies part of the array which met the corresponding criteria. It uses the result of the linearSearchRange to retrieve the indices for which we need to restrict the old array
    
    return arr