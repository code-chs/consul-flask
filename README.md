# consul and flask with docker-compose


**This is a proof of concept, working prototye:** single consul server, no tls, minimum failsafe, two app nodes
the purpose of this example to demonstrate workarond for docker-compose's static variables (service "init")


1. Run `docker-compose build' to build the containers specified in the docker-compose file.

1. Run `docker-compose up` to start the containers (add -d to run them in the background. Then run `docker-compose stop` when done.)  

1. Browse to http://localhost:5001 or http://localhost:5002 for node1 and node2 to see the response from the web app, same db. 
