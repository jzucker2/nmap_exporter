# https://fastapi.tiangolo.com/deployment/docker/
# TODO: update and pin python version
FROM python:3.12 AS builder

# TODO: Is this the best workdir?
WORKDIR /code

# TODO: need to go over requirements
COPY ./requirements.txt /code/requirements.txt

# This looks good
RUN pip wheel --no-deps --wheel-dir /code/wheels -r /code/requirements.txt

FROM python:3.12-slim AS runner

RUN apt-get update -y && apt-get install -y \
        curl \
    && apt-get clean

COPY --from=builder /code/wheels /wheels
COPY --from=builder /code/requirements.txt .

RUN pip install --no-cache /wheels/*

WORKDIR /code

# This looks good
COPY ./app /code/app

# Expose the port on which the application will run
EXPOSE 9292

HEALTHCHECK --interval=5s --timeout=5s --retries=3 \
    CMD curl -f http://0.0.0.0:9292/healthz || exit 1

# TODO: make port configurable and maybe get behind gunicorn
CMD ["fastapi", "run", "app/main.py", "--port", "9292"]
