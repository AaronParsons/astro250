# 
#  central_limit.py
#  <Ay 250: Lab #3, testing the central limit theorem>
#  
#  Created by Nick Hand on 2012-09-21.
# 
import scipy.stats
import numpy as np
import pylab as pl

def test_CLT(Ns, host_dist, scale=0., loc=1., interactive=True):
    """
    @brief test the CLT by drawing N-sized samples from an underlying host 
    distribution and plotting the histogram of the sample averages
    
    @param Ns: draw samples of size N (array)
    @param host_dist: underlying distribution to draw from (scipy.stats function)
    @param scale: the scale keyword to pass to the host_dist function (float)
    @param loc: the loc keyword to pass to the host_dist function (float)
    @param interactive: plot the sample distributions interactively (boolean) 
    """
    # ARP: love the doxygen docstring
    # ARP: I like that you put the bulk of your code in a reusable function,
    # ARP: but I think you'll find your function to be more reusable if you separate the math and the plotting
    # ARP: into separate functions

    # set up the figure showing the histogram
    fig1 = pl.figure()
    ax1 = fig1.gca()
    
    if interactive:
        pl.ion() # make pylab interactive
        # ARP: I enjoyed the animation
        
        # label the axes
        ax1.set_xlabel("sample averages", fontsize=16)
        ax1.set_ylabel("probability density", fontsize=16)
        fig1.show()

    std_devs = []

    for N in Ns:
        sample_avgs = [] # store sample averages here

        # compute 10,000 sample averages to measure an accurate pdf
        N_mc = 10000
        for i in np.arange(N_mc):
    
            # take the mean of N random variates drawn from exponential 
            # distribution exp = lambda * exp(-lambda*x)
            # mu = 10.0, std dev = 10.0
            avg = np.mean(host_dist.rvs(size=N, scale=scale, loc=loc))
            sample_avgs.append(avg)  
    
        # plot the histogram of the sample averages
        if interactive:
            ax1.set_title('N = %d' %N)
            pdf, bins, patches = ax1.hist(sample_avgs, bins=50,normed=True, alpha=0.1)
            pl.draw()
    
        # save the standard deviation of the sample averages
        std_devs.append(np.std(sample_avgs))
 
    # clear the interactive axes and plot the final large-N histogram
    ax1.cla()
    pdf, bins, patches = ax1.hist(sample_avgs, bins=50, facecolor='gray', normed=True, alpha=0.4)
    ax1.set_xlabel("sample averages", fontsize=16)
    ax1.set_ylabel("probability density", fontsize=16)
    ax1.set_title('CLT for sample size N=%d, drawn from %s distribution' %(Ns[-1], host_dist.name))
    
    # overlay a normal distribution with mu = 1.0 and sigma = 10.0 / sqrt(N)
    x = np.linspace(np.amin(sample_avgs), np.amax(sample_avgs), 1000)
    
    # get the mean and std dev of host distribution
    mu = host_dist.mean(scale=scale, loc=loc)
    sigma = host_dist.std(scale=scale, loc=loc)
    ax1.plot(x, scipy.stats.norm.pdf(x, loc=mu, scale=sigma/np.sqrt(N)), c='k')

    fig1.savefig('clt_hist_%s.png' %host_dist.name)
    pl.close()

    # set up the figure showing the histogram
    fig2 = pl.figure()
    ax2 = fig2.gca()

    ax2.scatter(Ns, std_devs, color='k')
    ax2.plot(Ns, sigma/np.sqrt(Ns), c='k') # ARP: this plot shows your prediction & measurement well, but could be loglog to facilitate interpretation

    # label the axes
    ax2.set_xlabel("sample size N", fontsize=16)
    ax2.set_ylabel("standard deviation", fontsize=16)
    fig2.savefig('sigma_vs_N_%s.png' %host_dist.name)

    return

if __name__ == '__main__':
    # ARP: I'm a big fan of separating resuable code from what runs on the command line, as you do here
    # ARP: Don't know if you know about the optparse module for a quick way to whip up a command line interface.
    
    
    Ns = np.linspace(1, 200, 25)  # these are the sample sizes (the usual 'N')
    test_CLT(Ns, scipy.stats.uniform, scale=10, loc=1, interactive=True)
