import os, shutil

from . import common

class OnionShare(object):
    """
    OnionShare is the main application class. Pass in options and run
    start_onion_service and it will do the magic.
    """
    def __init__(self, onion, local_only=False, stay_open=False):

        # The Onion object
        self.onion = onion

        self.hidserv_dir = None
        self.onion_host = None
        self.stealth = None

        # files and dirs to delete on shutdown
        self.cleanup_filenames = []

        # do not use tor -- for development
        self.local_only = local_only

        # automatically close when download is finished
        self.stay_open = stay_open

    def set_stealth(self, stealth):

        self.stealth = stealth
        self.onion.stealth = stealth

    def start_onion_service(self):
        """
        Start the onionshare onion service.
        """

        # Choose a random port
        self.port = common.get_available_port(17600, 17650)

        if self.local_only:
            self.onion_host = '127.0.0.1:{0:d}'.format(self.port)
            return

        self.onion_host = self.onion.start_onion_service(self.port)

        if self.stealth:
            self.auth_string = self.onion.auth_string

    def cleanup(self):
        """
        Shut everything down and clean up temporary files, etc.
        """

        # cleanup files
        for filename in self.cleanup_filenames:
            if os.path.isfile(filename):
                os.remove(filename)
            elif os.path.isdir(filename):
                shutil.rmtree(filename)
        self.cleanup_filenames = []
