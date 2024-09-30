import os
from .utils import LogHelper
from .metrics import Metrics


log = LogHelper.get_env_logger(__name__)


class NmapClient(object):
    @classmethod
    def get_client(cls):
        return cls()
