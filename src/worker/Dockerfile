FROM ubuntu:18.04

WORKDIR /app

COPY . /app
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt


ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]