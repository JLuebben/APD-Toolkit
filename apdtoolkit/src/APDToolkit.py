
__author__ = ''

KEY = 'APDToolkit'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt',
                    'temp': None,
                    'planarity': .1}  # Edit this to define cmd line options for
# the plugin and their default values.
from lauescript.core.core import *

def run(pluginManager):
    """
    Asks the plugin manager for user input and executes
    the APD-Toolkit's main functions.
    """
    from lauescript.laueio.inout import FlexLoad
    from lauescript.laueio.loader import Loader
    from lauescript.types.data import DATA
    from os.path import isfile

    printer = pluginManager.setup()
    data = DATA()
    loader = Loader(printer)
    pluginManager.register_variable(loader, 'loader')
    pluginManager.register_variable(data, 'data')
    planarityThreshold = float(pluginManager.arg('planarity'))
    # data.register_pluginManager(pluginManager)
    dabapath = pluginManager.get_databasepath()
    # print(pluginManager.arg('temp'))
    # print(pluginManager.arg('load'))

    filename = pluginManager.arg('load')
    if not isfile(filename):
        filename = None
        printer('No file specified. Searching for files in working directory.'
                '\nTo specify a file use \'load <filename>\'.\n')
    if filename:
        # if filename.endswith('.apd'):
        #     printer('APD-Script file found. Executing script.')
        #     from lauescript.core.scripting import Parser
        #
        #     parser = Parser(filename, indent=5, config=pluginManager)
        #     printer.enter()
        #     parser()
        #     printer.exit()
        #     exit()
        FlexLoad(data, loader, dabapath, pluginManager, filename, planarityThreshold=planarityThreshold)
    else:
        FlexLoad(data, loader, dabapath, pluginManager, planarityThreshold=planarityThreshold)
    printer('Loading successful.')
    data.update()
    # for atom in data['exp'].atoms:
    #     print atom.get_active_invariom()
