from ubuntu:18.04
RUN apt-get update \
	&& apt-get install -y python3-pip python3-dev \
	&& cd /usr/local/bin \
	&& ln -s /usr/bin/python3 python \
	&& pip3 install --upgrade pip
WORKDIR /app
COPY . /app

RUN pip3 --no-cache-dir install -r insurance-forecast/requirements.txt
EXPOSE 80



WORKDIR /app/insurance-forecast/api

ENTRYPOINT ["python3"]

CMD ["server-api.py"]

 
