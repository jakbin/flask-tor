import os, shutil

from . import common

class OnionStart(object):
    """
    OnionShare is the main application class. Pass in options and run
    start_onion_service and it will do the magic.
    """
    def __init__(self, onion, local_only=False, stay_open=False, persistent_key_file=None, reuse_key=True):
        """
        Args:
            onion (Onion): The Onion controller object.
            local_only (bool): If True, only bind to localhost (no Tor).
            stay_open (bool): Unused, for compatibility.
            persistent_key_file (str, optional): Path to file for saving/loading the onion service private key. If provided, the same onion address will be reused across runs (unless reuse_key is False).
            reuse_key (bool, optional): If True (default), reuse the key in persistent_key_file for the onion address. If False, always generate a new address and overwrite the file.
        """
        # The Onion object
        self.onion = onion
        self.hidserv_dir = None
        self.onion_host = None
        self.stealth = None
        self.local_only = local_only
        # Path to store/load persistent onion private key (text file containing 'ED25519-V3:...' format)
        self.persistent_key_file = os.path.expanduser(persistent_key_file) if persistent_key_file else None
        print(self.persistent_key_file)
        self.reuse_key = reuse_key

    def start_onion_service(self):
        """
        Start the onionshare onion service.
        """

        # Choose a random port
        self.port = common.get_available_port(17600, 17650)

        if self.local_only:
            self.onion_host = '127.0.0.1:{0:d}'.format(self.port)
            return

        existing_key = None
        if self.persistent_key_file and self.reuse_key and os.path.exists(self.persistent_key_file):
            try:
                with open(self.persistent_key_file, 'r') as f:
                    existing_key = f.read().strip() or None
            except Exception:
                existing_key = None

        self.onion_host = self.onion.start_onion_service(self.port, existing_key=existing_key)

        # Save newly generated key if we didn't reuse one
        if self.persistent_key_file and (self.onion.private_key is not None):
            # Only save if either no existing file or we generated a new key
            if (not existing_key) or (existing_key and existing_key != self.onion.private_key):
                try:
                    parent_dir = os.path.dirname(self.persistent_key_file)
                    if parent_dir:
                        os.makedirs(parent_dir, exist_ok=True)
                    with open(self.persistent_key_file, 'w') as f:
                        f.write(self.onion.private_key)
                except Exception as e:
                    print(f"[flask-tor] Failed to save persistent key file '{self.persistent_key_file}': {e}")

        if self.stealth:
            self.auth_string = self.onion.auth_string

