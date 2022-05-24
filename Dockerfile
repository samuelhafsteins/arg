FROM ubuntu:21.04

WORKDIR /src/
COPY ./src/* .

RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y git dnsutils \
	&& rm -rf /var/lib/apt/lists/*

CMD [ "python3","/src/main.py" ]
