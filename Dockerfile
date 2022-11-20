FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y upgrade && \
    apt-get -y install python3.10 && \
    apt update && apt install python3-pip -y

WORKDIR /app
EXPOSE 8000

# Method1 - installing LibreOffice and java
RUN apt-get --no-install-recommends install libreoffice -y
RUN apt-get install -y libreoffice-java-common

# Method2 - additionally installing unoconv
RUN apt-get install unoconv

ARG CACHEBUST=1
RUN mkdir -p /app/app

COPY app /app/app
COPY requirements.txt /app
COPY init_docker.sh /app
COPY start.sh /app

RUN pip3 install -r requirements.txt
RUN apt autoremove && apt clean

#RUN python3 ./start.sh
