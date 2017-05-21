import sys
import fcntl
import struct
import socket
import ctypes

if sys.platform == 'darwin':
    from . import bsd_ifreqioctls as ioctls
else:
    from . import linux_ifreqioctls as ioctls

# Buffer constants
IFNAMESIZE = 16


class sockaddr_gen(ctypes.Structure):
    _fields_ = [("sa_family", ctypes.c_uint16),
                ("sa_data", (ctypes.c_uint8 * 22))]


class in_addr(ctypes.Structure):
    # AF_INET / IPv4
    _pack_ = 1
    _fields_ = [("s_addr", ctypes.c_uint32)]


class sockaddr_in(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("sin_family", ctypes.c_ushort),
                ("sin_port", ctypes.c_ushort),
                ("sin_addr", in_addr),
                ("sin_zero", (ctypes.c_uint8 * 16))]


class in6_u(ctypes.Union):
    # AF_INET6 / IPv6
    _pack_ = 1
    _fields_ = [("u6_addr8", (ctypes.c_uint8 * 16)),
                ("u6_addr16", (ctypes.c_uint16 * 8)),
                ("u6_addr32", (ctypes.c_uint32 * 4))]


class in6_addr(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("in6_u", in6_u)]


class sockaddr_in6(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("sin6_family", ctypes.c_short),
                ("sin6_port", ctypes.c_ushort),
                ("sin6_flowinfo", ctypes.c_uint32),
                ("sin6_addr", in6_addr),
                ("sin6_scope_id", ctypes.c_uint32)]


class sockaddr_dl(ctypes.Structure):
    # AF_LINK / BSD|OSX
    _fields_ = [("sdl_len", ctypes.c_uint8),
                ("sdl_family", ctypes.c_uint8),
                ("sdl_index", ctypes.c_uint16),
                ("sdl_type", ctypes.c_uint8),
                ("sdl_nlen", ctypes.c_uint8),
                ("sdl_alen", ctypes.c_uint8),
                ("sdl_slen", ctypes.c_uint8)]


class sockaddr(ctypes.Union):
    _pack_ = 1
    _fields_ = [('gen', sockaddr_gen),
                ('in4', sockaddr_in),
                ('in6', sockaddr_in6)]


class ifmap(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('mem_start', ctypes.c_ulong),
                ('mem_end', ctypes.c_ulong),
                ('base_addr', ctypes.c_ushort),
                ('irq', ctypes.c_ubyte),
                ('dma', ctypes.c_ubyte),
                ('port', ctypes.c_ubyte)]


class ifr_data(ctypes.Union):
    _pack_ = 1
    _fields_ = [('ifr_addr', sockaddr),
                ('ifr_dstaddr', sockaddr),
                ('ifr_broadaddr', sockaddr),
                ('ifr_netmask', sockaddr),
                ('ifr_hwaddr', sockaddr),
                ('ifr_flags', ctypes.c_short),
                ('ifr_ifindex', ctypes.c_int),
                ('ifr_ifqlen', ctypes.c_int),
                ('ifr_metric', ctypes.c_int),
                ('ifr_mtu', ctypes.c_int),
                ('ifr_map', ifmap),
                ('ifr_slave', (ctypes.c_ubyte*IFNAMESIZE)),
                ('ifr_newname', (ctypes.c_ubyte*IFNAMESIZE)),
                ('ifr_data', ctypes.c_void_p)]


class ifreq(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('ifr_name', (ctypes.c_ubyte * IFNAMESIZE)),
                ('data', ifr_data)]


def set_ifaddress(iface, ip):
    # bin_ip = socket.inet_aton(ip)

    ifr = ifreq()
    ifr.ifr_name = (ctypes.c_ubyte * IFNAMESIZE)(*bytearray(iface))

    sin4 = sockaddr()
    sin4.in4.sin_family = socket.AF_INET
    s_addr_data = socket.inet_pton(socket.AF_INET, ip)
    sin4.in4.sin_addr.s_addr = struct.unpack('<L', s_addr_data)[0]

    ifr.data.ifr_addr = sin4

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fcntl.ioctl(sock, ioctls.SIOCSIFADDR, ifr)
