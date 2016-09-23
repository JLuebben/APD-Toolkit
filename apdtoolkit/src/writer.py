"""
Created on 08.02.2014

@author: Jens Luebben


Plugin for writing the results of the ADP transfer to a file.
The file format depends on the format used as input.
"""

from lauescript.types.adp import ADPDataError

KEY = 'W'
OPTION_ARGUMENTS = {'write': 'apd',
                    'use': 'cart_sum'}


def run(conf):
    """
    Called by the plugin manager.
    Asks the plugin manager for user input and calls
    the appropriate functions.
    :param conf: reference to the plugin manager.
    """
    global config
    config = conf
    printer = config.setup()

    filename = config.arg('write')
    if not filename:
        filename = 'apd'

    loader = config.get_variable('loader')
    writer = loader.get_write_copy(filename)

    attr = ['cart',
            'adp_cart',
            'afix']
    writer.set(attr, provide)

    writer.write()
    printer('File \'{}\' written'.format(filename))


def provide():
    """
    Generator for passing parameters to the IOP.
    This function is passed as an argument to the
    IOP. The IOP iterates of this function to
    overwrite its internal data based on the return
    values of this function.
    """
    use = config.arg('use')
    printer = config.get_active_printer()
    printer('Using {} for H-ADPs'.format(use[-3:]))
    data = config.get_variable()
    allA = config.arg('all')
    for atom in data['exp'].atoms:
        if atom.is_updated() or not atom.get_element() == 'H':
            if not atom.get_element() == 'H':
                if allA:
                    yield atom.name, atom.cart, atom.adp[use], ''
                    continue
                else:
                    yield atom.name, atom.cart, atom.adp['cart_meas'], ''
                    continue
            afix = ''
            if atom.get_element() == 'H':
                afix = 'AFIX 2'
            try:
                adp = atom.adp[use]
            except ADPDataError:
                printer('Warning: No estimated ADP available for atom {}'.format(atom.get_name()))
                printer('Using measured ADP instead.')
                adp = atom.adp['cart_meas']
            yield atom.name, atom.cart, adp, afix
            continue

        else:
            yield atom.name, atom.cart, atom.adp['cart_meas'], ''
