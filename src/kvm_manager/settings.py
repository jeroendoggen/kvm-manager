"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""


import os
import ConfigParser
import argparse


class Settings:
    """ Contains all the tools to analyse Blackboard assignments """
    logfile = "kvm_manager.log"
    summary_file = 'summary.log'
    config_file = "settings.conf"
    Config = ConfigParser.ConfigParser()
    Log = ConfigParser.ConfigParser()
    number_of_servers = 0

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
                    DebugPrint("skip: %s" % option)
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

    def get_cli_arguments(self):
        """Read all the cli arguments."""
        args = self.parser.parse_args()
        if (args.s is not None):
            self.servers = args.s
        if (args.l is not None):
            self.logfile = args.l
