FROM shaddock/seed:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

RUN \
     git clone https://github.com/epheo/shaddock &&\
     cd shaddock && python setup.py install

CMD['shaddock']