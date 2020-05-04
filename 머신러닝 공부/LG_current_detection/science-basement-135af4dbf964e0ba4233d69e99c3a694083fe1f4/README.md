## Overview
Materials used in science-basement workshop

## Installing dependencies
    $ sudo apt-get update
    $ sudo apt-get install git
    $ sudo apt-get install python3 python-dev python3-dev
    $ sudo apt-get install python3-serial python3-numpy python3-scipy python3-matplotlib  

    $ wget https://labs.picotech.com/raspbian/pool/main/libu/libusbdrdaq/libusbdrdaq_1.0.6-1r03_armhf.deb
    $ sudo dpkg -i libusbdrdaq_1.0.6-1r03_armhf.deb
    $ rm *.deb

## Using the code
Before running the code for first time, build drdaq driver:

    $ cd drdaq
    $ make

To start the measurements, use Python 3: 

    $ python3 measure_service.py

The code can be executed in a free-running mode, where instead of real sensors random number generator is used.
Such mode can be selected, by setting variable **full_functional** to *False*
