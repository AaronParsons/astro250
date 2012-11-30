# 
#  radiometer_test.py
#  <Ay 250: Lab #3, testing the radiometer equation>
#  
#  Created by Nick Hand on 2012-09-27.
# 
from scipy.stats import norm
import numpy as np
import pylab as pl

def test_radiometer_eqn(Ns, T_sys):
    """
    @brief test the accuracy of the radiometer equation by simulating N samples
    of Gaussian noise and measuring a system temperature for this noise. Computes
    the error on this temp for fixed N, and compares with the radiometer equation,
    sigma_T = T_sys / sqrt(BT), where B=bandpass, T = integration time
    
    @param Ns: draw samples of size N from normal distribution (array)
    @param T_sys: input system temperature for noise 
    """
    # boltzmann constant in m^2 kg s^-2 K^-1
    k_b = 1.3806503e-23  # ARP: defining constants should really occur outside of the function
    
    # define characteristic value for bandpass in Hz 
    B = 1e6 
    
    # the standard deviation of the voltage noise
    sigma_V = np.sqrt(k_b*T_sys*B) 
    
    sigma_T_measured = []
    sigma_T_theory = []
    for N in Ns:
        print N # ARP: I find users to be rather impatient unless you show that something is happening :)
            
        T_estimates = []
        N_mc = 10000 # ARP: maybe make this a parameter w/ default value?
        for i in range(N_mc):
            
            # draw N gaussian random variates with mean zero and std dev sigma_V
            voltage = norm.rvs(loc=0.0, scale=sigma_V, size=N)
            
            # calculate power as the voltage squared
            power = voltage**2
            
            # compute the product of B*T, bandpass times total integration time
            # N = 2*B*T
            BT = N/2. # ARP: this is fine, but does take me at my word that 2BT is how you count samples.  Might be interesting to think of a way to show that N=2BT...
            
            # get temperature from power and store our measured system temp
            temp = power / (k_b*B)
            T_estimated = np.mean(temp)
            T_estimates.append(T_estimated)
          
        # compute the erorr on our measured system temp  
        sigma_T_measured.append(np.std(T_estimates))
        
        # compute the true error from radiometer equation: sigma_T = T_sys / sqrt(BT)
        sigma_T_theory.append(T_sys / np.sqrt(BT))
     
    # plot the error on measured T as function of number of samples       
    pl.plot(Ns, sigma_T_theory, c='k')
    pl.plot(Ns, sigma_T_measured, ls='', marker='o', c='b')
    # ARP: as per CLT, loglog is the only way to plot power laws
    # ARP: and separating plotting and calculation enhances reusability of code
    pl.xlabel('number of independent samples, N=2BT', fontsize=16)
    pl.ylabel(r'error in $T_\mathrm{sys}$ estimation, $\sigma_T$', fontsize=16)
    pl.title(r'Testing the radiometer equation, assuming $T_\mathrm{sys}$ = %d K' %T_sys)
    pl.savefig('radiometer_sigmaT.png') # ARP: I guess I prefer showing the plot, rather than silently generating files.
    
    return 
    
if __name__ == '__main__':
    
    
    Ns = np.linspace(5.0, 500.0, 50.0)
    T_sys = 300.0
    test_radiometer_eqn(Ns, T_sys)
