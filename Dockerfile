FROM python:3

RUN mkdir -p /usr/src/one

WORKDIR /usr/src/one

COPY requirements.txt .

RUN pip install -r requirements.txt

ADD . .

RUN pip install --editable .

ENTRYPOINT [ "one" ]

CMD [ "--help" ]