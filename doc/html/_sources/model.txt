
The Shaddock Definiton Model
---------------------------------

Your model consist in a set of files that describe your general architecture,
It can be a simple Yaml few lines, a more complete Jinja2 templated multi 
files hierarchy or an integrated Python module that you interface with
the rest of your infratsructure.

Defining a **service**
~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following examples resume how you can describe a service in a cluster:

You will need at least the following options:

.. literalinclude:: ../../tests/model/900-simple-tests.yml
    :language: yaml
    :start-after: ---

The following options are currenlty implemented:

.. literalinclude:: ../../tests/model/800-service-tests.yml
    :language: yaml
    :start-after: ---


Including other files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Shaddock allow you to split your definition model into multiple yaml files
using the !include notation.

This, conbined with the templating allow you to design very complex
architectures without repetitions or loosing in readabality of your model.

.. literalinclude:: ../../tests/model/120-include-tests.yml
    :language: yaml
    :start-after: ---



Using the **scheduler**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Shaddock scheduler will ensure that all the requirements you provide are 
matched before starting a new service.

You can check:
- A container status
- If a port is open (tcp or udp)
- The return code of a http GET

You can also specify the number of retry, the time to wait before 2 checks, and
if the check should use the system proxy vars or not.

.. code:: yaml

     - {name: nova, status: stopped}
     - {name: nova, port: 8774, type: tcp}
     - {name: nova, port: 8774, state: down, type: tcp}
     - {host: google.com, port: 8774, state: down, type: tcp}
     - {name: nova, type: http, get: '/v2.0', port: 5000, code: 200}
     - {host: google.com, type: http, get: '/v2.0', port: 5000, code: 200}
     - {host: 127.0.0.1, type: http, get: '/', code: 200, useproxy: False }
     - {name: nova, sleep: 20} # defaults to 10
     - {name: nova, retry: 10} # defaults to 5


.. literalinclude:: ../../tests/model/500-scheduler-tests.yml
    :language: yaml
    :start-after: ---

Managing multiple hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~
Shaddock is able to schedule your services on different hosts accros your 
datacenter.
The only prerequirements for a host to be part of a Shaddock cluster is toi
have the Docker API installed and listening on a port.
You can then configure your hosts in your cluster defintion.

.. literalinclude:: ../../tests/model/site01/hosts_dc01.yml
    :language: yaml
    :start-after: ---


.. literalinclude:: ../../tests/model/200-hosts-tests.yml
    :language: yaml
    :start-after: ---


Using the templating functionalities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The model definition variables {{ your_var }} are templated using Jinja2
before being interpreted by Shaddock.
You can define any variables value in the **vars:** section of a cluster
definiton.

refs: http://jinja.pocoo.org/

.. literalinclude:: ../../tests/model/400-jinja-tests.yml
    :language: yaml
    :start-after: ---
