"""
log.py
class Log
This class starts a new thread with a loop to log the information on a set time interval.

"""


import psutil
import time
import datetime
from threading import Thread

class Log(Thread):

    fileName = ''


    def __init__(self,pid1, pid2, pid3, time):
        Thread.__init__(self)
        self.waittime = time # wait time
        self.pid1 = pid1
        self.pid2 = pid2
        self.pid3 = pid3

    def getFileName(self):
        global fileName
        return fileName

    def makeFile(self):
        #t = Thread()
        self.start()
        print("Thread started")


    def run(self):
        global fileName

        print("Started run")
        self.firstTimeFileOpen = True

        process1 = psutil.Process(self.pid1)
        process2 = psutil.Process(self.pid2)
        process3 = psutil.Process(self.pid3)

        l1 = list(process1.as_dict(attrs=["name"]).values())
        l2 = list(process2.as_dict(attrs=["name"]).values())
        l3 = list(process3.as_dict(attrs=["name"]).values())
        
        self.p1Name = str(l1[0])
        self.p2Name = str(l2[0])      
        self.p3Name = str(l3[0])

        
        while True:
            # Reseting the pid from the name if necessary
            if not psutil.pid_exists(self.pid1):
                time.sleep(5)
                for i in psutil.process_iter(attrs=['name','pid']):
                    if i.name() == self.p1Name:
                        pid1 = i.pid
                        process1 = psutil.Process(pid1)

            if not psutil.pid_exists(self.pid2):
                time.sleep(5)
                for i in psutil.process_iter(attrs=['name','pid']):
                    if i.name() == self.p2Name:
                        pid2 = i.pid
                        process2 = psutil.Process(pid2)

            if not psutil.pid_exists(self.pid3):
                time.sleep(5)
                for i in psutil.process_iter(attrs=['name','pid']):
                    if i.name() == self.p3Name:
                        pid3 = i.pid
                        process3 = psutil.Process(pid3)


            cpuUse1 = process1.memory_percent()
            cpuUse2 = process2.memory_percent()
            cpuUse3 = process3.memory_percent()


            P1Mem = process1.memory_info()[len(process1.memory_info()) -1]
            P2Mem = process2.memory_info()[len(process2.memory_info()) -1]
            P3Mem = process3.memory_info()[len(process3.memory_info()) -1]

            fileName = str(self.p1Name) + "_"+ str(self.p2Name)+"_"+str(self.p3Name)+".txt"
            # CVS file
            with open(fileName, "a") as files:
                ftime = datetime.datetime.now()
                fftime = ftime.strftime('%m/%d/%Y %H:%M:%S') # Format the date
                if self.firstTimeFileOpen:
                    files.write(str(self.p1Name) + ',CPU%'+',' +str(self.p2Name) + ",CPU%"+',' + str(self.p3Name) + ",CPU%"+',' +"Time")
                    files.write('\n')
                    self.firstTimeFileOpen = False
                cvS = str(P1Mem) + "," + str(cpuUse1) + "," +  str(P2Mem) + "," + str(cpuUse2) +"," + str(P3Mem)+  "," + str(cpuUse3) +  "," +  str(fftime) +"\n"
                files.write(cvS)


            time.sleep(self.waittime) # clock time