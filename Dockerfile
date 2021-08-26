FROM python:3
ADD . /code
WORKDIR /code
RUN mkdir /var/log/shore_app
RUN pip install -r requirements.txt
# RUN export FLASK_APP="shore_app:app"
# RUN export FLASK_ENV=development
# RUN flask run

# CMD python3 create_tables.py
CMD python3 -m shore_app.app
