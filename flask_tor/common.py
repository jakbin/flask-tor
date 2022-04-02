import base64
import hashlib
import inspect
import os
import platform
import random
import socket
import sys
import time

def set_debug(new_debug):
    global debug
    debug = new_debug

def get_path():
    return os.path.dirname(__file__)

def get_platform():
    """
    Returns the platform OnionShare is running on.
    """
    return platform.system()

def get_resource_path(filename):
    """
    Returns the absolute path of a resource, regardless of whether OnionShare is installed
    systemwide, and whether regardless of platform
    """
    p = get_platform()

    if getattr(sys, 'onionshare_dev_mode', False):
        # Look for resources directory relative to python file
        prefix = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))), 'share')

    elif p == 'Linux' and sys.argv and sys.argv[0].startswith(sys.prefix):
        # OnionShare is installed systemwide in Linux
        prefix = os.path.join(sys.prefix, 'share/onionshare')

    elif getattr(sys, 'frozen', False):
        # Check if app is "frozen"
        # https://pythonhosted.org/PyInstaller/#run-time-information
        if p == 'Darwin':
            prefix = os.path.join(sys._MEIPASS, 'share')
        elif p == 'Windows':
            prefix = os.path.join(os.path.dirname(sys.executable), 'share')

    return os.path.join(prefix, filename)

def get_tor_paths():
    p = get_platform()
    if p == 'Linux':
        tor_path = '/usr/bin/tor'
        tor_geo_ip_file_path = '/usr/share/tor/geoip'
        tor_geo_ipv6_file_path = '/usr/share/tor/geoip6'
    elif p == 'Windows':
        base_path = os.path.join(os.path.dirname(os.path.dirname(get_resource_path(''))), 'tor')
        tor_path               = os.path.join(os.path.join(base_path, 'Tor'), "tor.exe")
        tor_geo_ip_file_path   = os.path.join(os.path.join(os.path.join(base_path, 'Data'), 'Tor'), 'geoip')
        tor_geo_ipv6_file_path = os.path.join(os.path.join(os.path.join(base_path, 'Data'), 'Tor'), 'geoip6')
    elif p == 'Darwin':
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(get_resource_path(''))))
        tor_path               = os.path.join(base_path, 'Resources', 'Tor', 'tor')
        tor_geo_ip_file_path   = os.path.join(base_path, 'Resources', 'Tor', 'geoip')
        tor_geo_ipv6_file_path = os.path.join(base_path, 'Resources', 'Tor', 'geoip6')

    return (tor_path, tor_geo_ip_file_path, tor_geo_ipv6_file_path)

def random_string(num_bytes, output_len=None):
    """
    Returns a random string with a specified number of bytes.
    """
    b = os.urandom(num_bytes)
    h = hashlib.sha256(b).digest()[:16]
    s = base64.b32encode(h).lower().replace(b'=', b'').decode('utf-8')
    if not output_len:
        return s
    return s[:output_len]

def human_readable_filesize(b):
    """
    Returns filesize in a human readable format.
    """
    thresh = 1024.0
    if b < thresh:
        return '{0:.1f} B'.format(b)
    units = ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    u = 0
    b /= thresh
    while b >= thresh:
        b /= thresh
        u += 1
    return '{0:.1f} {1:s}'.format(round(b, 1), units[u])

def format_seconds(seconds):
    """Return a human-readable string of the format 1d2h3m4s"""
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    human_readable = []
    if days:
        human_readable.append("{:.0f}d".format(days))
    if hours:
        human_readable.append("{:.0f}h".format(hours))
    if minutes:
        human_readable.append("{:.0f}m".format(minutes))
    if seconds or not human_readable:
        human_readable.append("{:.0f}s".format(seconds))
    return ''.join(human_readable)

def estimated_time_remaining(bytes_downloaded, total_bytes, started):
    now = time.time()
    time_elapsed = now - started  # in seconds
    download_rate = bytes_downloaded / time_elapsed
    remaining_bytes = total_bytes - bytes_downloaded
    eta = remaining_bytes / download_rate
    return format_seconds(eta)

def get_available_port(min_port, max_port):
    """
    Find a random available port within the given range.
    """
    with socket.socket() as tmpsock:
        while True:
            try:
                tmpsock.bind(("127.0.0.1", random.randint(min_port, max_port)))
                break
            except OSError:
                pass
        _, port = tmpsock.getsockname()
    return port
