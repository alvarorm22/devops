# devops

## API

This API has been implemented with Python, it has been used the Flask module to expose the API service for requests.
The api2json works as follows: 

- It receives a request to serve the air quality measurements of some cities
- api2json execute a query to a postgres instance to get this information in csv
- Then the API transform the data and return it in a well structured JSON

### Tools and scripts

Some scripts have been developed to build and deploy the images easier:

-- Makefile: It import deploy.env file and build | up | stop | start the containers. Also publish command is available to tag and upload the images to Docker Hub
-- docker-compose: Make use this config file to deploy and build images. Dependencies between containers are indicated in this file too. Environment variables used by docker-compose must be indicated in an .env file

## POSTGRES

This postgres image has been built to start and load the `environment_airq_measurand.csv`file in a table. It can be started with Makefile and docker-compose

## CI 

A CI flow has been built so that when performing an MR to github a trigger is launched to build the image and upload it to docker hub. This point has been implemented with Travis CI. All dependencies and steps are in .travis.yaml file. 
The flow run as follows:

-- MR is push to the GitHub repository
-- A trigger is launched in Travis
-- All dependencies are installed
-- A simple pylint test is executed
-- Builds the docker images
-- Push the images to Docker Hub

## DEPLOYMENT

All of these containers are been deployed in a kubernetes cluster. Yaml config files are provided in k8s folder:

-- 1 Deployment with 5 replicas for api2json image
-- 1 Deployment with 1 replicas for postgres image
-- 1 Service to expose the api2json deployment
-- 1 Service to expose the postgres deployment
-- 1 Secret for passwords and db

Also, a solution cache has been implemented in this exercise. It has been use a Redis for the cache and a API-Cache implemented in Python. These config files are includes in k8s folder too, and they are the following:

-- 1 Deployment with 1 replicas for the rediscache image
-- 1 Deployment with 1 replicas for the redis instance
-- 1 Service to expose the rediscache deployment
-- 1 Service to expose the redis deployment
-- 1 Secret for passwords

The logic of the rediscache implementation is as follows:

The rediscache container sends requests to api2json service and caches the return value in a Redis database for 1 hour. During this time if the rediscache receives another request, it look if the data is in Redis and return this value, otherwise it sends a new request to the api2json API and load the data in the cache layer for one hour.

This strategy gets decrease the postgres load and return data quickly. Another invalidation strategies can bee implemented simply change the ttl of data in cache layer.


All of these deployments and services can be launched with command: `kubectl create -f <file.yaml>`


## MONITORING, LOGS AND BACKUP

To ensure proper operation of this solution there are some points that can bee monitorized easily:

-- API Ports: They have to be allways open to reveives requests. It can bee monitorized for example whith some Ansible playbooks. Also Kubernetes offers the possibility of implementing liveness HTTP request for pods, the kubelet is checking the ports healtz and can restart de container when the port is no able to respond
-- Postgres and Redis: Load, CPU, memory and other graphics can be displayed in a Grafana Dashboard. Prometheus and InfluxDB can be used for storing metrics.

For logs, an optimal solution could be sends it to a ELK platform, so developers and operators can review it easily from Kibana.

There most important things to do a backup are the data volumes of datastores


