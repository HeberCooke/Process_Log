"""
Heber Cooke 1/23/2020
python project

"""

import psutil
from tkinter import *
import time
from log import Log
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import csv


def main():

    timeSelect = ""
    selection1 = ""
    selection2 = ""
    selection3 = ""

    global tm
    tm = 5
    global count
    count = 1
    global fileName 



    # Selects the pid info from main list box or the list box from top 3
    def selectPid():
        #print(listBox.get(ACTIVE))
        global count

        if  count == 1:
            lbl1["text"]= listBox.get(ACTIVE) 
            count += 1   
            return
        elif count == 2:
            lbl2['text'] = str(listBox.get(ACTIVE))        
            count += 1
            return
        elif count == 3:
            lbl3['text'] = str(listBox.get(ACTIVE))
            count = 1
            return

    def timeOne():
        global tm
        print("Time set to 1 min")
        lbl4['text']= "Time set to 1 min"
        tm = 60
        
    def timeThirty():
        global tm
        print("time set to 30 min")
        tm = 1800
        lbl4['text']= "Time set to 30 min"
        

    def timeOneHr():
        global tm
        print("Time set to 1 hour")
        tm = 3600
        lbl4['text']= "Time set to 1 hour"
        


    def start1():
        global tm
        global fileName

        pid1 = int(lbl1['text'].split()[0])
        pid2 = int(lbl2['text'].split()[0])
        pid3 = int(lbl3['text'].split()[0])
    
        log = Log(pid1, pid2, pid3, tm )
        log.makeFile()
        time.sleep(1)
        fileName = log.getFileName()

    def makeChart():
        global fileName
        if fileName:

            plt.style.use('seaborn')
            column1 = []
            column2 = []
            column3 = []
            time = []
            count = 1
            with open(fileName) as f:
                for row in csv.reader(f):
                    if count == 1:
                        name1 = row[0]
                        name2 = row[2]
                        name3 = row[4]
                        count = 0
                    else:
                        column1.append((int(row[0]) // 1000) // 1000)
                        column2.append((int(row[2]) // 1000) // 1000)
                        column3.append((int(row[4]) // 1000) // 1000)

                        # column1.append(row[0])#
                        # column2.append(row[2])#int(row[2]) / 1000
                        # column3.append(row[4])#int(row[4]) / 1000
                        time.append(row[6]) # 6 is the 

            # Changes the window size
            fig_size = plt.rcParams['figure.figsize']
            fig_size[0] = 12
            fig_size[1] = 6
            plt.rcParams['figure.figsize']= fig_size
            #print(plt.rcParams.get('figure.figsize'))

            plt.plot(time,column1,color='red', label=name1,marker='.')
            plt.plot(time,column2,color='b', label=name2, marker='.')
            plt.plot(time,column3,color='g', label=name3, marker='.')
            plt.ylabel('Megabytes')
            plt.xlabel('Time')
            plt.title(name1+','+name2+','+name3)
            
            plt.xticks(np.arange(0,len(time), step=2)) # steps the x axis date to 3
            #plt.yticks(np.arange(0, max(column1), step=.5))
            plt.grid(True)

            #plt.grid(b=True, which='major', color='k', linestyle='-')
            #plt.grid(b=True, which='minor', color='k', linestyle='-', alpha=0.08)#
            plt.minorticks_on()
            #plt.legend(loc="best")
            plt.legend(bbox_to_anchor=(0, 1.02,1,0.2), loc='lower left')
            plt.xticks(rotation=30)
            plt.tight_layout()
            plt.show()

    # Main window
    window = Tk() 
    window.title("TSK-Log")
    window.configure(background="black")
    window.geometry("730x605") # Height then width
    window.resizable(0,0) # not resizable
    window.config(padx=5)
    menuBar = Menu(window)
    
    menuBar.add_command(label="Select PID", command= selectPid)
    menuBar.add_command(label="1Min", command=timeOne)
    menuBar.add_command(label="30Min", command=timeThirty)
    menuBar.add_command(label="1Hr", command=timeOneHr)
    menuBar.add_command(label='Start',command=start1)

    # Process window
    frameLblPid = LabelFrame(window, text="PROCESSES", fg='blue',bg='black')
    frameLblPid.config(font=('bold'), padx=5)
    frameLblPid.grid(row=0,column=0)
    # Info window
    infoFrame = LabelFrame(window, text="INFO", fg='blue', bg='black')
    infoFrame.config(font='bold',padx=5, width = 300, height = 600)
    infoFrame.grid(row=0, column = 1, sticky= N+S+E+W)
    # labels for window
    cpuP ="%-5s%-15s" % (str(psutil.cpu_percent(interval=1)),"% CPU")
    cpuPercent = Label(infoFrame, text=cpuP, bg='black',fg='blue',font=12)
    cpuPercent.grid(row=6, column= 2)

    mem ="%-5s%-15s" %( str(psutil.virtual_memory()[2]) ,"% Virtual Memory")
    memLabel = Label(infoFrame, text=mem, bg='black',fg='blue',font=12 )
    memLabel.grid(row=7, column= 2)

    scrollbar = Scrollbar(frameLblPid, orient=VERTICAL)
    scrollbar.grid(row=0, column=1, sticky= N+S)

    listBox = Listbox(frameLblPid,selectmode=SINGLE, yscrollcommand=scrollbar.set)
    listBox.config(height=26,width=40, font=('Times',14), bg="black", fg='white')
    listBox.grid(row=0,column=0)
    scrollbar['command'] = listBox.yview


    # This gets the processes that use the most memory
    p = ([(p.pid, p.info) for p in sorted(psutil.process_iter(attrs=['name', 'memory_percent']), key=lambda p: p.info['memory_percent'])][-4:])  
    a, b, c, d = p
    top3Name = a[1]['name']
    top3Pid = a[0]
    top3Mem = str(round(a[1]['memory_percent'],2))  
    top2Name = b[1]['name']
    top2Pid = b[0]
    top2Mem = str(round(b[1]['memory_percent'],2)) 
    top1Name = c[1]['name']
    top1Pid = c[0]
    top1Mem = str(round(c[1]['memory_percent'],2))    
    top0Name = d[1]['name']
    top0Pid = d[0]
    top0Mem = str(round(d[1]['memory_percent'],2)) 
 
    infoLabel = Label(infoFrame, text="Top CPU % Use", font=('Times',14), bg="black", fg='white')
    infoLabel.grid(row=0, column=2)

    lblTop1 = Label(infoFrame, text="%-8s%-10s%-30s" % (top0Mem, top0Pid, top0Name),font=('Times',14), bg="black", fg='white')
    lblTop1.grid(row=1,column=2)
    lblTop2 = Label(infoFrame, text="%-8s%-10s%-30s" % (top1Mem, top1Pid, top1Name),font=('Times',14), bg="black", fg='white')
    lblTop2.grid(row=2,column=2)
    lblTop3 = Label(infoFrame, text="%-8s%-10s%-30s" % (top2Mem, top2Pid, top2Name),font=('Times',14), bg="black", fg='white')
    lblTop3.grid(row=3,column=2)
    lblTop4 = Label(infoFrame, text="%-8s%-10s%-30s" % (top3Mem, top3Pid, top3Name),font=('Times',14), bg="black", fg='white')
    lblTop4.grid(row=4,column=2)


    labelFrameSelection = LabelFrame(infoFrame, text = "Selected", fg='blue',bg='black')
    labelFrameSelection.config(font='bold', padx=5, width =280 , height =200 )
    labelFrameSelection.grid(row=5, column= 2, sticky= N+E+W)

    # labels to show selections 
    lbl1 = Label(labelFrameSelection,text='NONE', textvariable= selection1, font=('Times',14), bg="black", fg='white')
    lbl1.pack()
    lbl2 = Label(labelFrameSelection,text='NONE', textvariable= selection2, font=('Times',14), bg="black", fg='white')
    lbl2.pack()
    lbl3 = Label(labelFrameSelection,text='NONE', textvariable= selection3, font=('Times',14), bg="black", fg='white')
    lbl3.pack()
    lbl4 = Label(labelFrameSelection, text=timeSelect,font=('Times', 14), bg='black', fg='white')
    lbl4.pack()

    # Process iterator
    processList = psutil.process_iter(attrs=['pid','name'])
    # Put Items in the window
    for proc in processList:
        try:
            processName = proc.name().strip()
            processId = proc.pid
            listBox.insert(END," %-15s%-20s"% ( str(processId),processName))
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    

    # Button to show current chart
    btn = Button(infoFrame, text="Show Chart",width=10, height=5,font=("Times",14),fg='blue', command=makeChart)
    btn.grid(row=8, column=2, pady=20,padx=10, sticky=N+E+S+W)

    listBox.activate(0)
    window.config(menu=menuBar)
    window.mainloop()
    

main()