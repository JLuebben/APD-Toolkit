__author__ = 'jens'

from lauescript.cryst.iterators import iter_atom_pairs

KEY = 'restrain'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'write': 'restraints.txt'}  # Edit this to define cmd line options for


def run(pluginManager):
    """
    This is the entry point for the plugin manager.
    The plugin manager will pass a reference to itself
    to the function.
    Use the APD_Printer instance returned by
    pluginManager.setup() instead of the 'print'
    statement to generate autoformated cmd line output.
    :param pluginManager: Reference to the plugin manager
    instance.
    """
    global printer
    printer = pluginManager.setup()
    data = pluginManager.get_variable('data')
    molecule = data['exp']
    printer.table(['Atom 1', 'Atom 2', 'Type', 'Distance'], head=True)
    restraints = RestraintManager()
    for atom1, atom2 in iter_atom_pairs(molecule, bound=False):
        if atom1.get_element() == 'H' or atom2.get_element() == 'H':
            continue
        value = getBondNumber(atom1, atom2)
        if value:
            r = Restraint(value, atom1-atom2, atom1, atom2, 'exp')
            printer.table('{:7>},{:7<},1-{},{:5.3f}'.format(atom1.get_name(),
                                                            atom2.get_name(),
                                                            value+1,
                                                            atom1-atom2).split(','))

            restraints.add(atom1, atom2, r)
    printer.table(done=True)
    restraints = RestraintManager()
    for molecule in data.values():
        for atom1, atom2 in iter_atom_pairs(molecule, bound=False):
            if atom1.get_element() == 'H' or atom2.get_element() == 'H':
                continue
            value = getBondNumber(atom1, atom2)
            if value:
                restraints.add(atom1, atom2, Restraint(value,
                                                       atom1.cartDistance(atom2),
                                                       atom1,
                                                       atom2,
                                                       modelCompound=molecule.name))

    restraintList = restraints.harvestRestraints()
    restraints.selfSum()
    bondMap = restraints.mapBonds(restraintList)
    with open(pluginManager.arg('write'), 'w') as fp:
        fp.write(''.join([str(r) for r in bondMap.keys()]))

    printer()
    printer.spacer()
    printer('\n{} written.'.format(pluginManager.arg('write')))
    printer('\nAdd \'+{}\' to your shelxl instruction file\'s header.'.format(pluginManager.arg('write')))


class Restraint(object):
    ESDs = {1: 0.01,
            2: 0.02,
            3: 0.05}
    Prefixes = {1: 'DFIX',
                2: 'DANG',
                3: 'DANG'}

    @staticmethod
    def setESD(type, value):
        Restraint.ESDs[type] = value

    def __init__(self, type, distance, atom1, atom2, modelCompound=''):
        self.type = type
        self.distance = distance
        self.atom1 = atom1
        self.atom2 = atom2
        self.modelCompound = modelCompound
        self.string = ''
        self.makeString()

    def setDistance(self, value):
        self.distance = value

    def makeString(self, modelCompound=None):
        self.string = '\n{prefix} {dist:5.3f} {esd:5.3f} {name1} {name2}'.format(prefix=Restraint.Prefixes[self.type],
                                                                                 dist=self.distance,
                                                                                 esd=Restraint.ESDs[self.type],
                                                                                 name1=self.atom1.get_name(),
                                                                                 name2=self.atom2.get_name(),)
        if not self.modelCompound == 'exp':
            self.string += '  ! {}'.format(self.modelCompound)
        if modelCompound:
            self.string += '  ! {}'.format(modelCompound)

    def __str__(self):
        return self.string


class RestraintManager(object):
    def __init__(self):
        self.restraints = {}

    def add(self, atom1, atom2, restraint):
        self._add(self.hashBond(atom1, atom2, restraint.modelCompound), restraint)

    def _add(self, key, value):
        try:
            self.restraints[key].append(value)
        except KeyError:
            self.restraints[key] = [value]

    def __getitem__(self, item):
        return self.restraints[self.hashBond(item[0], item[1], item[2])]

    @staticmethod
    def hashBond(atom1, atom2, modelCompound=''):
        return ','.join(sorted([atom1.get_name(), atom2.get_name()])+[modelCompound])

    @staticmethod
    def sum(restraints):
        bType = restraints[0].type
        distance = sum([restraint.distance for restraint in restraints]) / float(len(restraints))
        atom1 = restraints[0].atom1
        atom2 = restraints[0].atom2
        modelCompound = {restraint.modelCompound for restraint in restraints}
        modelCompound = ' & '.join(modelCompound)
        return Restraint(bType, distance, atom1, atom2, modelCompound)

    def harvestDict(self):
        return {key: self.sum(value) for key, value in self.restraints.items()}

    def harvestRestraints(self):
        rDict = self.harvestDict()
        rList = sorted(rDict.items(), key=lambda pair: pair[0])
        return [pair[1] for pair in rList]

    def getFittingRestraints(self, atom1, element2, modelCompound, type, distance, threshold=0.1, scaling=1.5):
        """
        Searchs the model compound of atom1 for suitable distance restraints taking bond type measured distance and
        elements into account.
        :param atom1: ATOM. All distances involving atom1 are searched for matches.
        :param element2: String. Element symbol of the bond partner of atom1.
        :param modelCompound: String. Name of the model compound searched for suitable restraints.
        :param type: Int. Identifier for the distance type. 1=1-2 distance, 2=1-3 distance, 3=1-4 distance. etc.
        :param distance: Float. Bond distance of the measured bond. (Or 1-3 or 1-4 distance.)
        :param threshold: Float. Only bond distances that differ from the measured distances by less than threshold are
        used for restraints. Threshold gets modified depending on the values of type and scaling. Defaults to 0.1
        :param scaling: Float. Threshold gets multiplied by type**scaling to account for lower accuracies of
        1-3 and 1-4 distances. Defaults to 1.5
        :return: list(Restraint). List of all suitable restraints from the given model compound.
        """
        threshold *= type**scaling
        compoundRestraints = [self.restraints[key] for key in self.restraints.keys() if key.endswith(','+modelCompound)]
        compoundRestraints = [r for r in compoundRestraints if r.type == type]
        elements = {atom1.get_element(), element2}
        return [r for r in compoundRestraints
                if len({r.atom1.get_element(), r.atom2.get_element()}.intersection(elements)) == 2 and
                r.distance - distance <= threshold]

    def selectRestraints(self, reference, selection):
        best = (999, None)
        for r in selection:
            diff = abs(r.distance - reference.distance)
            if diff < best[0]:
                best = (diff, r)
        return best[1]

    def selfSum(self):
        self.restraints = self.harvestDict()

    def merge(self, restraints):
        return self.sum(restraints)
        grouped = {}
        for r in restraints:
            h = self.hashBond(r.atom1, r.atom2, '')
            try:
                grouped[h].append(r)
            except KeyError:
                grouped[h] = [r]
        return [self.sum(r) for r in grouped.values()]

    def mapBonds(self, l):
        printer()
        printer.spacer()
        printer('\nMapping bonds to model compounds.')
        bondMap = {}
        for r in l:
            if not r.modelCompound == 'exp':
                continue
            try:
                _ = r.atom1.invariom.name
                _ = r.atom2.invariom.name
            except AttributeError:
                pass
            else:
                fitting = self.getFittingRestraints(r.atom1.invariom,
                                                    r.atom2.get_element(),
                                                    r.atom1.invariom.molecule.name,
                                                    r.type,
                                                    r.distance)
                fitting += self.getFittingRestraints(r.atom2.invariom,
                                                     r.atom1.get_element(),
                                                     r.atom2.invariom.molecule.name,
                                                     r.type,
                                                     r.distance)
                if not fitting:
                    continue
                selected = self.sum(fitting)
                if selected:
                    printer('\nSelected: {}'.format(str(selected)[1:]))
                    r.setDistance(selected.distance)
                    printer('Model:    {}'.format(str(r)[1:]))
                    r.makeString(modelCompound=selected.modelCompound)
                    printer('Ideal:    {}'.format(str(r)[1:]))
                    bondMap[str(r)] = selected
                else:
                    printer('\nNot found Model: {}    1-{}'.format(str(r)[1:], r.type+1))
        return bondMap


def getBondNumber(atom1, atom2, maxDepth=3, currentDepth=1, blacklist=None):
    """
    Returns the number of bonds that are between atom1 and atom2 or zero if the number
    of bonds is larger than maxDepth.
    :param atom1: ATOM instance.
    :param atom2: ATOM instance.
    :param maxDepth: Int: Maximum number of bonds analyzed.
    :param currentDepth: For recursive function calls only.
    :param blacklist: For recursive function calls only.
    :return: Int: Number of bonds between atom1 and atom2.
    """
    if not blacklist:
        blacklist = [atom1]
    if currentDepth == maxDepth+1:
        return 0
    currentDepth += 1
    for atom1a in atom1.iter_bound_atoms():
        if atom1a in blacklist:
            continue
        blacklist.append(atom1a)
        if atom1a == atom2:
            return currentDepth - 1
        else:
            value = getBondNumber(atom1a, atom2, maxDepth=maxDepth, currentDepth=currentDepth, blacklist=blacklist)
            if value:
                return value
    return 0
