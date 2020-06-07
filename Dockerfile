FROM python:3

RUN mkdir -p /usr/src/one

WORKDIR /root

COPY requirements.txt /usr/src/one

RUN pip install -r /usr/src/one/requirements.txt

ADD . /usr/src/one

RUN pip install --editable /usr/src/one

RUN mkdir -p /root/.one/ && \
    touch /root/.one/credentials

ENTRYPOINT [ "one" ]

CMD [ "--help" ]