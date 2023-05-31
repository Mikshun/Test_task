FROM python:3.10-alpine3.17
WORKDIR /usr/src/app
COPY reqieremnts.txt ./
RUN apk update && apk upgrade
RUN apk add ffmpeg
RUN pip install -r reqieremnts.txt

EXPOSE 8000
