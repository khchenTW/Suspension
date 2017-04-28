import matplotlib
matplotlib.use('Agg')
import matplotlib.patches as mpatches
import random
import math
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats.mstats import gmean

x1 = []
y1 = []
x2 = []
y2 = []
x3 = []
y3 = []
x4 = []
y4 = []
x5 = []
y5 = []
x6 = []
y6 = []

'''
f2 = open(var1+"'1'.txt", 'r')
f3 = open(var1+"'2'.txt", 'r')
f4 = open(var1+"'3'.txt", 'r')
f5 = open(var1+"'4'.txt", 'r')
f6 = open(var1+"'5'.txt", 'r')
'''
resTotal1 = []
resTotal2 = []
resTotal3 = []
resTotal4 = []
resTotal5 = []
resTotal6 = []
target = "output/Results-tasks10_stypeS_"
g = 6
def fileInput(var1, group):
    fileidx = 0
    utililist = []
    while fileidx < group:
        tmpUtil = []
        f1 = open(var1+str(fileidx)+".txt", 'r')
        count = -1
        flag = 0
        tmpRes1 = []
        tmpRes2 = []
        tmpRes3 = []
        tmpRes4 = []
        tmpRes5 = []
        tmpRes6 = []

        for line in f1:
            if count == -1:
                #filename to get utilization:
                filename = line.split('_')
                #print filename
                tmpUtil.append(int(filename[1]))
                pass

            #Content to get Arithmetic mean and Gmean
            if 0 <count < 35:
                if count%2==1:
                    strline = line.replace('[','')
                    strline = strline.replace(']','')
                    strline = strline.replace('\n','')
                    strline = strline.split(',')
                    #strline[x] x = 0-16
                    #[ILPcarry, ILPblock, ILPjit, Inflation, ILPbaseline, Combo, TDA, TDAcarry, TDAblock, TDAjit, TDAjitblock, TDAmix, CTbaseline, CTcarry, CTblock, CTjit, CTmix]
                    #ILPbaseline
                    tmpRes1.append(int(strline[4]))
                    #CTBaseline
                    tmpRes2.append(int(strline[12]))
                    #TDA
                    tmpRes3.append(int(strline[6]))
                    #CTmix
                    tmpRes4.append(int(strline[16]))
                    #TDAmix
                    tmpRes5.append(int(strline[11]))
                    #ILPjit
                    tmpRes6.append(int(strline[2]))

            if count == 35:
                '''
                #print 'Gmean:'+line
                strline = line.replace('[','')
                strline = strline.replace(']','')
                strline = strline.replace('\n','')
                strline = strline.split(',')
                print strline
                #strline[x] x = 0-16
                y1.append(float(strline[0]))
                '''
                count = -1
                continue
            count += 1
        f1.close()
        resTotal1.append(tmpRes1)
        resTotal2.append(tmpRes2)
        resTotal3.append(tmpRes3)
        resTotal4.append(tmpRes4)
        resTotal5.append(tmpRes5)
        resTotal6.append(tmpRes6)
        utililist.append(tmpUtil)
        fileidx += 1
    return utililist
    #print resTotal6

def getResPerUtili(res, numinSets): #work for tasks 10 an 20
    utililist = []
    readyres = [[] for i in range(8)]
    count = 0
    for ind, i in enumerate(res): #each file
        #print ""
        #print i
        #print len(i)
        tmp = []
        icount = 0
        for j in i: #every 17 input for each utilization
            tmp.append(j)
            count+=1
            #print icount
            if count > numinSets-1:
                readyres[icount]=readyres[icount]+tmp
                tmp = []
                count = 0
                icount = (icount+1)%8
        icount = 0
        count = 0

    for i in readyres:
        #print " "
        #print i
        utililist.append(i)
    return utililist
    #print readyres[0]
    #print len(readyres[0])

utili = fileInput(target, g)
for i in utili[0]:
    x1.append(i)
    x2.append(i)
    x3.append(i)
    x4.append(i)
    x5.append(i)
    x6.append(i)
#after this, 6 sets of methods are prepared
def wayofMean(way):
    for i in getResPerUtili(resTotal1,17): #when g = 6
        y1.append(way(i))
    for i in getResPerUtili(resTotal2,17): #when g = 6
        y2.append(way(i))
    for i in getResPerUtili(resTotal3,17): #when g = 6
        y3.append(way(i))
    for i in getResPerUtili(resTotal4,17): #when g = 6
        y4.append(way(i))
    for i in getResPerUtili(resTotal5,17): #when g = 6
        y5.append(way(i))
    for i in getResPerUtili(resTotal6,17): #when g = 6
        y6.append(way(i))
wayofMean(gmean)

#print x1, y1

#getResPerUtili(resTotal1,100) #g = 1

'''
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
'''
name='test'
#repr
fileName = 'Results-tasks10_stype_S'
folder = 'plots/'
# plot in pdf
pp = PdfPages(folder + fileName + '.pdf')
title = 'Gmean-10Tasks-S'
plt.title(title, fontsize=20)
plt.grid(True)
#plt.ylabel('Geometric Mean', fontsize=20)
#plt.xlabel('Approaches($U^*$)', fontsize=20)
ax = plt.subplot()
ax.tick_params(axis='both', which='major',labelsize=16)
ax.set_ylabel("Geometric Mean", size=20)
ax.set_xlabel("Utilization (%)", size=20)

'''
labels = ('CPRTA','EPST-K', 'CRPTA','EPST-K')
'''
marker = itertools.cycle(('D', 'd', 'o', 's', 'v'))

try:
    ax.plot( x1, y1, '-', marker = marker.next(), label='ILPBase', linewidth=2.0)
    ax.plot( x2, y2, '-', marker = marker.next(), label='CTBase', linewidth=2.0)
    #ax.plot( x3, y3, '-', marker = marker.next(), label='TDA', linewidth=2.0)
    #ax.plot( x4, y4, '-', marker = marker.next(), label='CTmix', linewidth=2.0)
    ax.plot( x5, y5, '-', marker = marker.next(), label='TDAmix', linewidth=2.0)
    ax.plot( x6, y6, '-', marker = marker.next(), label='ILPcombo', linewidth=2.0)
except ValueError:
    print "ValueError"

#ax.vlines(0.5, 0, 1, transform=ax.transAxes )
#ax.text(0.35, 0.04, "$U^*=60\%$", transform=ax.transAxes, size=16 )
#ax.text(0.85, 0.04, "$U^*=70\%$", transform=ax.transAxes, size=16 )

ax.legend(loc=0)
figure = plt.gcf()
figure.set_size_inches([10, 5])

pp.savefig()
plt.clf()
plt.show()
pp.close()
