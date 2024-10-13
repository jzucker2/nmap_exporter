ARG PYTHON_VERSION=3.12-alpine
FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN set -x \
    && apk update  \
    && apk add --no-cache  \
      gcc \
      python3-dev \
      musl-dev \
      linux-headers

# TODO: Is this the best workdir?
WORKDIR /code

# TODO: need to go over requirements
COPY ./requirements.txt /code/requirements.txt

# This looks good
RUN pip wheel --no-deps --wheel-dir /code/wheels -r /code/requirements.txt

FROM python:${PYTHON_VERSION} AS runner

RUN set -x \
    && apk update  \
    && apk add --no-cache  \
      curl \
      nmap \
      nmap-scripts

COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .

RUN pip install --no-cache --no-deps /wheels/*

WORKDIR /code

# This looks good
COPY ./app /code/app

# Expose the port on which the application will run
EXPOSE 9292

HEALTHCHECK --interval=5s --timeout=5s --retries=3 \
    CMD curl -f http://0.0.0.0:9292/healthz || exit 1

# TODO: make port configurable and maybe get behind gunicorn
CMD ["fastapi", "run", "app/main.py", "--port", "9292"]
