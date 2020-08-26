FROM python:3

RUN mkdir -p /usr/src/one

WORKDIR /root

ADD . /usr/src/one

RUN pip install --editable /usr/src/one

RUN mkdir -p /root/.one/ && \
    touch /root/.one/secrets

ENTRYPOINT [ "one" ]

CMD [ "--help" ]