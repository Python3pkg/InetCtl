__version__ = '0.1'

from .if_ctl import set_ifaddress
from netifaces import interfaces
from netifaces import ifaddresses
from netifaces import gateways
from netifaces import address_families

import sys
import os


if __name__ == '__main__':
    if os.geteuid() != 0:
        os.execvp("sudo", ["sudo"] + sys.argv)

    if_ctl.set_ifadress('en1', '192.168.3.111')
