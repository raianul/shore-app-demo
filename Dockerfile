FROM python:3
ADD . /code
WORKDIR /code
RUN mkdir /var/log/shore_app
RUN pip3 install -e .