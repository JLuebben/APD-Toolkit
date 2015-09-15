
__author__ = ''

KEY = 'APDToolkit'  # Edit this to control which cmd line keyword starts the plugin.
OPTION_ARGUMENTS = {'load': 'myFile.txt'}  # Edit this to define cmd line options for
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

    printer = pluginManager.setup()
    data = DATA()
    loader = Loader(printer)
    pluginManager.register_variable(loader, 'loader')
    pluginManager.register_variable(data, 'data')
    # data.register_pluginManager(pluginManager)
    dabapath = pluginManager.get_databasepath()

    filename = pluginManager.arg('load')
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
        FlexLoad(data, loader, dabapath, pluginManager, filename)
    else:
        FlexLoad(data, loader, dabapath, pluginManager)
    printer('Loading successful.')
    data.update()
    for atom in data['exp'].atoms:
        print atom.get_active_invariom()
