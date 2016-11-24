Usage
-----


Using the command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: raw
    
    usage: shdk [--version] [-v] [--log-file LOG_FILE] [-q] [-h] [--debug]
                [-f SHDK_MODEL] [-d SHDK_IMGDIR] [-c SHDK_CLUSTER]
                [--docker-version DOCKER_VERSION] [-i DOCKER_URL] [--boot2docker]
                [--tls] [--tlscert DOCKER_CERT_PATH] [--tlskey DOCKER_KEY_PATH]
                [--tlsverify DOCKER_TLS_VERIFY] [--tlscacert DOCKER_CACERT_PATH]
    

Shaddock shell:
    
.. code:: raw
    
    optional arguments:
      --version             Show Shaddock's version number and exit.
      -v, --verbose         Increase verbosity of output. Can be repeated.
      --log-file LOG_FILE   Specify a file to log output. Disabled by default.
      -q, --quiet           Suppress output except warnings and errors.
      -h, --help            Show this help message and exit.
      --debug               Show tracebacks on errors.
      -f SHDK_MODEL, --file SHDK_MODEL
                            Template file to use.
      -d SHDK_IMGDIR, --images-dir SHDK_IMGDIR
                            Directory to build Docker images from.
      -c SHDK_CLUSTER, --cluster SHDK_CLUSTER
                            The cluster to use (No value is all by default).
      --docker-version DOCKER_VERSION
                            Docker API version number
      -i DOCKER_URL, --url DOCKER_URL
                            Force a specific host url API.
      --boot2docker         Use Boot2Docker TLS conf.You should first:"eval $(sudo
                            docker-machine env machine_name)"
      --tls                 Use TLS; implied by tls-verify flags.
      --tlscert DOCKER_CERT_PATH
                            Path to TLS certificate file.
      --tlskey DOCKER_KEY_PATH
                            Path to TLS key file.
      --tlsverify DOCKER_TLS_VERIFY
                            Use TLS and verify the remote.
      --tlscacert DOCKER_CACERT_PATH
                            Trust only remotes providing a certificate signed by
                            theCA given here.

Commands:

.. code:: raw

      build          Build a service
      complete       print bash completion command
      create         Create a new container
      help           print detailed help for another command
      logs           Display the logs of a container
      ps             Show a list of Containers.
      pull           Pull a container from the Docker Repository
      restart        Restart a container
      rm             Remove a container
      show           Show details about a container
      start          Start a new container
      stop           Stop a container


Using shaddock in a project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    import shaddock

