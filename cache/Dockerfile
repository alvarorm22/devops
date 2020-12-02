FROM python:3.6.12-alpine3.12  

ADD cache.py /

# install Python 3
RUN apk update && apk add gcc python3-dev musl-dev


RUN pip3 install httpcore==0.12.0
RUN pip3 install httpx==0.16.1
RUN pip3 install redis==3.5.3
RUN pip3 install flask 

CMD [ "python", "/cache.py" ]

EXPOSE 5005

