"""
    KVM Manager
    Copyright 2014, Jeroen Doggen, jeroendoggen@gmail.com
"""

from __future__ import print_function, division  # We require Python 2.6+

import sys
import os


class Setup():
    """ Setup class: pre-configure the system """
    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger