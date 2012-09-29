'''
Verify the radiometer equation,
and show that the factor of two
is where it should be.

Isaac Shivvers, Fall 2012



The radiometer equation is basically saying that the 
error of our measured temperature (aka our signal) is
proportional to the power in the noise (aka T_sys)
divided by the square root of the number of samples
(from the central limit theorem and the variance
of the mean of a gaussian signal).
'''

import numpy as np
import matplotlib.pyplot as plt


# generate some white noise samples:
noise = np.random.standard_normal(1e6)
p = noise**2
print 'the standard deviation of x^2 (where x is a gaussian RV) is:', np.std(p)

# now make a plot to prove the point:
x, y = [], []
print 'sorry this may be slow!'
for i in np.linspace(0, 6, 50):
    print i
    # generate noise and measure the signal
    means = [np.mean( np.random.standard_normal(int(1*10**i)) ) for jjj in range(100)]
    err   = np.std(means)
    x.append(int(1*10**i))
    y.append(err)


yy = np.array(x)**-.5
plt.loglog(x, yy, c='k', label='predicted')
plt.scatter(x, y, marker='x', c='r', label='measured')

plt.title('How correct is the radiometer equation?')
plt.xlabel(r'number of samples ($\sqrt{Bt}$)')
plt.ylabel(r'$\sigma_T$')
plt.legend()
plt.show()

