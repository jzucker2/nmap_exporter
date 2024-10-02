# nmap_exporter

I plan on using the Home Assistant wled library: `python-nmap` located here: https://github.com/home-assistant-libs/python-nmap

## Alternatives

* https://github.com/nmmapper/python3-nmap

## How to Run

### Configure Docker Compose

Example `docker-compose.yml` like:

```yaml
services:

  nmap_exporter:
    container_name: nmap_exporter
    image: ghcr.io/jzucker2/nmap_exporter
    restart: always
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - WLED_IP_LIST=10.0.1.1,10.0.1.2,10.0.1.3
    ports:
      - "9292:9292"
    stdin_open: true
    tty: true
```

### Set Env Vars

By default, logging is info level. To set to debug, provide the env `DEBUG=true` flag

|                   Env Var Name                   | Default Value | Example Value |                               Description                               |
|:------------------------------------------------:|:-------------:|:-------------:|:-----------------------------------------------------------------------:|
|                     `DEBUG`                      |    `false`    |    `true`     |          This determines debug logging and a few other things           |
|      `DEFAULT_NMAP_SCRAPE_INTERVAL_SECONDS`      |     `60`      |     `30`      | This determines how often to scrape prometheus metrics from `nmap` scan |
|                `NMAP_SCAN_HOST`                  |    `None`     | `10.0.0.1/24` |          This is the ip range of addresses to scan and scrape           |

## Prometheus

For prometheus I have some options:

* https://github.com/trallnag/prometheus-fastapi-instrumentator
* https://github.com/prometheus/client_python
* https://prometheus.github.io/client_python/
* https://prometheus.github.io/client_python/exporting/http/fastapi-gunicorn/

### Add to Prometheus for Metrics Collection

Add this to your `prometheus.yml`

```yaml
- job_name: 'nmap_exporter'

  # metrics_path defaults to '/metrics'
  # scheme defaults to 'http'.
  static_configs:
    - targets: [ '<host_ip>:9292' ]
      labels:
        instance: 'host_machine'
```

## Scheduler

* https://fastapi-utils.davidmontague.xyz/
  * https://github.com/dmontagu/fastapi-utils
* https://github.com/amisadmin/fastapi-scheduler
* https://github.com/amisadmin/fastapi-amis-admin

## fastapi

I am new to fastapi

* https://fastapi.tiangolo.com/tutorial/
* https://fastapi.tiangolo.com/advanced/
* https://fastapi.tiangolo.com/how-to/general/
* https://github.com/fastapi/full-stack-fastapi-template/tree/master

## Development

Notes about dev work here.

### Curl Commands

```
# healthcheck
curl -i "http://localhost:9292/healthz" \
    -H "Content-Type: application/json"

# simple nmap scan of localhost
curl -i "http://localhost:9292/scan/local" \
    -H "Content-Type: application/json"

# simple nmap scan test of default scan host (set in env var for now)
curl -i "http://localhost:9292/scan/test" \
    -H "Content-Type: application/json"

# now test with prometheus metrics on default nmap host (set in env var for now)
curl -i "http://localhost:9292/prometheus/default" \
    -H "Content-Type: application/json"
```

### Logging

* https://stackoverflow.com/questions/77001129/how-to-configure-fastapi-logging-so-that-it-works-both-with-uvicorn-locally-and
  * This is the pattern I went with for now
* https://github.com/tiangolo/fastapi/discussions/7457

### Docker Images

* https://www.reddit.com/r/FastAPI/comments/rrwglp/reduce_size_of_the_official_fastapi_image/
* https://www.reddit.com/r/FastAPI/comments/11rfbae/using_docker_for_your_fastapi_apps_considering/

## Updates

```
pip install --upgrade -r update-requirements.txt
```
