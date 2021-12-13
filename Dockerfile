# pull official base image
FROM python:3.9.4-alpine

# set work directory
WORKDIR /

# copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt


# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        libressl-dev libffi-dev gcc musl-dev python3-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/app/