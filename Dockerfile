FROM python:3
ADD . /code
WORKDIR /code
RUN mkdir /var/log/shore_app
RUN pip3 install -e .
# RUN pip3 install -r requirements.txt
# RUN export FLASK_APP="shore_app:app"
# RUN export FLASK_ENV=development
# RUN flask run
# CMD python3 create_tables.py
# CMD python3 create_database.py
# CMD python3 -m shore_app.app
# CMD export FLASK_APP=shore_app
# CMD export FLASK_ENV=development
# CMD flask run --host=0.0.0.0


# FROM mysql
# COPY init.sql /docker-entrypoint-initdb.d/1-init.sql
