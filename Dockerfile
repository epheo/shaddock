FROM shaddock/seed:latest
MAINTAINER Thibaut Lapierre <root@epheo.eu>

## Run exple:
# docker run --rm -i -v /path/to/your/config/:/var/lib/shaddock \
# --env DOCKER_HOST="https://172.42.42.42::2376" -t shaddock/shaddock

RUN \
     git clone https://github.com/epheo/shaddock &&\
     git clone https://github.com/epheo/shaddock-openstack /var/lib/shaddock/
     cd shaddock && python setup.py install

VOLUME /var/lib/shaddock

CMD ["shaddock"]