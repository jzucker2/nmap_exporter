import os
from .utils import LogHelper
# from .version import version
# from .metrics import Metrics
from .nmap_client import NmapClient


log = LogHelper.get_env_logger(__name__)


DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS = int(os.environ.get(
    'DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS',
    60))


class ScraperException(Exception):
    pass


class MissingIPListScraperException(ScraperException):
    pass


class Scraper(object):
    @classmethod
    def get_client(cls):
        return cls(NmapClient.get_client())

    @classmethod
    def default_nmap_ip(cls):
        # TODO: consolidate env imports
        return os.environ.get('DEFAULT_WLED_IP',
                              "10.0.1.179")

    @classmethod
    def get_default_scrape_interval(cls):
        return int(DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS)

    def __init__(self, nmap_client):
        self._nmap_client = nmap_client

    @property
    def nmap_client(self):
        return self._nmap_client
