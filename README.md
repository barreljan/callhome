# CallHome

This set of two programs is a simple call home function with 1 job; getting the IPsec site-to-site tunnel reconfigured after a DHCP renew has taken place.
Basically, the servers helds records of clients (in MySQL) and the client intermittently calls the server to see if his IP address is the same.
If not the same, the client makes the call to the server that his IP adres is updated.
Then, the server executes a Netconf script to adjust the firewall on that side and the client also initiates a script to adjust on his side.

Basically if your ISP decides to change your home IP, this automates the change in the tunnel configuration on both sides.

The server is build and tested on:

 * Centos7

The client is not tested so far

# Current status
This is alpha in the earliest state. New to Flask and Werkzeug, so im trying.
