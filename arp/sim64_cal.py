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
         0:(-959, -817, ),
         1:(-130,  -79, ),
         2:(-249,   75, ),
         3:(-207, -668,   ),
         4:(78,    0,  ),
         5:(505, 189, ),
         6:(-611,  889, ),
         7:(-206, -695, ),
         8:(-532,  138, ),
         9:(-114, -974, ),
        10:(-589,  190,),
        11:(-595,  869,  ),
        12:(809, -645,  ),
        13:(215,  540, ),
        14:(-389,  745, ),
        15:(-101, -997,  ),
        16:(373, 94,  ),
        17:(695,  356,  ),
        18:(538, -943,   ),
        19:(45, -641,  ),
        20:(391, -763, ),
        21:(-337, -462,),
        22:(-973,   29,  ),
        23:(910,  401,  ),
        24:(750, -319, ),
        25:(-150,   32,  ),
        26:(830,  122,  ),
        27:(945, 653,  ),
        28:(285,  449,  ),
        29:(663,  276, ),
        30:(-430,  971,  ),
        31:(797, -146,  ),
        32:(384, -752, ),
        33:(-189, -534,  ),
        34:(776,   67, ),
        35:(-245, 781, ),
        36:(-287, -189,  ),
        37:(902,  394, ),
        38:(-435,  -59,  ),
        39:(711,  592, ),
        40:(-116, -197,),
        41:(-209,  749, ),
        42:(-689,  363, ),
        43:(-621,  610,  ),
        44:(421,  738, ),
        45:(-710,  951, ),
        46:(-336, 175,  ),
        47:(106, -922, ),
        48:(-861, -223,   ),
        49:(88,  683, ),
        50:(-503,  629,  ),
        51:(898,   42,),
        52:(-271, -892,  ),
        53:(334, -979,  ),
        54:(374,  986, ),
        55:(-578,  332,  ),
        56:(369, -400,  ),
        57:(355, -811,  ),
        58:(635,  129,   ),
        59:(45, -787,  ),
        60:(569, -458, ),
        61:(505,  649,  ),
        62:(-748,  311),
    },

    'beam': a.fit.Beam2DGaussian,
    'bm_prms': {
        'bm_xwidth': .5,
        'bm_ywidth': .5,
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
        x,y = prms['antpos'][ant]
        aa.set_params({str(ant): {'top_x':x, 'top_y':y}})
        #print aa.get_params({str(ant):['top_x','top_y']})
    return aa

src_prms = {
    'srcA': {'ra':'11:30', 'dec':'40:00', 'jys':1000.},
    'srcB': {'ra':'12:30', 'dec':'40:00', 'jys':1000.},
    'srcC': {'ra':'11:30', 'dec':'30:00', 'jys':1000.},
    'srcD': {'ra':'11:45', 'dec':'28:00', 'jys':1000.},
    'srcE': {'ra':'12:00', 'dec':'27:00', 'jys':1000.},
    'srcF': {'ra':'12:15', 'dec':'28:00', 'jys':1000.},
    'srcG': {'ra':'12:30', 'dec':'30:00', 'jys':1000.},
}

def get_catalog(srcs=None, cutoff=None, catalogs=['helm','misc']):
    '''Return a catalog containing the listed sources.'''
    custom_srcs = ['src'+i for i in 'ABCDEFG']
    if srcs is None:
        cat = a.src.get_catalog(srcs=srcs, cutoff=cutoff, catalogs=catalogs)
    else:
        cat = a.src.get_catalog(srcs=[s for s in srcs if not s in custom_srcs],
            cutoff=cutoff, catalogs=catalogs)
        for src in [s for s in srcs if s in custom_srcs]:
            cat[src] = a.fit.RadioFixedBody(0., 0., janskies=0., mfreq=.15, name=src)
    cat.set_params(src_prms)
    return cat

