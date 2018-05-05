FROM python:2.7-alpine3.6

WORKDIR /sender_service

ADD . /sender_service

#Install python requirements
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "sender_service.py"]