"""
Created on Feb 12, 2014

@author: Jens Luebben

Module for generating a micro database file based on an ONIOM
calculation.
"""
KEY = 'micro'
OPTION_ARGUMENTS = {'load': None,
                    'cluster': 15,
                    'temp': None,
                    'match': 'geom'}
HEADLINE = ' Using micro mode  '
BOTTOMLINE = ' Exiting micro mode'

from lauescript.types.data import DATA
from lauescript.core.core import quickLoad, apd_exit


def run(pluginManager):
    """
    Called by the plugin manager.
    Asks the plugin manager for user input and
    configures the database generator to generate
    the desired database file.
    """
    import lauescript.database as db
    from lauescript.types.data import GENERATOR
    from lauescript.laueio.inout import FlexLoad
    from lauescript.laueio.loader import Loader
    from lauescript.core.core import apd_exit

    printer = pluginManager.setup()
    data = DATA()
    loader = Loader(printer)
    pluginManager.register_variable(loader, 'loader')
    pluginManager.register_variable(data, 'data')
    dabapath = '.'
    match = pluginManager.arg('match')
    if pluginManager.arg('generate'):
        printer('Generating new micro database.')
        data = GENERATOR([], True)
        path = pluginManager.arg('load')
        db.generate_micro_database(data, pluginManager.get_frequency_cutoff(), path=path,
                                   printer=printer, clustersize=int(pluginManager.arg('cluster')),
                                   frequency_scale=pluginManager.get_config_valueFloat('Database', 'frequency_scale'))
        apd_exit(0)
    data = pluginManager.get_variable()
    printer('Loading data.')
    filename = pluginManager.arg('load')
    printer('Setting ADP transfer mode to pattern matching.\n')
    loader = Loader(printer)
    pluginManager.register_variable(loader, 'loader')
    if filename:
        if '.apd' in filename:
            printer('APD-Script file found. Executing script.')
            from lauescript.scripting import Parser

            parser = Parser(filename, indent=5)
            printer.enter()
            parser()
            printer.exit()
            apd_exit()
        FlexLoad(data, loader, dabapath, pluginManager, filename, noTransfer=True)
        # data['exp'] = quickLoad(pluginManager, filename)
    else:
        FlexLoad(data, loader, dabapath, pluginManager, noTransfer=True)
        # data['exp'] = quickLoad(pluginManager, filename)
    printer('Loading successful.')
    printer.spacer()
    printer('\nUsing option {} to transfer ADPs.'.format(match))
    data.update(match=match)