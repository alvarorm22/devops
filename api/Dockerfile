FROM python:3.6.12-alpine3.12  

ADD api-carto.py /

# install Python 3

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install flask
RUN pip3 install psycopg2==2.7.6

CMD [ "python3", "./api-carto.py" ]

EXPOSE 5000
