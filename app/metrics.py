from enum import Enum
from prometheus_client import Gauge, Counter, Summary


class MetricsLabels(Enum):
    SCAN_HOST = 'scan_host'
    VERSION = 'version'
    NMAP_VERSION = 'nmap_version'
    NMAP_SUBVERSION = 'nmap_subversion'
    HOST = 'host'
    HOSTNAME = 'hostname'
    STATE = 'state'
    PORT_STATE = 'port_state'
    PROTOCOL = 'protocol'
    PORT = 'port'

    @classmethod
    def nmap_instance_info_labels(cls):
        return list([
            cls.VERSION.value,
            cls.NMAP_VERSION.value,
            cls.NMAP_SUBVERSION.value,
        ])

    @classmethod
    def basic_scan_labels(cls):
        return list([
            cls.SCAN_HOST.value,
        ])

    @classmethod
    def basic_host_scan_result_labels(cls):
        return list([
            cls.HOST.value,
            cls.HOSTNAME.value,
            cls.STATE.value,
        ])

    @classmethod
    def basic_port_scan_result_labels(cls):
        return list([
            cls.HOST.value,
            cls.HOSTNAME.value,
            cls.PROTOCOL.value,
            cls.PORT.value,
            cls.PORT_STATE.value,
        ])


class Metrics(object):
    NMAP_CLIENT_SIMPLE_TEST_COUNTER = Counter(
        'nmap_client_simple_test_total',
        'Count of times the simple nmap client test is run',
        MetricsLabels.basic_scan_labels()
    )

    NMAP_CLIENT_SCAN_HOST_COUNTER = Counter(
        'nmap_client_scan_host_total',
        'Count of times the nmap client scans host',
        MetricsLabels.basic_scan_labels()
    )

    SCRAPER_SCRAPE_SCAN_HOST_EXCEPTIONS = Counter(
        'nmap_scraper_scrape_scan_host_exceptions_total',
        'Counts any exceptions attempting to scrape a scan host',
        MetricsLabels.basic_scan_labels()
    )

    SCRAPER_SCRAPE_SCAN_HOST_TIME = Summary(
        'nmap_scraper_scrape_scan_host_time_seconds',
        'Tracks the timing for scraping a scan host',
        MetricsLabels.basic_scan_labels()
    )

    SCRAPER_SCRAPE_SELF_EXCEPTIONS = Counter(
        'nmap_scraper_scrape_self_exceptions_total',
        'Counts any exceptions attempting to scrape self (this app) instance',
    )

    SCRAPER_SCRAPE_SELF_TIME = Summary(
        'nmap_scraper_scrape_self_time_seconds',
        'Tracks the timing for scraping self (this app) instance',
    )

    NMAP_INSTANCE_INFO = Gauge(
        'nmap_instance_info',
        'Details about the actual nmap scraper instance (this app)',
        MetricsLabels.nmap_instance_info_labels()
    )

    NMAP_SCANNED_HOST_STATE = Gauge(
        'nmap_scanned_host_state',
        'State for a nmap scanned host result',
        MetricsLabels.basic_host_scan_result_labels()
    )

    NMAP_SCANNED_PORT_STATE = Gauge(
        'nmap_scanned_port_state',
        'State for a nmap scanned port result',
        MetricsLabels.basic_port_scan_result_labels()
    )
