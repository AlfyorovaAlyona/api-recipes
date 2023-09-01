# 3.9 - version of python, alpine - light version of linux
FROM python:3.9-alpine3.13

LABEL maintainer="github:AlfyorovaAlyona"

ENV PYTHONUNBUFFERED 1

# copy files from local machine to container
COPY ./requirements.txt /tmp/requirements.txt
# requirements applicable to dev only (not needed for deployment)
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

# by default, the mode is deployment, not development
ARG DEV=false
# create a virt env inside docker container,
# upgrade pip, install requirements,
# create user in the container (not root!)
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # update the package list
    apk add --update --no-cache postgresql-client jpeg-dev && \
    # create a virtual package to store dependencies
    apk add --update --no-cache --virtual .tmp-build-deps \
    # install packages into .temp-build-deps
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home django-user

ENV PATH="/py/bin:$PATH"

# switch to non-root user
USER django-user