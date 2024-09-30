from prometheus_client import Gauge, Counter, Summary


class MetricsLabels(object):
    ARCHITECTURE = 'architecture'
    ARDUINO_CORE_VERSION = 'arduino_core_version'
    BRAND = 'brand'
    BUILD = 'build'
    FREE_HEAP = 'free_heap'
    IP = 'ip'
    MAC_ADDRESS = 'mac_address'
    NAME = 'name'
    PRODUCT = 'product'
    VERSION = 'version'
    SEGMENT = 'segment'
    BSSID = 'bssid'
    EXCEPTION_CLASS = 'exception_class'
    COLOR_PRIORITY = 'color_priority'
    COLOR_TUPLE_POSITION = 'color_tuple_position'
    SCRAPE_EVENT = 'scrape_event'

    @classmethod
    def wargos_instance_info_labels(cls):
        return list([
            cls.VERSION,
        ])

    @classmethod
    def instance_info_labels(cls):
        return list([
            cls.ARCHITECTURE,
            cls.ARDUINO_CORE_VERSION,
            cls.BRAND,
            cls.BUILD,
            cls.IP,
            cls.MAC_ADDRESS,
            cls.NAME,
            cls.PRODUCT,
            cls.VERSION,
        ])

    @classmethod
    def basic_info_labels(cls):
        return list([
            cls.NAME,
            cls.IP,
        ])

    @classmethod
    def scrape_events_labels(cls):
        return list([
            cls.IP,
            cls.SCRAPE_EVENT,
        ])

    @classmethod
    def wifi_bssid_labels(cls):
        return list([
            cls.NAME,
            cls.IP,
            cls.BSSID,
        ])

    @classmethod
    def basic_segment_labels(cls):
        return list([
            cls.NAME,
            cls.IP,
            cls.SEGMENT,
        ])

    @classmethod
    def segment_color_labels(cls):
        return list([
            cls.NAME,
            cls.IP,
            cls.SEGMENT,
            cls.COLOR_PRIORITY,
            cls.COLOR_TUPLE_POSITION,
        ])

    @classmethod
    def basic_client_labels(cls):
        return list([
            cls.IP,
        ])

    @classmethod
    def basic_online_labels(cls):
        return list([
            cls.IP,
        ])

    @classmethod
    def basic_instance_scraper_labels(cls):
        return list([
            cls.IP,
        ])

    @classmethod
    def instance_scraper_exception_labels(cls):
        return list([
            cls.IP,
            cls.EXCEPTION_CLASS,
        ])

    @classmethod
    def basic_state_labels(cls):
        return list([
            cls.NAME,
            cls.IP,
        ])

    @classmethod
    def basic_udp_sync_labels(cls):
        return list([
            cls.NAME,
            cls.IP,
        ])


class Metrics(object):
    WARGOS_INSTANCE_INFO = Gauge(
        'wargos_instance_info',
        'Details about the actual wargos scraper instance (this app)',
        MetricsLabels.wargos_instance_info_labels()
    )

    WLED_CLIENT_SIMPLE_TEST_COUNTER = Counter(
        'wargos_wled_client_simple_test_total',
        'Count of times the simple WLED client test is run',
        MetricsLabels.basic_client_labels()
    )

    WLED_CLIENT_CONNECT_EXCEPTIONS = Counter(
        'wargos_wled_client_connect_exceptions_total',
        'Counts any exceptions attempting to connect to a WLED instance',
        MetricsLabels.basic_client_labels()
    )

    WLED_CLIENT_CONNECT_TIME = Summary(
        'wargos_wled_client_connect_time_seconds',
        'Tracks the timing for a wled instance connection',
        MetricsLabels.basic_client_labels()
    )

    WLED_SCRAPER_SCRAPE_SELF_EXCEPTIONS = Counter(
        'wargos_wled_scraper_scrape_self_exceptions_total',
        'Counts any exceptions attempting to scrape self instance',
    )

    WLED_SCRAPER_SCRAPE_SELF_TIME = Summary(
        'wargos_wled_scraper_scrape_self_time_seconds',
        'Tracks the timing for scraping self instance',
    )

    WLED_SCRAPER_SCRAPE_ALL_EXCEPTIONS = Counter(
        'wargos_wled_scraper_scrape_all_exceptions_total',
        'Counts any exceptions attempting to scrape all WLED instances',
    )

    WLED_SCRAPER_SCRAPE_ALL_TIME = Summary(
        'wargos_wled_scraper_scrape_all_time_seconds',
        'Tracks the timing for scraping all WLED instances',
    )

    WLED_SCRAPER_SCRAPE_INSTANCE_EXCEPTIONS = Counter(
        'wargos_wled_scraper_scrape_instance_exceptions_total',
        'Counts any exceptions attempting to scrape a single WLED instance',
        MetricsLabels.basic_instance_scraper_labels()
    )

    WLED_SCRAPER_SCRAPE_INSTANCE_TIME = Summary(
        'wargos_wled_scraper_scrape_instance_time_seconds',
        'Tracks the timing for scraping a single WLED instances',
        MetricsLabels.basic_instance_scraper_labels()
    )

    WLED_SCRAPER_SCRAPE_INSTANCE_BY_TYPE_EXCEPTIONS = Counter(
        'wargos_wled_scraper_scrape_instance_by_type_exceptions_total',
        'Counts exceptions by type while scraping a single WLED instance',
        MetricsLabels.instance_scraper_exception_labels()
    )

    WLED_INSTANCE_SCRAPE_EVENTS_COUNTER = Counter(
        'wargos_wled_instance_scrape_events_total',
        'Count of scrape events by type per WLED instance',
        MetricsLabels.scrape_events_labels()
    )

    WLED_INSTANCE_ONLINE = Gauge(
        'wargos_wled_instance_online',
        'Whether WLED instance is online and available (0 means offline)',
        MetricsLabels.basic_online_labels()
    )

    INSTANCE_INFO = Gauge(
        'wargos_wled_instance_basic_info',
        'Details about the WLED instance info, mostly hw and build info',
        MetricsLabels.instance_info_labels()
    )

    INSTANCE_FREE_HEAP = Gauge(
        'wargos_wled_instance_free_heap',
        'The current free heap of the WLED instance (in bytes)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_UDP_PORT = Gauge(
        'wargos_wled_instance_udp_port',
        'The current udp port of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_UPTIME_SECONDS = Gauge(
        'wargos_wled_instance_uptime_seconds',
        'The current uptime of the instance (in seconds)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_PALETTE_COUNT_VALUE = Gauge(
        'wargos_wled_instance_palette_count_value',
        'The current palette count of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_EFFECT_COUNT_VALUE = Gauge(
        'wargos_wled_instance_effect_count_value',
        'The current effect count of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_LED_COUNT_VALUE = Gauge(
        'wargos_wled_instance_led_count_value',
        'The current LED count of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_LED_FPS_VALUE = Gauge(
        'wargos_wled_instance_fps_value',
        'The current fps value of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_LED_MAX_POWER = Gauge(
        'wargos_wled_instance_max_power',
        'The max power value of the instance (in milliamps)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_LED_CURRENT_POWER = Gauge(
        'wargos_wled_instance_current_power',
        'The current power value of the instance (in milliamps)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_LED_MAX_SEGMENTS = Gauge(
        'wargos_wled_instance_max_segments',
        'The max segments value of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_NIGHTLIGHT_DURATION_MINUTES = Gauge(
        'wargos_wled_instance_nightlight_duration_minutes',
        'The duration of the nightlight of the instance (in minutes)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_NIGHTLIGHT_ON_VALUE = Gauge(
        'wargos_wled_instance_nightlight_on_value',
        'The bool value of whether the nightlight of the instance is enabled',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_NIGHTLIGHT_TARGET_BRIGHTNESS_VALUE = Gauge(
        'wargos_wled_instance_nightlight_target_brightness_value',
        'The target brightness value of the nightlight of the instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_SEGMENT_COLOR_VALUE = Gauge(
        'wargos_wled_instance_segment_color_value',
        'The color value (with priority) of the segment of the instance',
        MetricsLabels.segment_color_labels()
    )

    INSTANCE_SEGMENT_BRIGHTNESS_VALUE = Gauge(
        'wargos_wled_instance_segment_brightness_value',
        'The brightness value of the segment of the instance',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_CLONES_VALUE = Gauge(
        'wargos_wled_instance_segment_clones_value',
        'The segment this segment clones for the instance',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_EFFECT_ID_VALUE = Gauge(
        'wargos_wled_instance_segment_effect_id_value',
        'The effect_id for this instance',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_INTENSITY_VALUE = Gauge(
        'wargos_wled_instance_segment_intensity_value',
        'The intensity value for this instance',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_LENGTH_VALUE = Gauge(
        'wargos_wled_instance_segment_length_value',
        'The length for this segment',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_ON_VALUE = Gauge(
        'wargos_wled_instance_segment_on_value',
        'The bool value of whether the segment of the instance is enabled',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_PALETTE_ID_VALUE = Gauge(
        'wargos_wled_instance_segment_palette_id_value',
        'The palette_id value of the segment',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_REVERSE_VALUE = Gauge(
        'wargos_wled_instance_segment_reverse_value',
        'Flips the segment (in 2D set up) to change direction',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_SEGMENT_ID_VALUE = Gauge(
        'wargos_wled_instance_segment_id_value',
        'The segment_id value of the segment',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_SELECTED_VALUE = Gauge(
        'wargos_wled_instance_segment_selected_value',
        'The bool value of whether the segment of the instance is selected',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_SPEED_VALUE = Gauge(
        'wargos_wled_instance_segment_speed_value',
        'The relative effect speed of the segment',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_CCT_VALUE = Gauge(
        'wargos_wled_instance_segment_cct_value',
        'The white spectrum color temperature (0 is warmest, 255 is coldest)',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_START_VALUE = Gauge(
        'wargos_wled_instance_segment_start_value',
        'For 2-D set up, this determines segment starts (from top left)',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_SEGMENT_STOP_VALUE = Gauge(
        'wargos_wled_instance_segment_stop_value',
        'For 2D set up, this determines segment starts (from top left)',
        MetricsLabels.basic_segment_labels()
    )

    INSTANCE_FILESYSTEM_SPACE_TOTAL = Gauge(
        'wargos_wled_instance_filesystem_space_kb_total',
        'The total space of the filesystem (in kb)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_FILESYSTEM_SPACE_USED = Gauge(
        'wargos_wled_instance_filesystem_space_kb_used',
        'The used space of the filesystem (in kb)',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_WIFI_CHANNEL = Gauge(
        'wargos_wled_instance_wifi_channel',
        'The current wifi channel of the WLED instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_WIFI_RSSI = Gauge(
        'wargos_wled_instance_wifi_rssi',
        'The current wifi RSSI of the WLED instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_WIFI_SIGNAL = Gauge(
        'wargos_wled_instance_wifi_signal',
        'The current wifi signal of the WLED instance',
        MetricsLabels.basic_info_labels()
    )

    INSTANCE_WIFI_BSSID = Gauge(
        'wargos_wled_instance_wifi_bssid',
        'The current bssid of the wifi the WLED instance is connected to',
        MetricsLabels.wifi_bssid_labels()
    )

    INSTANCE_LIVE_STATE = Gauge(
        'wargos_wled_instance_live_state',
        'The current WLED instance live state bool value',
        MetricsLabels.basic_state_labels()
    )

    INSTANCE_STATE_BRIGHTNESS = Gauge(
        'wargos_wled_instance_state_brightness',
        'The current WLED instance brightness',
        MetricsLabels.basic_state_labels()
    )

    INSTANCE_STATE_TRANSITION = Gauge(
        'wargos_wled_instance_state_transition',
        'Duration of crossfade between colors/brightness (1 unit is 100ms)',
        MetricsLabels.basic_state_labels()
    )

    INSTANCE_STATE_ON = Gauge(
        'wargos_wled_instance_state_on',
        'The current WLED instance is on value',
        MetricsLabels.basic_state_labels()
    )

    INSTANCE_STATE_PLAYLIST_ID = Gauge(
        'wargos_wled_instance_state_playlist_id',
        'The current WLED instance playlist_id',
        MetricsLabels.basic_state_labels()
    )

    INSTANCE_STATE_PRESET_ID = Gauge(
        'wargos_wled_instance_state_preset_id',
        'The current WLED instance preset_id',
        MetricsLabels.basic_state_labels()
    )

    INSTANCE_SYNC_RECEIVE_STATE = Gauge(
        'wargos_wled_instance_sync_receive_state',
        'The current state of the WLED instance sync receive setting',
        MetricsLabels.basic_udp_sync_labels()
    )

    INSTANCE_SYNC_SEND_STATE = Gauge(
        'wargos_wled_instance_sync_send_state',
        'The current state of the WLED instance sync send setting',
        MetricsLabels.basic_udp_sync_labels()
    )

    INSTANCE_SYNC_RECEIVE_GROUPS = Gauge(
        'wargos_wled_instance_sync_receive_groups',
        'The current state of the WLED instance sync receive groups',
        MetricsLabels.basic_udp_sync_labels()
    )

    INSTANCE_SYNC_SEND_GROUPS = Gauge(
        'wargos_wled_instance_sync_send_groups',
        'The current state of the WLED instance sync send groups',
        MetricsLabels.basic_udp_sync_labels()
    )
