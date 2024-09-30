import os
from nmap import PortScanner
from .utils import LogHelper
# from .metrics import Metrics


log = LogHelper.get_env_logger(__name__)


class NmapClient(object):
    @classmethod
    def get_client(cls):
        return cls()

    @classmethod
    def get_nmap_scan_host(cls):
        return os.environ.get('NMAP_SCAN_HOST',
                              '127.0.0.1')

    def __init__(self):
        super().__init__()
        self._scanner = PortScanner()

    @property
    def scanner(self):
        return self._scanner
