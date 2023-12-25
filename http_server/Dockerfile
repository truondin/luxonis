FROM python:3.10
WORKDIR /code

RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install Jinja2

COPY ./main.py main.py
COPY ./index.html index.html

ENTRYPOINT ["python3", "main.py"]