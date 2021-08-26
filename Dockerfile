FROM python:3
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
# RUN export FLASK_APP="shore_app:app"
# RUN export FLASK_ENV=development
# RUN flask run

# CMD python3 create_tables.py
CMD python3 shore_app/app.py
