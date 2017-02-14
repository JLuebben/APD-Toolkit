"""
Created on 13.02.2017

@author: Jens Luebben

"""
KEY = 'IR'
OPTION_ARGUMENTS = {'load': 'test.test',
                    'type': 'transmission'}
HEADLINE = '''GENERATE IR-SPECTRUM'''
RESOLUTION = 5000

from lauescript.core import *
from lauescript.cryst.iterators import database
import numpy as np
from numpy import tanh, log

def run(pluginManager):
    printer = pluginManager.setup()
    mode = pluginManager.arg('type')
    if not mode in ['transmission', 'emission', 'absorption']:
        printer('ERROR: type not understood. "type" must be <emission>, <absorption> or <transmission>')
        pluginManager.exit()
    data = database(pluginManager, asDict=True)
    molecule = pluginManager.get_variable('data')['exp']
    hk = 0.719385E0
    hc = 16.85773329E0
    Temp = 10.
    points = np.zeros(RESOLUTION)

    for atom in molecule.atoms:
        modelCompound = atom.invariom.molecule
        modelCompound = data[modelCompound.name]
        # print(modelCompound.IRIntensities)
        for freq0, I in zip(modelCompound.freq, modelCompound.IRIntensities):
            m_red = freq0[1]
            if mode == 'emission':
                delta = (1 / (tanh(hk * freq0[0] / Temp))) * hc / freq0[0] / m_red
                points += gaussian(np.linspace(0, 5000, RESOLUTION), freq0[0], 5) * delta
            else:
                points += gaussian(np.linspace(0, 5000, RESOLUTION), freq0[0], 5) * I
    from matplotlib import pyplot as mp
    # mp.plot(np.ones(RESOLUTION)-points)
    if mode == 'emission':
        mp.plot(points)
        fileName = 'emission.eps'
    elif mode == 'absorption':
        mp.plot(points)
        fileName = 'absorption.eps'
    else:
        mp.plot(1-(points/max(points)))
        fileName = 'transmission.eps'
    # mp.ylim(0,1)
    # mp.xlim(200,320)
    mp.savefig(fileName)

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
