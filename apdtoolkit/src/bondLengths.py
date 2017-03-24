"""
Created on 13.02.2017

@author: Jens Luebben

"""
KEY = 'B'
OPTION_ARGUMENTS = {'load': 'test.test',
                    }
HEADLINE = '''Compare Bond Lengths'''

from lauescript.core.core import quickLoad
from lauescript.cryst.iterators import database, iter_atom_pairs
from lauescript.cryst.match import match_point_clouds
import numpy as np
from numpy import tanh, log
import itertools

def run(pluginManager):
    printer = pluginManager.setup()
    molecule1 = pluginManager.get_variable('data')['exp']
    molecule2 = quickLoad(pluginManager, pluginManager.arg('load')[0])
    # molecule3 = quickLoad(pluginManager, pluginManager.arg('load')[1])
    dists1 = []
    for atom1, atom2 in iter_atom_pairs(molecule1):
        otherAtom1 = molecule2[atom1.name]
        otherAtom2 = molecule2[atom2.name]
        # thirdAtom1 = molecule3[atom1.name]
        # thirdAtom2 = molecule3[atom2.name]
        dist = abs(atom1-atom2)
        otherDist = abs(otherAtom1-otherAtom2)
        # thirdDist = abs(thirdAtom1-thirdAtom2)
        # print(abs(dist - otherDist) - abs(dist- thirdDist))
        print(abs(dist - otherDist))
        # dists1.append(abs(dist - otherDist) - abs(dist- thirdDist))
        dists1.append(abs(dist - otherDist))
    print()
    print(np.mean(dists1))



















    return
    atoms1 = [atom for atom in molecule1.atoms if not atom.get_active_invariom() == 'O1h1h' and not atom.get_active_invariom() == 'H1o1h']
    atoms2 = [atom for atom in molecule2.atoms if not atom.get_active_invariom() == 'O1h1h' and not atom.get_active_invariom() == 'H1o1h']
    c1 = [atom.cart for atom in atoms1]
    c2 = [atom.cart for atom in atoms2]
    x = match_point_clouds(c1, c2, threshold=.5)[0]
    # a=0
    # for i, j in zip(atoms1, atoms2):
    #     print(i, atoms2[x[a]])
    #     a+=1
    getOtherAtom = {atom.name: atoms2[i] for i, atom in zip(x, atoms1)}
    # for key, value in getOtherAtom.items():
    #     print(key, value)
    dists1 = []
    for atom1, atom2 in iter_atom_pairs(molecule1):
        if not atom1.get_element() == 'H' and not atom2.get_element() == 'H':
            continue
        if atom1.get_active_invariom() == 'O1h1h' or atom2.get_active_invariom() == 'O1h1h':
            continue
        # print(atom1, atom2, '----', getOtherAtom[atom1.name], getOtherAtom[atom2.name])
        dist1 = atom1 - atom2
        dist2 = getOtherAtom[atom1.name] - getOtherAtom[atom2.name]
        # print(abs(dist1-dist2), '\n')
        dists1.append(abs(dist1-dist2))

    molecule2 = quickLoad(pluginManager, pluginManager.arg('load')[1])
    atoms1 = [atom for atom in molecule1.atoms if not atom.get_active_invariom() == 'O1h1h' and not atom.get_active_invariom() == 'H1o1h']
    atoms2 = [atom for atom in molecule2.atoms if not atom.get_active_invariom() == 'O1h1h' and not atom.get_active_invariom() == 'H1o1h']
    c1 = [atom.cart for atom in atoms1]
    c2 = [atom.cart for atom in atoms2]
    x = match_point_clouds(c1, c2, threshold=.5)[0]
    # a=0
    # for i, j in zip(atoms1, atoms2):
    #     print(i, atoms2[x[a]])
    #     a+=1
    getOtherAtom = {atom.name: atoms2[i] for i, atom in zip(x, atoms1)}
    # for key, value in getOtherAtom.items():
    #     print(key, value)
    dists2 = []
    ii = 0
    diffs = []
    for atom1, atom2 in iter_atom_pairs(molecule1):
        if not atom1.get_element() == 'H' and not atom2.get_element() == 'H':
            continue
        if atom1.get_active_invariom() == 'O1h1h' or atom2.get_active_invariom() == 'O1h1h':
            continue
        # print(atom1, atom2, '----', getOtherAtom[atom1.name], getOtherAtom[atom2.name])
        dist1 = atom1 - atom2
        dist2 = getOtherAtom[atom1.name] - getOtherAtom[atom2.name]
        # print(abs(dist1-dist2), '\n')
        dists2.append(abs(dist1-dist2))
        if dists2[-1]>.1:
            ii+=1
            continue
        printer('{:6} {:6}: {:5.3f}--{:5.3f}'.format(atom1.name, atom2.name, dists1[ii], dists2[ii]))
        diffs.append(dists1[ii] -dists2[ii])
        ii+=1
    for diff in diffs:
        print(diff)
    print()
    print(np.mean(diffs))
    # for i, atoms in enumerate(iter_atom_pairs(molecule1)):
    #     atom1, atom2 = atoms[0], atoms[1]
    #     if not atom1.get_element() == 'H' and not atom2.get_element() == 'H':
    #         continue
    #     if atom1.get_active_invariom() == 'O1h1h' or atom2.get_active_invariom() == 'O1h1h':
    #         continue
    #     printer('{:6} {:6}: {:5.3f}--{:5.3f}'.format(atom1.name, atom2.name, dists1[i], dists2[i]))


