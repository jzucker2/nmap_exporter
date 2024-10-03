import asyncio
import os
from .utils import LogHelper
from .version import version
from .metrics import Metrics
from .nmap_client import NmapClient


log = LogHelper.get_env_logger(__name__)


DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS = int(os.environ.get(
    'DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS',
    3600))


class ScraperException(Exception):
    pass


class MissingIPListScraperException(ScraperException):
    pass


def scan_host_callback(host, hostname, state):
    pass


class Scraper(object):
    @classmethod
    def get_client(cls, scan_host_callback=None):
        if not scan_host_callback:
            scan_host_callback = scan_host_callback
        return cls(NmapClient.get_client())

    @classmethod
    def get_default_scrape_interval(cls):
        return int(DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS)

    def __init__(self, nmap_client):
        self._nmap_client = nmap_client

    @property
    def nmap_client(self):
        return self._nmap_client

    def scrape_self(self):
        with Metrics.SCRAPER_SCRAPE_SELF_EXCEPTIONS.count_exceptions():
            with Metrics.SCRAPER_SCRAPE_SELF_TIME.time():
                current_version = version
                log.debug(f'scrape_self current_version: {current_version}')
                nmap_version_info = self.nmap_client.get_version()
                log.debug(f'scrape_self current_version: {current_version} '
                          f'with nmap_version_info: {nmap_version_info}')
                Metrics.NMAP_INSTANCE_INFO.labels(
                    version=current_version,
                    nmap_version=nmap_version_info.nmap_version or "",
                    nmap_subversion=nmap_version_info.nmap_subversion or "",
                ).set(1)

    async def scrape_scan_host(self, scan_host):
        await asyncio.sleep(0)
        with Metrics.SCRAPER_SCRAPE_SCAN_HOST_EXCEPTIONS.labels(
            scan_host=scan_host,
        ).count_exceptions():
            with Metrics.SCRAPER_SCRAPE_SCAN_HOST_TIME.labels(
                scan_host=scan_host,
            ).time():
                log.info(f"nmap scanning scan_host: {scan_host}")
                await self.nmap_client.scan(scan_host)

    async def scrape_local_scan_host(self):
        scan_host = self.nmap_client.get_local_scan_host()
        await self.scrape_scan_host(scan_host)

    async def scrape_default_scan_host(self):
        scan_host = self.nmap_client.get_nmap_default_scan_host()
        await self.scrape_scan_host(scan_host)

    async def perform_full_scrape(self):
        # first scrape self info for this app
        log.debug('perform_full_scrape')
        self.scrape_self()
        log.debug('done with scrape self now scrape default scan host')
        # then scrape all wled instances
        await self.scrape_default_scan_host()
        log.debug('done with scraping default scan host')
