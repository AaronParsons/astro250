import numpy as n
import optparse , sys
import pylab as p

def get_mean(sample_size, normal=False):
    '''cent_limit takes an argument N = number of samples.'''
    if normal: 
        set = n.random.normal(size=sample_size)
    else:
        set = n.random.randint(1,10000,sample_size)
    return n.mean(set)

def cent_lim(N,sample_size=5,normal=False):
    means = []
    for i in xrange(N):
        means.append(get_mean(sample_size,normal=normal))
    return means


try: 
    # ARP: enclosing huge blocks of code in try statements is usually frowned upon,
    # b/c it's hard to track down what threw the exception.  Also, if you just
    # to catch KeyboardInterrupt and exit, why catch it?
    o = optparse.OptionParser()
    o.add_option('-n', type='int', dest='largen',default=10000,
                 help='Number of sample means to use') 
    o.add_option('-s', type='int', dest='sample_size',default=5,
                 help='sample size to use to generate mean.')
    opts,args = o.parse_args(sys.argv[1:]) # ARP: I like your command line interface.  Usually worth the effort

    means = cent_lim(opts.largen)
    p.figure(2)
    p.hist(means,bins=1000) # ARP: plot is nice, and it looks like a normal distribution, but is it?  How can you know?
    p.axvline(n.mean(means), label='Mean=%d'%n.mean(means))
    p.legend()


    #note that here we are using normally distributed noise with mean = 0 and sd = 1
    avgs = []
    stds = []
    for i in xrange(1,20):
        mus = cent_lim(100,sample_size=2**i, normal=True) 
        avgs.append( n.mean(mus))
        stds.append(n.std(mus))


    x = 2**n.arange(1,20) # ARP: you create x here to match the xrange(1,20) above, but better style is to create x first, and then use "for i in x:" so that this relationship is explicit
    p.figure(1)
    p.loglog(x,stds)
    p.loglog(x,1/x**.5) # ARP: nice graph of what you expect.
    p.show()
        

except(KeyboardInterrupt):
    exit()
    

     
