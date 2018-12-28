# import serial
# ser = serial.Serial('/dev/ttyACM3')
import serial
import datetime
import os
import csv
dataFolder = "/home/lakitha/Documents/mintsData/"

def main():

    ser = serial.Serial(
        port='/dev/ttyACM0',\
        baudrate=9600,\
        parity  =serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)

    print("connected to: " + ser.portstr)

    #this will store the line
    line = []

    while True:
        for c in ser.read():
            line.append(chr(c))
            if chr(c) == '-':
                dataString     = (''.join(line))
                dataStringPost = dataString.replace('-', '')
                dataSplit(dataStringPost,datetime.datetime.now())
                line = []
                break

    ser.close()
        # if chr(c) == '-':
        #     print(''.join(line))

def dataSplit(dataString,dateTime):
    dataOut   = dataString.split('!')
    if(len(dataOut) == 2):
        tag       = dataOut[0]
        dataQuota = dataOut[1]
        if(tag.find("#mintsO")==0):
            sensorSplit(dataQuota,dateTime)

def sensorSplit(dataQuota,dateTime):
    dataOut    = dataQuota.split('>')
    if(len(dataOut) == 2):
        sensorID   = dataOut[0]
        sensorData = dataOut[1]
        sensorSend(sensorID,sensorData,dateTime)
        # print("Sensor ID  : "+sensorID)
        # print("Sensor Data: "+sensorData)
        # print("Date Time : " +str(dateTime))



def sensorSend(sensorID,sensorData,dateTime):
    if(sensorID=="HTU21D"):
        HTU21DWrite(sensorData,dateTime)
    if(sensorID=="BMP280"):
        BMP280Write(sensorData,dateTime)
    if(sensorID=="GAS1"):
        GAS1Write(sensorData,dateTime)

def HTU21DWrite(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "HTU21D"
    if(len(dataOut) == 2):
        sensorDictionary = {
                "DateTime"           : str(dateTime),
        		"Temperature" :dataOut[0],
            	"Humdity"     :dataOut[1],
        	     }

    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    # print(writePath)
    print(sensorDictionary)
#
def BMP280Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "BMP280"
    if(len(dataOut) == 2):
        sensorDictionary = {
                "DateTime"           : str(dateTime),
        		"Temperature" :dataOut[0],
            	"Pressure"     :dataOut[1],
        	     }

    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    # print(writePath)
    print(sensorDictionary)


def GAS1Write(sensorData,dateTime):
    dataOut    = sensorData.split(':')
    sensorName = "GAS1"
    if(len(dataOut) == 4):
        sensorDictionary = {
                "DateTime"   : str(dateTime),
        		"NO2"  :dataOut[0],
            	"SO2"  :dataOut[1],
                "O3"   :dataOut[2],
                "C02"  :dataOut[3],
        	     }
    #Getting Write Path
    writePath = getWritePath(sensorName,dateTime)
    exists = directoryCheck(writePath)
    writeCSV2(writePath,sensorDictionary,exists)
    # print(writePath)
    print(sensorDictionary)

def writeCSV2(writePath,sensorDictionary,exists):
    keys =  list(sensorDictionary.keys())
    with open(writePath, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        print(exists)
        if(not(exists)):
            writer.writeheader()
        writer.writerow(sensorDictionary)



def getWritePath(labelIn,dateTime):
    writePath = dataFolder +str(dateTime.year) + "/" + str(dateTime.month) +"/mintsO"+ labelIn + str(dateTime.year) + str(dateTime.month) + str(dateTime.day) + ".csv"
    return writePath;

def getListDictionaryFromPath(dirPath):
    print("Reading : "+ dirPath)
    reader = csv.DictReader(open(dirPath))
    reader = list(reader)

def fixCSV(keyIn,valueIn,currentDictionary):
    editedList       = editDictionaryList(currentDictionary,keyIn,valueIn)
    return editedList

def editDictionaryList(dictionaryListIn,keyIn,valueIn):
    for dictionaryIn in dictionaryListIn:
        dictionaryIn[keyIn] = valueIn

    return dictionaryListIn

def getDateDataOrganized(currentCSV,nodeID):
    currentCSVName = os.path.basename(currentCSV)
    nameOnly = currentCSVName.split('-Organized.')
    dateOnly = nameOnly[0].split(nodeID+'-')
    print(dateOnly)
    dateInfo = dateOnly[1].split('-')
    print(dateInfo)
    return dateInfo


def getFilePathsforOrganizedNodes(nodeID,subFolder):
    nodeFolder = subFolder+ nodeID+'/';
    pattern = "*Organized.csv"
    fileList = [];
    for path, subdirs, files in os.walk(nodeFolder):
        for name in files:
            if fnmatch(name, pattern):
                fileList.append(os.path.join(path, name))
    return sorted(fileList)


def getLocationList(directory, suffix=".csv"):
    filenames = listdir(directory)
    dateList = [ filename for filename in filenames if filename.endswith( suffix ) ]
    return sorted(dateList)


def getListDictionaryCSV(inputPath):
    # the path will depend on the node ID
    reader = csv.DictReader(open(inputPath))
    reader = list(reader)
    return reader

def writeCSV(reader,keys,outputPath):
    directoryCheck(outputPath)
    csvWriter(outputPath,reader,keys)

def directoryCheck(outputPath):
    exists = os.path.isfile(outputPath)
    directoryIn = os.path.dirname(outputPath)
    if not os.path.exists(directoryIn):
        os.makedirs(directoryIn)
    return exists

def csvWriter(writePath,organizedData,keys):
    with open(writePath,'w') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(organizedData)


def gainDirectoryInfo(dailyDownloadLocation):
    directoryPaths = []
    directoryNames = []
    directoryFiles = []
    for (dirpath, dirnames, filenames) in walk(dailyDownloadLocation):
        directoryPaths.extend(dirpath)
        directoryNames.extend(dirnames)
        directoryFiles.extend(filenames)

    return directoryPaths,directoryNames,directoryFiles;

if __name__ == "__main__":
   main()
