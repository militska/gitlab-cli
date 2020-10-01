FROM python:3-alpine
WORKDIR /usr/src/app

COPY rm_images.py ./rm_images.py
RUN pip install requests
