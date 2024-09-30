import asyncio
from typing import Union

from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from .version import version

from prometheus_fastapi_instrumentator import Instrumentator


from .utils import LogHelper
# from .nmap_client import NmapClient
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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# real stuff here


@app.get("/test")
async def simple_test():
    await asyncio.sleep(0)
    return {"message": "Hello World"}


@app.get("/prometheus/default")
async def prometheus_default():
    await asyncio.sleep(0)
    return {"message": "Hello World"}


@app.get("/prometheus/all")
async def prometheus_scrape_all():
    await asyncio.sleep(0)
    return {"message": "Hello World"}


@app.on_event("startup")
@repeat_every(seconds=Scraper.get_default_scrape_interval())
async def perform_full_routine_metrics_scrape() -> None:
    log.debug(f"Going to perform full scrape of all metrics "
              f"(interval: {Scraper.get_default_scrape_interval()}) "
              f"=========>")
    await asyncio.sleep(0)
