"""
Command-line interface to the Devicedemo API.
"""

import argparse

from devicedemoclient.v1.api import client as v1_client
from devicedemoclient.v1.api import shell as v1_shell


class DevicedemoClientArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(DevicedemoClientArgumentParser, self).__init__(*args, **kwargs)

    def error(self, message):
        """

        :param message: string the error message
        :return:
        """
        pass

