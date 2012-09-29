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
        d = [np.mean(r.standard_cauchy(n)) for x in range(x_len)]
    elif type=='t':
        d = [np.mean(r.triangular(-15, 0, 15, size=n)) for x in range(x_len)]
    elif type=='u':
        d = [np.mean(r.uniform(-15, 15, n)) for x in range(x_len)]
    return d



print 'here we go - sorry for being slow'

x_len = 10000
# build CLT figure
f1, axs = plt.subplots(nrows=3, ncols=4)
ns = [1, 1e2, 1e3, 1e4]
types = ['u','l','t']
names = ['uniform', 'lorentz', 'triangular']
std_o_means = np.empty(np.shape(axs))
for i in range(3):
    for j in range(4):
        if i==1:
            bins = np.linspace(-15, 15, 25)
        else:
            bins = 25
        ax = axs[i,j]
        dist = build_dist(types[i], ns[j])
        std_o_means[i,j] = np.std(dist)
        ax.hist( dist, bins=bins, alpha=.75, color='gray' )
        plt.setp(ax.get_xticklabels(), visible=False)
        plt.setp(ax.get_yticklabels(), visible=False)
        ax.annotate('{} ::: n={}'.format(names[i], ns[j]), xy=(0,1), xycoords='axes fraction')

# build figure tracing std_o_mean
plt.figure(2)
plt.title('Evolution of the standard deviation of the mean')
clrs = ['r','g','b']
for i in range(3):
    plt.scatter( ns, std_o_means[i,:], c=clrs[i], label=names[i] )
plt.xlabel('n')
plt.ylabel('STD of the mean')
plt.legend(loc='best')
plt.show()





