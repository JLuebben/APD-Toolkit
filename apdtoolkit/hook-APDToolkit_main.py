"""
hook file for pyinstaller.
This file is executed when building the APD-Toolkit.
Plugins need to be included even when distributed as an external data package to make sure that all dependencies
are packaged correctly. The overhead from efectivly including the plugin source files twice is neglectable.
"""
import os
plugins = ['apd.' + name[:-3] for name in os.listdir(__file__[:-12] + '/plugins/') if name.endswith('.py')]
lib = ['apd.lib.crystgeom2.' + name[:-3] for name in os.listdir(__file__[:-12] + '/lib/crystgeom2/') if name.endswith('.py')] + \
      ['apd.lib.' + name[:-3] for name in os.listdir(__file__[:-12] + '/lib/') if name.endswith('.py')]

hiddenimports = hiddenimports=['sklearn.neighbors.typedefs',
                               'sklearn.utils.sparsetools._graph_validation',
                               'sklearn.utils.sparsetools._graph_tools',
                               'sklearn.utils.lgamma',
                               'scipy.special._ufuncs_cxx',
                               'lauescript',
                               'lauescript.core',
                               'lauescript.laueio',
                               'lauescript.types',
                               'lauescript.data',
                               'lauescript.cryst',
                               'lauescript.cryst.iterators'] + plugins + lib
