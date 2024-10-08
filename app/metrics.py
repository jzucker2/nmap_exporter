from enum import Enum
from prometheus_client import Gauge, Counter, Summary


class MetricsLabels(Enum):
    SCAN_HOST = 'scan_host'
    VERSION = 'version'

    @classmethod
    def nmap_instance_info_labels(cls):
        return list([
            cls.VERSION.value,
        ])

    @classmethod
    def basic_scan_labels(cls):
        return list([
            cls.SCAN_HOST.value,
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
