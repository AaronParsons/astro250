import aipy as a, numpy as n,glob,ephem

class AntennaArray(a.fit.AntennaArray):
    def set_jultime(self, t=None):
        a.fit.AntennaArray.set_jultime(self, t=t)
    def get_params(self, ant_prms={'*':'*'}):
        try: prms = a.fit.AntennaArray.get_params(self, ant_prms)
        except(IndexError): return {}
        for k in ant_prms:
            try: top_pos = n.dot(self._eq2zen, self[int(k)].pos)
            except(ValueError): continue
            if ant_prms[k] == '*':
                prms[k].update({'top_x':top_pos[0], 'top_y':top_pos[1], 'top_z':top_pos[2]})
            else:
                for val in ant_prms[k]:
                    if   val == 'top_x': prms[k]['top_x'] = top_pos[0]
                    elif val == 'top_y': prms[k]['top_y'] = top_pos[1]
                    elif val == 'top_z': prms[k]['top_z'] = top_pos[2]
        return prms
    def set_params(self, prms):
        changed = a.fit.AntennaArray.set_params(self, prms)
        for i, ant in enumerate(self):
            ant_changed = False
            top_pos = n.dot(self._eq2zen, ant.pos)
            try:
                top_pos[0] = prms[str(i)]['top_x']
                ant_changed = True
            except(KeyError): pass
            try:
                top_pos[1] = prms[str(i)]['top_y']
                ant_changed = True
            except(KeyError): pass
            try:
                top_pos[2] = prms[str(i)]['top_z']
                ant_changed = True
            except(KeyError): pass
            if ant_changed: ant.pos = n.dot(n.linalg.inv(self._eq2zen), top_pos)
            changed |= ant_changed
        return changed


prms = {
    'loc': ('+37:55.1', '-122:09.4'), # Leuschner Obs.
    'antpos':{
         0:(-959, -817,  12),
         1:(-130,  -79,   8),
         2:(-249,   75,  -9),
         3:(-207, -668,  14),
         4:(  78,    0, -17),
         5:( 505,  189,  17),
         6:(-611,  889,  10),
         7:(-206, -695,  24),
         8:(-532,  138,  26),
         9:(-114, -974,  -1),
        10:(-589,  190, -11),
        11:(-595,  869,   3),
        12:( 809, -645, -29),
        13:( 215,  540,  12),
        14:(-389,  745,   3),
        15:(-101, -997,  29),
        16:( 373,   94,  23),
        17:( 695,  356, -28),
        18:( 538, -943, -22),
        19:(  45, -641, -29),
        20:( 391, -763,  10),
        21:(-337, -462, -16),
        22:(-973,   29, -18),
        23:( 910,  401,  -4),
        24:( 750, -319, -16),
        25:(-150,   32,  26),
        26:( 830,  122, -30),
        27:( 945,  653, -21),
        28:( 285,  449,  -6),
        29:( 663,  276, -24),
        30:(-430,  971,  -4),
        31:( 797, -146, -13),
        32:( 384, -752,  -4),
        33:(-189, -534, -24),
        34:( 776,   67,  17),
        35:(-245,  781,  -2),
        36:(-287, -189, -23),
        37:( 902,  394,  -1),
        38:(-435,  -59, -12),
        39:( 711,  592,   0),
        40:(-116, -197, -25),
        41:(-209,  749, -30),
        42:(-689,  363,  13),
        43:(-621,  610, -19),
        44:( 421,  738,  16),
        45:(-710,  951,   6),
        46:(-336,  175,  20),
        47:( 106, -922,  -6),
        48:(-861, -223,  -8),
        49:(  88,  683, -26),
        50:(-503,  629,   0),
        51:( 898,   42,   7),
        52:(-271, -892, -22),
        53:( 334, -979,  22),
        54:( 374,  986, -20),
        55:(-578,  332,   7),
        56:( 369, -400, -14),
        57:( 355, -811, -28),
        58:( 635,  129, -22),
        59:(  45, -787,   2),
        60:( 569, -458,  22),
        61:( 505,  649,  14),
        62:(-748,  311, -10),
    },  

    'beam': a.fit.Beam2DGaussian,
    'bm_prms': {
        'bm_xwidth': n.Inf,
        'bm_ywidth': n.Inf,
    },
}

def get_aa(freqs):
    '''Return the AntennaArray to be used for simulation.'''
    location = prms['loc']
    antennas = []
    nants = len(prms['antpos'])
    for i in range(nants):
        beam = prms['beam'](freqs)
        try: beam.set_params(prms['bm_prms'])
        except(AttributeError): pass
        antennas.append(a.fit.Antenna(0.,0.,0., beam))
    aa = AntennaArray(prms['loc'], antennas)
    for ant in prms['antpos']:
        x,y,z = prms['antpos'][ant]
        aa.set_params({str(ant): {'top_x':x, 'top_y':y, 'top_z':z}})
        #aa.set_params({str(ant): {'top_x':x, 'top_y':y, 'top_z':0}})
        #print aa.get_params({str(ant):['top_x','top_y']})
    return aa

src_prms = {
    'srcA': {'ra':'12:00', 'dec':'40:00', 'jys':1000.},
    'srcB': {'ra':'12:30', 'dec':'40:00', 'jys':1000.},
    'srcC': {'ra':'13:00', 'dec':'40:00', 'jys':1000.},
    'srcD': {'ra':'13:30', 'dec':'40:00', 'jys':1000.},
    'srcE': {'ra':'14:00', 'dec':'40:00', 'jys':1000.},
    'srcF': {'ra':'14:30', 'dec':'40:00', 'jys':1000.},
    'srcG': {'ra':'15:00', 'dec':'40:00', 'jys':1000.},
    'srcH': {'ra':'15:30', 'dec':'40:00', 'jys':1000.},
    'srcI': {'ra':'16:00', 'dec':'40:00', 'jys':1000.},
    'srcJ': {'ra':'16:30', 'dec':'40:00', 'jys':1000.},
    'srcK': {'ra':'17:00', 'dec':'40:00', 'jys':1000.},
    'srcL': {'ra':'17:30', 'dec':'40:00', 'jys':1000.},
}

def get_catalog(srcs=None, cutoff=None, catalogs=['helm','misc']):
    '''Return a catalog containing the listed sources.'''
    custom_srcs = ['src'+i for i in 'ABCDEFGHIJKL']
    if srcs is None:
        cat = a.src.get_catalog(srcs=srcs, cutoff=cutoff, catalogs=catalogs)
    else:
        cat = a.src.get_catalog(srcs=[s for s in srcs if not s in custom_srcs],
            cutoff=cutoff, catalogs=catalogs)
        for src in [s for s in srcs if s in custom_srcs]:
            cat[src] = a.fit.RadioFixedBody(0., 0., janskies=0., mfreq=.15, name=src)
    cat.set_params(src_prms)
    return cat

