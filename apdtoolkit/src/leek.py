"""
Created on Feb 12, 2014

@author: Jens Luebben

Plugin for estimating anisotropic rigid body vibrations from ONIOM point mass computations
"""
KEY = 'leek'
OPTION_ARGUMENTS = {'load': None,
                    'mode': 'TLS',
                    'data': 'exp'}
HEADLINE = ' Using pointmasses to estimate rigid body movement  '

import numpy as np

from lauescript.laueio.inout import read_database
from lauescript.types.atom import ATOM
from lauescript.cryst.crystgeom import rotate_adp3


def run(pluginManager):
    data = pluginManager.get_variable('data')
    useData = pluginManager.arg('data')
    printer = pluginManager.setup()
    dabapa = './APD_DABA_{:.1f}_.txt'.format(data.temperature)
    database = open(dabapa, 'r').readlines()
    read_database(data, database, invlist=[], readAll=True)
    pseudoMols = [data[key] for key in data.keys() if key.startswith('pointMass_')]
    data.give_molecule('periphery', [])
    periphery = data['periphery']
    for i, pm in enumerate(pseudoMols):
        for datom in pm.atoms:
            # printer('{}     {}'.format(atom.cart, atom.adp['cart_int']))
            atom = ATOM('X{}'.format(i), 'C', datom.cart, molecule=periphery)
            atom.adp['cart_meas'] = datom.adp['cart_int']
            periphery.atoms.append(atom)
    printer('Generating Pseudo Molecule from point masses:')
    for atom in periphery.atoms:
        printer(str(atom))
    data['pseudo'] = periphery
    printer('\nGenerating rigid body vibration description via TLS fit against\nPseudo Molecule.')
    options = {'options': ['correlate'], 'data': ['pseudo']}
    pluginManager.call('T2', options)
    TLS = pluginManager.get_variable('TLS')

    refMol = data[useData]
    for atom in refMol.atoms:
        generateADP(atom, TLS)
        atom.adp['frac_int'] = rotate_adp3(atom.adp['cart_int'],
                                                  atom.molecule.cart2fracmatrix,
                                                  atom.molecule.cell)
        atom.adp['cart_sum'] = atom.adp['cart_int'] + atom.adp['cart_ext']
        atom.adp['frac_sum'] = atom.adp['frac_int'] + atom.adp['frac_ext']



def generateADP(atom, TLS):
    """
    Computes the ADP of an atom located at the cartesian coordinates 'cart' based on the parameters
    'T', 'L' and 'S' encoding the rigid body movement of the atom.
    :param atom:
    :param TLS:
    :return:
    """
    x1, x2, x3 = atom.cart
    TLS = np.array(TLS)
    newADP = []
    U11 = np.array([1, 0, 0, 0, 0, 0, 0, x3 * x3, x2 * x2, 0, 0, -2 * x2 * x3, 0, 0, 0, 0, 0, 2 * x3, 0, -2 * x2, 0])
    U11 = np.dot(TLS, U11)
    newADP.append(U11)
    U22 = np.array([0, 1, 0, 0, 0, 0, x3 * x3, 0, x1 * x1, 0, -2 * x1 * x3, 0, 0, 0, 0, -2 * x3, 0, 0, 0, 0, 2 * x1])
    U22 = np.dot(TLS, U22)
    newADP.append(U22)
    U33 = np.array([0, 0, 1, 0, 0, 0, x2 * x2, x1 * x1, 0, -2 * x1 * x2, 0, 0, 0, 0, 0, 0, 2 * x2, 0, -2 * x1, 0, 0])
    U33 = np.dot(TLS, U33)
    newADP.append(U33)

    U12 = np.array([0, 0, 0, 1, 0, 0, 0, 0, -x1 * x2, -x3 * x3, x2 * x3, x1 * x3, -x3, x3, 0, 0, 0, 0, 0, x1, -x2])
    U12 = np.dot(TLS, U12)
    newADP.append(U12)
    U13 = np.array([0, 0, 0, 0, 1, 0, 0, -x1 * x3, 0, x2 * x3, -x2 * x2, x1 * x2, x2, 0, -x2, 0, 0, -x1, x3, 0, 0])
    U13 = np.dot(TLS, U13)
    newADP.append(U13)
    U23 = np.array([0, 0, 0, 0, 0, 1, -x2 * x3, 0, 0, x1 * x3, x1 * x2, -x1 * x1, 0, -x1, x1, x2, -x3, 0, 0, 0, 0])
    U23 = np.dot(TLS, U23)
    newADP.append(U23)
    atom.adp['cart_ext'] = newADP
    atom.adp['frac_ext'] = rotate_adp3(newADP,
                                                  atom.molecule.cart2fracmatrix,
                                                  atom.molecule.cell)

