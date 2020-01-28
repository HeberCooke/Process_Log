import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np
import csv


plt.style.use('seaborn')

def main():
    
    column1 = []
    column2 = []
    column3 = []
    time = []
    count = 1
    with open('C.txt') as f:
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


main()