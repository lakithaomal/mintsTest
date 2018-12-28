# from datetime import timezone
import time
import os
import datetime
# import numpy as np
# import pickle
# from skimage import io, color
# import cv2
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
import serial
ser1 =  serial.Serial('/dev/ttyACM1', 9600)
# ser2 =  serial.Serial('/dev/ttyACM0', 9600)

# ser1.flushInput()
def main():


    print("Mints - Multi-scale Integrated Sensing and Simulation")
    # global ser1
    utcnow = datetime.datetime.utcnow()


    sendData("-mints:time:"+ str(utcnow.year).zfill(4) +str(utcnow.month).zfill(2)+str(utcnow.day).zfill(2)+str(utcnow.hour).zfill(2)+str(utcnow.minute).zfill(2)+str(utcnow.second).zfill(2)+"-")

    # ser1 =  serial.Serial('/dev/ttyACM0', 9600)
    while(True):
        # command = input("Print Command: ")
        #
        # sendData("-mints:HTU21D-")
        # #
        sendData("-mints:BMP280-")
        time.sleep(2)
        sendData("-mints:HTU21D-")
        time.sleep(2)
        # # print("Command Read: " + command)







def timeTaken(message,start):
    print(message+str(time.time()-start)+' Seconds')

def gzExtractor(gzLocation):
    os.system('gzip -f ' +gzLocation)

def sendData(data):
    ser1.write(data.encode())

if __name__ == "__main__":
   main()
