===========
set_if
===========

May come in handy when you want to set ip adresses in python.

set_if uses ioctl system calls instead of using system commands.

To get available interfaces and information about them I recommend "https://pypi.python.org/pypi/netifaces".

- Usage
To be able to run, you need to execute process with sudo.

	*set_ifadress(iface, ip)*

	ex: **set_ifadress('en1', '192.168.1.1')**


Dependencies
=========

* netifaces


The mother ship
-------------

`drobban <https://github.com/drobban/set_if>`_.
