from .onion import *
from .onionstart import OnionStart
import sys, threading, os

def run_with_tor(persistent_key_file=None, reuse_key=True):
    """
    Start Flask app with Tor hidden service.

    Args:
        persistent_key_file (str, optional): Path to a file for saving/loading the onion service private key. If provided, the same onion address will be reused across runs (unless reuse_key is False). If None, a new address is generated each run.
        reuse_key (bool, optional): If True (default), reuse the key in persistent_key_file for the onion address. If False, always generate a new address and overwrite the file.

    Returns:
        int: The port number to use for the Flask app.
    """
    # Start the Onion object
    onion = Onion()
    try:
        onion.connect()
    except (TorTooOld, TorErrorInvalidSetting, TorErrorAutomatic, TorErrorSocketPort, TorErrorSocketFile, TorErrorMissingPassword, TorErrorUnreadableCookieFile, TorErrorAuthError, TorErrorProtocolError, BundledTorNotSupported, BundledTorTimeout) as e:
        sys.exit(e.args[0])
    except KeyboardInterrupt:
        print("")
        sys.exit()

    # Start the onionshare app
    try:
        app_tor = OnionStart(onion, persistent_key_file=persistent_key_file, reuse_key=reuse_key)
        # app_tor.set_stealth(stealth)
        app_tor.start_onion_service()
    except KeyboardInterrupt:
        print("")
        sys.exit()

    print(f" * Running on http://{app_tor.onion_host}")
    return app_tor.port

