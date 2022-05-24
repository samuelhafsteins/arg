FROM ubuntu:21.04

WORKDIR /src/
COPY . .

RUN apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y git dnsutils \
	&& rm -rf  /src/.git \
	&& rm -rf /var/lib/apt/lists/*

CMD [ "python3", "/src/main.py" ]
