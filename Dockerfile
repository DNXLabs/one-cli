FROM python:3.9-buster

RUN apt-get update && apt-get install -y \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/src/one

WORKDIR /root

ADD . /usr/src/one

RUN pip install --editable /usr/src/one

RUN mkdir -p /root/.one/ && \
    touch /root/.one/secrets

ENTRYPOINT [ "one" ]

CMD [ "--help" ]