# -*- mode: python -*-


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
                               'lauescript.cryst.iterators',
                               'lauescript.cryst.transformations',
                               'lauescript.cryst.rings',
                               'lauescript.cryst.cif',
                               'lauescript.cryst.sort',
                               'lauescript.cryst.geom',
                               'lauescript.cryst.flexmatch',
                               'lauescript.cryst.filter',
                               'lauescript.cryst.crystgeom',
                               'lauescript.cryst.symmetry',
                               'lauescript.cryst.harmonysearch',
                               'lauescript.cryst.invarioms',
                               'lauescript.cryst.match',
                               'lauescript.cryst.tables',
                               'lauescript.cryst.molgraph',
                               'lauescript.laueio.pdb_iop',
                               'lauescript.laueio.cif_iop',
                               'lauescript.laueio.pdb_iop',
                               'lauescript.laueio.shelxl_iop',
                               'lauescript.laueio.inout',
                               'lauescript.laueio.loader',
                               'lauescript.laueio.io',
                               'lauescript.laueio.xd_iop',
                               'lauescript.types.adp',
                               'lauescript.types.molecule',
                               'lauescript.types.data',
                               'lauescript.types.atom',
                               'lauescript.invstring2',
                               'lauescript.database',
                               'lauescript.makeconfig',
                               'lauescript.core.scripting',
                               'lauescript.core.pluginmanager',
                               'lauescript.core.error',
                               'lauescript.core.core',
                               'lauescript.core.apd_printer',
                               'lib2to3',
                               'networkx']



a = Analysis(['bin/APDToolkit'],
             pathex=['/home/jens/LS/projects/APD-Toolkit'],
             hiddenimports=hiddenimports,
             hookspath=['./apdtoolkit/'],
             runtime_hooks=None,
             datas=[('./Grammar.txt', 'lib2to3'),
                    ('./PatternGrammar.txt', 'lib2to3')])
#a.datas += [('lib2to3', '/usr/lib64/python2.7/lib2to3/Grammar.txt', 'DATA')]
#a.datas += [('/usr/lib64/python2.7/lib2to3/Grammar.txt', '.')]
#a.datas += [('/usr/lib64/python2.7/lib2to3/Grammar.txt', './lib2to3/')]
#a.binaries = [x for x in a.binaries if not x[0].startswith('networkx')]
#a.binaries = [x for x in a.binaries if not 'lib2to3' in x[0]]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='apdtoolkit',
          debug=False,
          strip=None,
          upx=True,
          console=True )
