'''
Central Limit Theorem in Python

to run from shell:
$ python central_limit.py

Isaac Shivvers, Fall 2012
'''

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as r


def build_dist(type, n):
    if type=='l':
        # ARP: I like the list comprehensions
        d = [np.mean(r.standard_cauchy(n)) for x in range(x_len)]
    elif type=='t':
        d = [np.mean(r.triangular(-15, 0, 15, size=n)) for x in range(x_len)]
    elif type=='u':
        d = [np.mean(r.uniform(-15, 15, n)) for x in range(x_len)]
    return d



print 'here we go - sorry for being slow'

x_len = 10000 # ARP: for hardcoded parameters, I prefer using all uppercase (in the style of #define)
# build CLT figure
f1, axs = plt.subplots(nrows=3, ncols=4)
ns = [1, 1e2, 1e3, 1e4]
# ARP: types and names clearly correspond, so why not make them a dict?
# ARP: also, these map to functions in numpy.random, so why not also make that explicit in the dict:
# ARP: {'u': ('uniform',r.uniform)} or something like that, so that it's clear how these all are used together
types = ['u','l','t']
names = ['uniform', 'lorentz', 'triangular']
std_o_means = np.empty(np.shape(axs))
# ARP: I find these loops very hard to read.  Would prefer:
# ARP: for i,type in enumerate(types):   and    for j,n in enumerate(ns):
# ARP: that way, you know what you're looking over, and what i,j are counting.
for i in range(3):
    for j in range(4):
        if i==1:
            bins = np.linspace(-15, 15, 25)
        else:
            bins = 25
        ax = axs[i,j]
        dist = build_dist(types[i], ns[j])
        std_o_means[i,j] = np.std(dist)
        # ARP: these look like they converge to normal (except lorentz ??), but how do you know?
        ax.hist( dist, bins=bins, alpha=.75, color='gray' )
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        # ARP: the statement below always errors out for me, for some reason
        #ax.annotate('{} ::: n={}'.format(names[i], ns[j]), xy=(0,1), xycoords='axes fraction')

# build figure tracing std_o_mean
plt.figure(2)
plt.title('Evolution of the standard deviation of the mean')
clrs = ['r','g','b']
for i in range(3): # ARP: I think it'd be better to use a zip statement here "som,c,name = zip(std_o_means,clrs,names)"
    plt.scatter( ns, std_o_means[i,:], c=clrs[i], label=names[i] )
    # ARP: what does this plot show?  The distribution changes with n, but does sigma?
plt.xlabel('n')
plt.ylabel('STD of the mean')
plt.legend(loc='best')
plt.show()





