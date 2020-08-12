FROM python:3.5-jessie  AS build-env
LABEL maintainer="https://github.com/thcp"

WORKDIR /app

ADD . /app

RUN pip3 install --upgrade pip \
    && \
    pip install -r requirements.txt

FROM python:3.5-alpine
COPY --from=build-env /app /app
COPY --from=build-env /usr/local/lib/python3.5/site-packages /usr/local/lib/python3.5/site-packages

WORKDIR /app
ENV PYTHONPATH=/usr/local/lib/python3.5/site-packages

CMD python app.py