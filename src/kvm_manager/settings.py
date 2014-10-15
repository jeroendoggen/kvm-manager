"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""


import ConfigParser
import argparse
import sys


class Actions:
    create = False
    start = False
    stop = False
    delete = False
    destroy = False
    listen = False


class Settings:
    """ Contains all the tools to analyse Blackboard assignments """
    logfile = "kvm_manager.log"
    summary_file = 'summary.log'
    config_file = "settings.conf"
    Config = ConfigParser.ConfigParser()
    Log = ConfigParser.ConfigParser()
    number_of_servers = 0
    source_image = 0
    actions = Actions()
    servers = 0

    parser = argparse.ArgumentParser(
        prog="kvm_manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="KVM Manager commandline arguments:",
        epilog="Report bugs to jeroendoggen@gmail.com.")

    def __init__(self):
        self.read_config_file(self.config_file)
        self.cli_arguments()

    def config_section_map(self, section):
        """ Helper function to read config settings """
        dict1 = {}
        options = self.Config.options(section)
        for option in options:
            try:
                dict1[option] = self.Config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
                sys.exit(1)
        return dict1

    def read_config_file(self, filename):
        """ Read the config  """
        try:
            self.Config.read(filename)
            self.number_of_servers = int(self.config_section_map("Config")['number_of_servers'])
            self.source_image = self.config_section_map("FileNames")['source_image']

        except AttributeError:
            #TODO: this does not work!! (AttributeError or KeyError needed? both?)
            print("Error while processing config file")
            sys.exit(1)

    def cli_arguments(self):
        """Configure a read all the cli arguments."""
        self.configure_cli_arguments()
        self.get_cli_arguments()

    def configure_cli_arguments(self):
        """Configure all the cli arguments."""
        self.parser.add_argument("-s", metavar="servers",
          help="Number of servers to create")
        self.parser.add_argument('-l', metavar='logfile',
          help="Set the name the logfile to use")

        self.parser.add_argument('--create', action='store_true', help='Create the virtual machine clones')
        self.parser.add_argument('--start', action='store_true', help='Start the virtual machines')
        self.parser.add_argument('--stop', action='store_true', help='Stop the virtual machines')
        self.parser.add_argument('--delete', action='store_true', help='Delete the virtual machines')
        self.parser.add_argument('--destroy', action='store_true', help='Kill the power to the virtual machines')
        self.parser.add_argument('--listen', action='store_true', help='Listen for virtual machines (to detect them after booting')

    def get_cli_arguments(self):
        """Read all the cli arguments."""
        args = self.parser.parse_args()
        if (args.s is not None):
            self.servers = args.s
        if (args.l is not None):
            self.logfile = args.l

        if (args.create is True):
            self.actions.create = True
        if (args.start is True):
            self.actions.start = True
        if (args.stop is True):
            self.actions.stop = True
        if (args.delete is True):
            self.actions.delete = True
        if (args.destroy is True):
            self.actions.destroy = True
        if (args.listen is True):
            self.actions.listen = True
