import asyncio
import os
from collections import namedtuple
from nmap import PortScanner
from .utils import LogHelper
from .metrics import Metrics


log = LogHelper.get_env_logger(__name__)


NmapVersionInfo = namedtuple(
    "NmapVersionInfo",
    ["nmap_version", "nmap_subversion"]
)


class NmapClient(object):
    @classmethod
    def get_client(cls):
        return cls()

    @classmethod
    def get_local_scan_host(cls):
        return '127.0.0.1'

    @classmethod
    def get_nmap_default_scan_host(cls):
        return os.environ.get('NMAP_DEFAULT_SCAN_HOST',
                              '10.0.0.0/24')

    @classmethod
    def get_nmap_default_scan_port_range(cls):
        return os.environ.get('NMAP_DEFAULT_SCAN_PORT_RANGE',
                              '22-443')

    @classmethod
    def get_nmap_default_scan_timeout_seconds(cls):
        return int(os.environ.get('NMAP_DEFAULT_SCAN_TIMEOUT_SECONDS',
                                  300))

    def __init__(self):
        super().__init__()
        self._scanner = PortScanner()

    @property
    def scanner(self) -> PortScanner:
        return self._scanner

    def get_version(self) -> NmapVersionInfo:
        try:
            version, subversion = self.scanner.nmap_version()
            return NmapVersionInfo(str(version), str(subversion))
        except Exception as e:
            log.error(f'nmap trying to get version, got e: {e}')
            return (None, None)

    def default_scanner_callback(self, host, scan_result):
        log.info('+++++++++++++++++++++++++++++++++++++++')
        log.info(f'default_scanner_callback => '
                 f'host: {host}, scan_result: {scan_result}')
        self._parse_scan_result(scan_result)

    def _parse_scan_result(self, scan_result):
        log.info(f'scan_result: {scan_result}')
        log.info(f'scan command_line: {self.scanner.command_line()}')
        for host in self.scanner.all_hosts():
            log.info('----------------------------------------------------')
            log.info(f'Host : {host} ({self.scanner[host].hostname()})')
            log.info(f'State : {self.scanner[host].state()}')
            for proto in self.scanner[host].all_protocols():
                log.info('----------')
                log.info(f'Protocol : {proto}')
                lport = self.scanner[host][proto].keys()
                lport.sort()
                for port in lport:
                    port_state = self.scanner[host][proto][port]['state']
                    log.info(f'port : {port}\tstate : {port_state}')

    def _scan(self, host, port_range=None):
        if not port_range:
            port_range = self.get_nmap_default_scan_port_range()
        log.info(f'Going to scan host: {host} with port_range: {port_range}')
        scan_result = self.scanner.scan(
            hosts=host,
            ports=port_range,
            timeout=self.get_nmap_default_scan_timeout_seconds(),
        )
        self._parse_scan_result(scan_result)

    async def scan(self, scan_host):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        await asyncio.sleep(0)
        Metrics.NMAP_CLIENT_SCAN_HOST_COUNTER.labels(
            scan_host=scan_host,
        ).inc()
        log.info(f"nmap scanning scan_host: {scan_host}")
        self._scan(scan_host)

    async def scan_default_host(self):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        scan_host = self.get_nmap_default_scan_host()
        log.info(f"nmap scanning default scan_host: {scan_host}")
        await self.scan(scan_host)

    async def scan_local_host(self):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        scan_host = self.get_local_scan_host()
        log.info(f"nmap scanning local scan_host: {scan_host}")
        await self.scan(scan_host)

    async def simple_scan_test(self):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        await asyncio.sleep(0)
        scan_host = self.get_nmap_default_scan_host()
        Metrics.NMAP_CLIENT_SIMPLE_TEST_COUNTER.labels(
            scan_host=scan_host,
        ).inc()
        log.info(f"nmap simple scan test scanning scan_host: {scan_host}")
        await self.scan_default_host()
