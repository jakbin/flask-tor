from .onion import *
from .onionstart import OnionStart
import sys, threading

def run_with_tor():
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
        app_tor = OnionStart(onion)
        # app_tor.set_stealth(stealth)
        app_tor.start_onion_service()
    except KeyboardInterrupt:
        print("")
        sys.exit()

    print(f" * Running on http://{app_tor.onion_host}")
    return app_tor.port

