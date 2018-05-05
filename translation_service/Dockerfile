FROM python:2.7-slim

RUN apt-get update && apt-get install -y \
wget \
&& wget http://apertium.projectjj.com/apt/install-nightly.sh -O - | bash \
&& apt-get -f install -y apertium-all-dev \
&& apt-get install apertium-en-es

WORKDIR /translation_service

ADD . /translation_service

#Install python requirements
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "translation_service.py"]