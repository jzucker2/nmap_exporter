from typing import Union

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from .version import version

from prometheus_fastapi_instrumentator import Instrumentator


from .utils import LogHelper
from .nmap_client import NmapClient
from .scraper import Scraper


log = LogHelper.get_env_logger(__name__)


app = FastAPI()


Instrumentator().instrument(app).expose(app)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/healthz")
def healthcheck():
    return {
        "message": "healthy",
        "version": version,
    }


# real stuff here


@app.get("/scan/test")
async def simple_scan_test():
    log.info('Starting with simple_scan_test')
    await NmapClient.get_client().simple_scan_test()
    log.info('Done with simple_scan_test')
    return {"message": "Hello World"}


@app.get("/scan/local")
async def scan_local():
    log.info('Starting with scan_local')
    await NmapClient.get_client().scan_local_host()
    log.info('Done with scan_local')
    return {"message": "Hello World"}


@app.get("/prometheus/default")
async def prometheus_default():
    log.info('Starting with prometheus_default')
    await Scraper.get_client().scrape_default_scan_host()
    log.info('Done with prometheus_default')
    return {"message": "Hello World"}


@app.on_event("startup")
@repeat_every(seconds=Scraper.get_default_scrape_interval())
async def perform_full_routine_metrics_scrape() -> None:
    log.debug(f"Starting perform_full_scrape of all metrics "
              f"(interval: {Scraper.get_default_scrape_interval()}) "
              f"=========>")
    await Scraper.get_client().perform_full_scrape()
    log.info('Done with perform_full_routine_metrics_scrape')
