FROM python:3.10
WORKDIR /code

#RUN apt-get update && apt-get install -y build-essential libffi-dev


RUN pip install --upgrade pip
RUN pip install psycopg2-binary
RUN pip install scrapy
RUN pip install scrapy-playwright

RUN playwright install
RUN playwright install-deps

COPY ./sreality .
RUN cd sreality

ENTRYPOINT ["scrapy", "crawl", "sreality_spider"]
#CMD ["bash"]