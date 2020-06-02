FROM python:3

RUN mkdir -p /usr/src/one

WORKDIR /root

COPY requirements.txt /usr/src/one

RUN pip install -r /usr/src/one/requirements.txt

ADD . /usr/src/one

RUN pip install --editable /usr/src/one

ENTRYPOINT [ "one" ]

CMD [ "--help" ]