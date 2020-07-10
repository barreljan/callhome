# CallHome

This set of two programs ('server' and 'client') is a simple call home function with 1 job; getting the IPsec site-to-site tunnel reconfigured after a DHCP renew has taken place.
Basically, the server helds records of clients (in MySQL) and the client intermittently calls the server to see if his IP address is the same.
If not the same, the client makes the call (JSON POST) to the server that his IP adres is updated, by what time etc.
Then, the server is asked to execute a job to adjust the firewall on that side and the client also executes a job to adjust on his side.

Basically if your ISP decides to change your home IP, this automates the change in the tunnel configuration on both sides.

This concept is based on an ipsec site-to-site tunnel between a Cisco ASA and Ubiquiti Edgerouter.


The server side is build and tested on:

 * Centos 7.8
 * Apache 2.4 + WSGI 4.7.1, OpenSSL 1.0.2k-fips
 * PHP 7.4.8
 * Python 3.7

The client is not tested so far then only on the dev system but with an actual Cisco ASA to interact with

# Current status
This is beta in the earliest state. New to Flask and Werkzeug, so i'm trying. But it is progressing nicely. Included Jinja, 
better project structure, simplified imports and usability between shared components.

# What works;

\- API part. It serves the JSON data I want. It accepts the JSON data I send. It processes it.
Make sure your Apache is compiled with the correct WSGI mods and libs. Oh and it logs towards MySQL in a basic way 
\- Client part. The client can call the API, decide if there is a change in IP, start the cisco asa 'worker' to fix it.
This shared worker can also be used on the server side, given that the Jinja2 template matches. Otherwise the worker needs 
some dynamic input to choose a different template.

It stil is not automated in such way. That bein said; it is still beta and a steep learning curve.