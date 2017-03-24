"""
Created on 13.02.2017

@author: Jens Luebben

"""
KEY = 'IR'
OPTION_ARGUMENTS = {'load': 'test.test',
                    'type': 'transmission'}
HEADLINE = '''GENERATE IR-SPECTRUM'''
RESOLUTION = 4000

from lauescript.core import *
from lauescript.cryst.iterators import database
import numpy as np
from numpy import tanh, log
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

def run(pluginManager):
    printer = pluginManager.setup()
    mode = pluginManager.arg('type')
    if not mode in ['transmission', 'emission', 'absorption', 'composite']:
        printer('ERROR: type not understood. "type" must be <emission>, <absorption> or <transmission>')
        pluginManager.exit()
    data = database(pluginManager, asDict=True)
    molecule = pluginManager.get_variable('data')['exp']
    hk = 0.719385E0
    hc = 16.85773329E0
    Temp = 100.
    points = np.zeros(RESOLUTION)

    for i, atom in enumerate(sorted(molecule.atoms, key=lambda atom: atom.get_element())):
        modelCompound = atom.invariom.molecule
        modelCompound = data[modelCompound.name]
        # print(modelCompound.IRIntensities)
        for freq0, I in zip(modelCompound.freq, modelCompound.IRIntensities):
            m_red = freq0[1]
            if mode == 'emission':
                delta = (1 / (tanh(hk * freq0[0] / Temp))) * hc / freq0[0] / m_red
                points += gaussian(np.linspace(0, 4000, RESOLUTION), freq0[0], 5) * delta
            else:
                points += gaussian(np.linspace(0, 4000, RESOLUTION), freq0[0], 15) * I
        if mode == 'composite':
            # plotTrans(list(range(RESOLUTION)), 1-(points/max(points)), 'transmissionX{:2n}.eps'.format(i), label='+'+atom.name)
            # plotTrans(list(range(RESOLUTION)), 1-(points/2000), 'transmissionX-{:0>2n}.eps'.format(i), label='+ {} from {}'.format(atom.name, atom.invariom.molecule.name))
            plotTrans(list(range(RESOLUTION)), 1-(points/2000), 'transmissionX-{}.png'.format(i), label='+ {} from {}'.format(atom.name, atom.invariom.molecule.name))
            # points = np.zeros(RESOLUTION)
    # from matplotlib import pyplot as mp
    # mp.plot(np.ones(RESOLUTION)-points)
    # points = np.array(list(reversed(points)))
    if mode == 'emission':
        # mp.plot(points)
        # fileName = 'emission.eps'
        plotEm(list(range(RESOLUTION)), points, 'emission.eps')
    elif mode == 'absorption':
        mp.plot(points)
        fileName = 'absorption.eps'
    else:
        # mp.plot(1-(points/max(points)))
        # fileName = 'transmission.eps'
        plotTrans(list(range(RESOLUTION)), 1-(points/max(points)), 'transmission.eps')
    # mp.savefig(fileName)

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def plotTrans(x, y, fileName, label=''):
    plt.gcf().clear()
    flatui = ["#9b59b6", "#3498db", "#95a5a6",  "#34495e", "#2ecc71"]
    sns.set_palette(flatui[1:])
    sns.set_style("ticks")
    palette = itertools.cycle(sns.color_palette())

    plt.plot(x, y, marker='', label=label, color=next(palette))


    plt.legend(loc='lower left')
    # plt.subplots()[1].xaxis.tick_top()
    plt.gcf().subplots_adjust(bottom=0.15, top=0.95)
    plt.gca().invert_xaxis()
    # xticks, xticklabels = plt.xticks()
    # yticks, yticklabels = plt.yticks()
    # yticks = [ -4.,  -2. ,  0. ,  2. ,  4.  , 6.,   8.,  10. , 12.,  14.]
    # plt.yticks(yticks)
    # xmin = -61
    # xmax = 61
    # plt.xlim(xmin, xmax)
    plt.ylim(0,1)
    # plt.xlim(-1.5,1.5)
    # plt.xticks(xticks)

    sns.despine(offset=10, trim=True, bottom=False, right=False, left=False, top=False)

    plt.xlabel('Wavenumber [1/cm]')
    plt.ylabel('Transmission [%]')
    # plt.ylabel('Electron Density')
    plt.savefig(fileName)
    # print('\nFigure written to <{}>.'.format(fileName))


def plotEm(x, y, fileName):
    flatui = ["#9b59b6", "#3498db", "#95a5a6",  "#34495e", "#2ecc71"]
    sns.set_palette(flatui[1:])
    sns.set_style("ticks")
    palette = itertools.cycle(sns.color_palette())
    plt.ylim(0, 2)
    yticks = list(range(3))
    plt.yticks(yticks)
    plt.plot(x, y, marker='', label='100 K', color="#3498db")

    # yy = gaussian(np.linspace(0, 4000, RESOLUTION), 150, 75)* 5
    # plt.plot(x, yy, marker='', label='Missing', color=next(palette))


    plt.legend(loc='upper left')
    # plt.subplots()[1].xaxis.tick_top()
    plt.gcf().subplots_adjust(bottom=0.15, top=0.95)
    plt.gca().invert_xaxis()
    # xticks, xticklabels = plt.xticks()
    # yticks, yticklabels = plt.yticks()
    # yticks = [ -4.,  -2. ,  0. ,  2. ,  4.  , 6.,   8.,  10. , 12.,  14.]
    # plt.yticks(yticks)
    # xmin = -61
    # xmax = 61
    # plt.xlim(xmin, xmax)
    # plt.ylim(-4,15)
    # plt.xlim(-1.5,1.5)
    # plt.xticks(xticks)

    sns.despine(offset=10, trim=True, bottom=False, right=True, left=False, top=True)

    plt.xlabel('Wavenumber [1/cm]')
    plt.ylabel('Emission')
    # plt.ylabel('Electron Density')

    plt.savefig(fileName)

    yy = gaussian(np.linspace(0, 4000, RESOLUTION), 150, 40)* 2
    plt.plot(x, yy, marker='', label='Missing', color="#9b59b6")
    plt.savefig('emission2.eps')

    p = y + yy
    yyy = np.array([sum(p[:i+1]) for i,j in enumerate(p)])
    yyy = yyy/max(yyy)
    yyy= np.array([1-i for i in yyy])
    yyy *= 2
    plt.plot(x, yyy, marker='', label='Missing', color="#95a5a6")
    plt.ylim(0, 2)
    plt.savefig('emission3.eps')
    # print('\nFigure written to <{}>.'.format(fileName))
