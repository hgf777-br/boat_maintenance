# pull official base image
FROM python:3.12

# Needed for SAML support
RUN  apt-get update
RUN  apt-get -y install libxml2-dev libxmlsec1-dev libxmlsec1-openssl
RUN  apt-get update && apt-get install cron -y && apt-get install vim -y && touch /var/log/cron.log
RUN  service cron start 

# set work directory
WORKDIR /home/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
