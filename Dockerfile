FROM python:3.9.0-alpine  AS build-env
LABEL maintainer="https://github.com/thcp"


ADD  ./app /app

ENV SITE_PACKAGES=/usr/local/lib/python3.9/site-packages

WORKDIR /app

RUN pip3 install --upgrade pip \
    && \
    pip install -r requirements.txt

FROM python:3.9.0-alpine
COPY --from=build-env /app /app
COPY --from=build-env ${SITE_PACKAGES} ${SITE_PACKAGES}

WORKDIR /app
ENV PYTHONPATH=${SITE_PACKAGES}

CMD python app.py