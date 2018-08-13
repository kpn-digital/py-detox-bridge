Detox Python Bridge
===========================

.. image:: https://secure.travis-ci.org/kpn-digital/py-detox-bridge.svg?branch=master
    :target:  http://travis-ci.org/kpn-digital/py-detox-bridge?branch=master

.. image:: https://img.shields.io/codecov/c/github/kpn-digital/py-detox-bridge/master.svg
    :target: http://codecov.io/github/kpn-digital/py-detox-bridge?branch=master

.. image:: https://img.shields.io/pypi/v/detox-bridge.svg
    :target: https://pypi.python.org/pypi/detox-bridge

.. image:: https://readthedocs.org/projects/detox-bridge/badge/?version=latest
    :target: http://detox-bridge.readthedocs.org/en/latest/?badge=latest

A bridge to enable python code to use the detox grey-box testing API ( https://github.com/wix/detox )


Requirements
============

NVM
---

The package requires nvm to be installed. Either the NVM environment variable needs to contain the full path of the nvm.sh script, or 
the NVM_DIR environment variable needs to point at the root directory of nvm containing the nvm.sh script.

NODE
----

The code emitted by this bridge requires node 8 or higher. Node 7.6 should work but is not tested.


Python
------

3.5 or 3.6 is required to use the package.

Detox
-----

Follow the getting started guide from detox ( https://github.com/wix/detox/blob/master/docs/Introduction.GettingStarted.md )


Usage
=====

.. code:: python

   from detox_bridge import await, by, detox, device, element, expect, node_with_detox

   app_path = "detox/examples/demo-react-native"

   # Start Node server in app_path root folder that contains node_modules

   with node_with_detox(app_path=app_path, default_timeout=10) as appserver:

       # Detox Config (we could also load this from package.json)

       ios_sim_release = {
           "binaryPath": "ios/build/Build/Products/Release-iphonesimulator/example.app",
           "type": "ios.simulator",
           "name": "iPhone 7 Plus"
       }

       configurations_obj = {"configurations": {"ios.sim.release": ios_sim_release}}

       # Longer timeout since the app may be installed

       appserver(await(detox.init(configurations_obj)), timeout=360)

       # Reload react native

       appserver(await(device.reloadReactNative()))

       # Expectation

       appserver(await(expect(element(by.id('welcome'))).toBeVisible()))

       # Cleanup

       appserver(await(detox.cleanup()))

Development
===========


Requirements
------------

Both python 3.5 and python 3.6 are required to run the suite suite.

Checkout
--------

After checkout run::

   git submodule update --init --recursive 


Running tests
-------------

To run the test suite::

    make test


Once the venv is there you can also run some tests via tox::

    venv/bin/tox -e py35 -- -k <regex>
