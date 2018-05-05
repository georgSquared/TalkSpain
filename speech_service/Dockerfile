FROM python:2.7-slim

#Install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
libc6-dev \
gcc \
make \
swig \
bison \
pulseaudio \
libpulse-dev \
osspd \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /speech_service

ADD . /speech_service

#Install python requirements
RUN pip install -r requirements.txt

#Set environment variables
ENV LD_LIBRARY_PATH=/usr/local/lib
ENV LD_LIBRARY_PATH=/usr/local/lib

#Install sphinxbase and pocketsphinx from each respective folder
WORKDIR /speech_service/sphinxbase-5prealpha/

RUN ./configure && \
make && \
make install

WORKDIR /speech_service/pocketsphinx-5prealpha/

RUN ./configure && \
make && \
make install

#Go back to service level workdir
WORKDIR /speech_service



#Expose port to public
EXPOSE 80

#Run the service
CMD ["python", "speech_service.py"]