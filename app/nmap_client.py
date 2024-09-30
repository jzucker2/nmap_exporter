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
                              '10.0.0.0/24')

    def __init__(self):
        super().__init__()
        self._scanner = PortScanner()

    @property
    def scanner(self):
        return self._scanner

    def scan(self):
        host = self.get_nmap_scan_host()
        log.info(f'Going to scan host: {host}')
        scan_result = self.scanner.scan(
            host, '22-443')
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
