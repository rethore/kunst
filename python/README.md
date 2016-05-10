# Python Backend
This directory host all the files used to run the python backend to control the lights of Svalin

## Running the REST API server
The REST API is a flask interface, that opens a port 6001 locally.

    $ python3 rest.py

Note that the first time you run the script you will have to press the blue button of the philips Hue router.


## Connection to the WebUI server
In order to access the port from another machine, one needs to open an ssh tunnel with backward forwarding of the port to the Raspberry pi:

   $ ssh username@my_server -R 6001:localhost:6001 -f -N

## Runing the light scheduler

    $ python3 light_scheduler.py



