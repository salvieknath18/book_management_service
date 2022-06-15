FROM python:latest

WORKDIR /usr/app

COPY requirement.txt /

RUN pip install -r /requirement.txt

COPY . .

ENV PYTHONPATH=/usr/app

ENV ENV_FILE_LOCATION=.env

ENTRYPOINT [ "python" ]

CMD ["app.py" ]
