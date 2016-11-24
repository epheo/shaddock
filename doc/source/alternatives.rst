
Alternative configuration and other systems
-------------------------------------------

Docker Machine and OS X support
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Please use the ``--boot2docker`` option and Shaddock will source the
environement variables set by Docker machine.

In order to set those variables you may want to 
``$(sudo docker-machine env machine_name)"`` first.


Run the shaddock shell from a container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code:: bash

    docker run --rm -i -v shaddock/tests/model/:/model \
        --env DOCKER_HOST="https://<your_host>:2376" \
        --env TEMPLATE_FILE=/model/service-tests.yml \
        -t shaddock/shaddock


**Seting up the Docker API to listen on tcp:**

`<https://docs.docker.com/reference/api/docker_remote_api/>`_


