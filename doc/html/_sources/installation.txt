Installation
------------

::

    pip install shaddock

Or, if you have virtualenvwrapper installed::

    mkvirtualenv shaddock
    pip install shaddock
    
Installing it from sources::

    git clone https://github.com/epheo/shaddock
    cd shaddock && sudo pip install .

Using an existing yaml definition model::

    git clone https://github.com/epheo/shaddock-openstack

Play with it! ::

    shaddock -f openstack-deployer.yml

    (shaddock) ps
    (shaddock) build 
    (shaddock) start 

    (shaddock) rm mysql001
