import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from scipy.stats import binom

# plot from z=-5 to z=5
z = np.linspace(-5,5,500)
# flip n coins
n=1024
# with probability of heads p
p=0.9

#plot the normal cdf
plt.plot(z,norm.cdf(z))

#calculate parameters for the average of a binomial variable A_n
mu=p
stddev=np.sqrt(p*(1-p)/n)

#calculate the upper limit of S_n (the binomial variable)
x=np.floor((mu+z*stddev)*n)

#plot the binomial cdf
plt.plot(z,binom.cdf(x,n,p))
plt.show()

