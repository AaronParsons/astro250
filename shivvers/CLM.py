'''
Central Limit Theorem in Python

Isaac Shivvers, Fall 2012
'''

import matplotlib.pyplot as plt
import numpy as np
import numpy.random as r


def append_dist(lll, type, nval=100):
    ''' sum another nval values drawn from distribution type to list lll '''
    if type=='L':
        lll.append(np.mean(r.standard_cauchy(nval)))
    elif type=='T':
        lll.append(np.mean(r.standard_t(1, nval)))
    elif type=='U':
        lll.append(np.mean(r.uniform(-15, 15, nval)))
    return lll

def gauss(x):
    ''' return gaussian on x with mean=0, std=1 '''
    return (1./(2*np.pi)**.5) * np.exp(-.5*x**2)



def run_demo(nval=100, bns=25, trial_length=1000):
    '''
    build and run CLM demo.
    nval: number of values to average at a time
    bns : number of histogram bins
    trial_length: how long to run the simulation 
    '''
    
    # we'll accumulate lists of the means of distributions in dists
    lortz = [np.mean(r.standard_cauchy(nval))]
    s_t   = [np.mean(r.standard_t(1, nval))]
    unif  = [np.mean(r.uniform(-15, 15, nval))]
    dists = [lortz, s_t, unif]
    
    # plot up a reference gaussian
    gx = np.linspace(-5, 5, 100)
    gy = gauss(gx)
    
    # set the bins array for the histograms
    bins = np.linspace(-3, 3, bns)
    
    # name and type the distributions
    names = ['Lorentz', 'Student T', 'Uniform']
    types = ['L', 'T', 'U']
    
    # make the plot
    hists = []
    f, axs = plt.subplots(nrows=3, ncols=1, sharex=True)
    plt.ion() # sets pyplot mode to interactive
    for i,ax in enumerate(axs):
        hists.append( ax.hist( dists[i], bins, alpha=.75, color='gray', normed=True) )
        ax.plot(gx, gy, c='r', lw=2)
        ax.axis([-3,3,0,.7])
        ax.annotate(names[i], xy=(-2.8,.6))
    plt.show()

    # update the distributions, and redraw the figure every 5 samples
    for iii in xrange(trial_length):
        for i,dd in enumerate(dists):
            append_dist(dd, types[i])
            if not iii%5:
                for patch in hists[i][-1]: patch.remove()
                hists[i] = axs[i].hist( dd, bins, alpha=.75, color='gray', normed=True)
        
        if not iii%5:
            plt.xlabel('samples: {}'.format(iii))
            plt.draw()


if __name__ == '__main__':
    run_demo()
    raw_input('\nDone!  Hit enter to exit.\n')