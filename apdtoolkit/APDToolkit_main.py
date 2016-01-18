
from os.path import expanduser, isfile, join, realpath, dirname
from sys import argv
import lauescript.core.pluginmanager as pluginmanager


def main():
    """
    Creates an instance of the plugin manager and configures is
    appropriately.
    After configuration the plugin manager is executed.
    """
    if 'help' in argv:
        print '\n\n########################################################################################\n'              '#                                       APDToolkit                                     #\n'              '########################################################################################\n'
        print 'A program for estimating hydrogen ADPs from the Invariom databse.'
        print """
Usage:
Plugins are called by using '-' as a prefix for the plugin KEY. e.g.: the Write plugin has the KEY 'W' and can
be started with '-W'. The execution order of plugins is the same as the order of statements on the cmd line.

Options are not prefixed by '-' characters. Every plugin has its own set of options. Some of them require their
own arguments. In these cases the argument is separated from the option with a whitespace character.
Every option is assigned to the plugin specified last on the cmd line when reading the line from left to right.
e.g.: '-A -W write out.res -A' assigns the option 'file' with the parameter 'out.res' to the plugin Write.

The main program accepts two options:
    [help] to print this message.
    [load <arg>] to load a specific crystallographic data file.

Commonly used plugins:
    [T] Perform a TLS fit
    [A] Perform an automatic rigid body segmentation and perform a subsequent segmented rigid body fit.
    [W] Write an output file of the same format as the input file.
    [S] Scale ADPs from different models onto each other.
    [descent] Write an invarioms.descent file.
    [compare] Compare to structure models quantitatively.

Consult the heads of plugin files for detailed plugin information.
Plugins are located as specified in '~/.APDToolkit.ini'

To create a file (out.res' with estimated H-APDs by automatic segmented rigid body analysis use
  >>>   APDToolkit load <fileName> -A -W write out.res   <<<
        """
        exit()
    if not '-D' in argv:
        argvs=argv[0:1]+['-APDToolkit']+argv[1:]
    else:
        argvs = argv
    config_file = expanduser(join('~', '.APDToolkit.ini'))
    if not isfile(config_file):
        from lauescript.makeconfig import run
        run(outputName='~/.APDToolkit.ini',
            data_path=join(dirname(dirname(dirname(dirname(realpath(__file__))))), join('lauescript', 'data')),
            plugin_path=join(dirname(dirname(realpath(__file__))), join('apdtoolkit', 'src')))
    pm = pluginmanager.PluginManager(argvs=argvs,
                                  headline='                              APDToolkit                              ',
                                bottomline='                          Exiting APDToolkit                          ',
                                headlines=False,
                                config=config_file,
                                macro_file=False)
    pm.execute()
    exit()
