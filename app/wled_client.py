import os
from wled import WLED
from .utils import LogHelper
from .metrics import Metrics


log = LogHelper.get_env_logger(__name__)


class WLEDClient(object):
    @classmethod
    def get_client(cls):
        return WLEDClient()

    @classmethod
    def default_wled_ip(cls):
        # TODO: consolidate env imports
        return os.environ.get('DEFAULT_WLED_IP',
                              "10.0.1.179")

    @classmethod
    async def get_wled_instance_device(cls, ip_address):
        log.debug(f"wled connecting to ip_address: {ip_address}")
        with Metrics.WLED_CLIENT_CONNECT_EXCEPTIONS.labels(
            ip=ip_address,
        ).count_exceptions():
            with Metrics.WLED_CLIENT_CONNECT_TIME.labels(
                ip=ip_address,
            ).time():
                async with WLED(ip_address) as led:
                    device = await led.update()
                    log.debug(f"wled got device: {device}")

                    return device

    @classmethod
    async def simple_wled_test(cls):
        """Don't overcomplicate this one. Simple usage like the dep docs"""
        device_ip = cls.default_wled_ip()
        Metrics.WLED_CLIENT_SIMPLE_TEST_COUNTER.labels(
            ip=device_ip,
        ).inc()
        log.info(f"wled connecting to device_ip: {device_ip}")
        async with WLED(device_ip) as led:
            device = await led.update()
            log.info(f"wled got device: {device}")
            log.info(f"device.info.version => {device.info.version}")
            log.info(f"device.info => {device.info}")
            log.info(f"device.state => {device.state}")

            # Turn strip on, full brightness
            await led.master(on=True, brightness=255)
