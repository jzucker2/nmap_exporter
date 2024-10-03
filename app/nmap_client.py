import asyncio
import os
from collections import namedtuple
from nmap import PortScannerAsync
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
                                  600))

    def __init__(self):
        super().__init__()
        self._scanner = PortScannerAsync()

    @property
    def scanner(self) -> PortScannerAsync:
        return self._scanner

    def get_version(self) -> NmapVersionInfo:
        try:
            version, subversion = self.scanner._nm.nmap_version()
            return NmapVersionInfo(str(version), str(subversion))
        except Exception as e:
            log.error(f'nmap trying to get version, got e: {e}')
            return (None, None)

    @classmethod
    def _parse_scanned_host_result(cls, host, host_result):
        log.info(f'Host : {host} ({host_result.hostname()})')
        log.info(f'State : {host_result.state()}')
        for proto in host_result.all_protocols():
            log.info('----------')
            log.info(f'Protocol : {proto}')
            lport = host_result[proto].keys()
            lport.sort()
            for port in lport:
                port_state = host_result[proto][port]['state']
                log.info(f'port : {port}\tstate : {port_state}')

    @classmethod
    def _parse_scan_result(cls, scan_host, scan_result):
        log.debug(f'parse for scan_host: {scan_host} '
                  f'and scan_result ({type(scan_result)}) '
                  f'=> scan_result: {scan_result}')
        all_hosts_results = scan_result["scan"]
        log.debug(f'parsing all_hosts_results: {all_hosts_results}')
        for host, host_result in all_hosts_results.items():
            log.debug('----------------------------------------------------')
            cls._parse_scanned_host_result(host, host_result)

    def default_scanner_callback(self, host, scan_result):
        log.debug('+++++++++++++++++++++++++++++++++++++++')
        log.debug(f'default_scanner_callback => '
                 f'host: {host}, scan_result: {scan_result}')
        self._parse_scan_result(host, scan_result)

    def _scan(self, host, port_range=None):
        if not port_range:
            port_range = self.get_nmap_default_scan_port_range()
        log.debug(f'Going to scan host: {host} with port_range: {port_range}')
        self.scanner.scan(
            hosts=host,
            ports=port_range,
            timeout=self.get_nmap_default_scan_timeout_seconds(),
            callback=self.default_scanner_callback,
        )
        while self.scanner.still_scanning():
            log.debug("Scanner waiting >>>")
            self.scanner.wait(2)
        log.debug('scanner is done!')

    async def scan(self, scan_host):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        await asyncio.sleep(0)
        Metrics.NMAP_CLIENT_SCAN_HOST_COUNTER.labels(
            scan_host=scan_host,
        ).inc()
        log.debug(f"nmap scanning scan_host: {scan_host}")
        self._scan(scan_host)

    async def scan_default_host(self):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        scan_host = self.get_nmap_default_scan_host()
        log.debug(f"nmap scanning default scan_host: {scan_host}")
        await self.scan(scan_host)

    async def scan_local_host(self):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        scan_host = self.get_local_scan_host()
        log.debug(f"nmap scanning local scan_host: {scan_host}")
        await self.scan(scan_host)

    async def simple_scan_test(self):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        await asyncio.sleep(0)
        scan_host = self.get_nmap_default_scan_host()
        Metrics.NMAP_CLIENT_SIMPLE_TEST_COUNTER.labels(
            scan_host=scan_host,
        ).inc()
        log.debug(f"nmap simple scan test scanning scan_host: {scan_host}")
        await self.scan_default_host()
