FROM alpine:latest

RUN apk upgrade
RUN apk add --no-cache --update \
    bash \
    linux-headers  \
    mysql \
    mysql-client \
    python3 \
    py-pip \
    expect


RUN mkdir /app
WORKDIR /app
ADD . /app/

ENV PIPENV_VERSION=2020.11.15
RUN pip --version
RUN pip install pipenv
RUN pipenv install

#EXPOSE 5000
#RUN bash db_setup.sh
#ENV FLASK_APP=urlmonster.py
#RUN pipenv run flask run
