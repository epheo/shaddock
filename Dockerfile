FROM shaddock/seed:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

RUN \
     apt-get update && apt-get install -y git &&\
     git clone https://github.com/epheo/shaddock &&\
     cd shaddock && python setup.py install