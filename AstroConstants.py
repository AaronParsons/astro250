# initial setup based on similar file in IDL written by James Graham

# set up cgs units
cm = 1.0
gram = 1.0
second = 1.0
erg = 1.0
kelvin = 1.0

# prefixes
giga = 1e9
mega = 1e6
kilo = 1e3
centi = 1e-2
milli = 1e-3
micro = 1e-6
nano = 1e-9
pico = 1e-12

# fundamental constants
h            = 6.62606876e-27   # planck constant
c            = 2.99792458e10    # speed of light
kb           = 1.3806503e-16    # Boltzmann constant
stefanBoltz  = 5.67040e-5       # Stefan-Boltzman constant
massProton   = 1.67262158e-24   # proton mass
massElectron = 9.10938188e-28   # electron mass
e            = 4.803242e-10     # e.s.u.
qemu         = 1.602176462e-20  # e.m.u
G            = 6.673e-8         # Newton's constant
bohrRadius   = 5.2918e-9        # cm
eV           = 1.60217653e-12   # ergs

# length conversion factors
km       = 1.0e+5 * cm  
meter    = 1.0e+2 * cm  
inch     = 2.54   * cm  
mm       = 0.1    * cm  
micron   = 1.0e-4 * cm  
angstrom = 1e-8   * cm  

# energy and power conversion factors
joule           = 1e7 * erg
watt            = 1e7 * erg / second
electronvolt    = 1.602176462e-12 * erg
rydberg         = 10973731.568 * meter**(-1.)

# astronomical constants
au     = 499.004782 * second * c  # the astronomical unit
arcsec = 1.0e0 / 206265.0         # radians
parsec = au / arcsec              # cm
minute = 60.                      # seconds
hour   = 60. * 60.                # seconds
day    = 8.64e4                   # seconds
year   = 365.2425 * da            # seconds

kGauss = 0.017202098950           # Gauss's constant for orbital
                                  # motion ... (kp)^2 = a^3
                                                                    
lumSun    = 3.826e33              # erg/s
massSun   = 1.9891e3              # gm
radSun    = 6.9598e10             # cm
tempSun   = 5770.0                # kelvin
vMagSun   = -26.74                # apparent V mag of sun
bolMagSun = 4.75                  # bolometric mag of sun

lStarSchecter  = 3.4e10 * lumSun  # l-star for Schecter luminosity function
mbStar         = -21.0e0          # M_B*
#mbStar = -20.6                   # M_B* Mihalis & Binney

massEarth   = 5.976e27            # Earth mass in gm
radEarth    = 6371 * km           # Earth's equatorial radius in cm 
massJupiter = 1898.8e27           # Jupiter in gm
radJupiter  = 70850 * km          # Jupiter's equatorial radius in cm

jansky  = 1.0e-23                 # erg/s/cm/cm/Hz

sigmaThomson = 6.6524e-25         # Thomson cross section

mjd00 = 2400000.5                 # zero point for modified julian day


