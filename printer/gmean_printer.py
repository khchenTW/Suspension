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

var1 = "Results-dtasks10_stypeS_"
f1 = open(var1+"0.txt", 'r')
'''
f2 = open(var1+"'1'.txt", 'r')
f3 = open(var1+"'2'.txt", 'r')
f4 = open(var1+"'3'.txt", 'r')
f5 = open(var1+"'4'.txt", 'r')
f6 = open(var1+"'5'.txt", 'r')
'''
for line in f:
    print line
print "Test"
'''
for line in lines:
    print line
    p = line.split()
    if p:
        x1.append(float(p[0]))
        y1.append(float(p[1]))
'''
'''
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
name='test'
#repr
fileName = 'Results-tasks10_stype_S'
folder = 'plots/'
# plot in pdf
pp = PdfPages(folder + fileName + '.pdf')
title = 'Gmean-10Tasks-S'
plt.title(title, fontsize=20)
plt.grid(True)
plt.ylabel('Geometric Mean', fontsize=20)
#plt.xlabel('Approaches($U^*$)', fontsize=20)
ax = plt.subplot()
ax.tick_params(axis='both', which='major',labelsize=16)

labels = ('CPRTA','EPST-K', 'CRPTA','EPST-K')

try:
    ax.plot( 0, '', labels=labels)
except ValueError:
    print "ValueError"

ax.vlines(0.5, 0, 1, transform=ax.transAxes )
ax.text(0.35, 0.04, "$U^*=60\%$", transform=ax.transAxes, size=16 )
ax.text(0.85, 0.04, "$U^*=70\%$", transform=ax.transAxes, size=16 )

figure = plt.gcf()
figure.set_size_inches([10, 4])

pp.savefig()
plt.clf()
pp.close()
'''
