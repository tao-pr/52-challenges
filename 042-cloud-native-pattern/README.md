
# Cloud Native PatternPlayground of Cloud native pattern in Kubernetes

Playing with basic design patterns of deployments in k8s.


## Prerequisites

To run a virtual cluster locally, we can use [minikube](https://minikube.sigs.k8s.io/docs/start/).
The following alias can be used interchangeably with `kubectl`

```sh
alias mk="minikube kubectl --" # use this as is kubectl
```

Start minikube on your local machine

```sh
minikube start # needs a docker daemon to run
mk get po -A # test displaying the cluster
minikube dashboard # show the cluster dashboard UI

mk create namespace 42 # create the test namespace
```

## Setting up

Build a docker image of the simple FastAPI app for deployment 
and load it into minikube.

```sh
docker build -t prebuilt/my-service .

minikube image load prebuilt/my-service # load from local docker

minikube image ls # should show the loaded image
```

## 1. Basic Deployment

Deploy the sample RESTful service

```sh
# Choose any of these deployment 
mk apply -f v1/rolling-deploy.yaml
mk apply -f v1/recreate-deploy.yaml

# Service deployment
mk apply -f v1/service.yaml
```

Then you can get and access the service via

```sh
mk -n42 get svc # list the service
minikube -n42 svc my-service-api # open in browser (with the correct port)
```

Try restarting the deployment. This will apply the deployment policy.

```sh
mk -n42 rollout restart deploy/my-service
```

## 2. Green-Blue Deployment

Deploy both green & blue

```sh
mk apply -f v1/blue-deploy.yaml
mk apply -f v1/green-deploy.yaml

# When checking pods with app=my-service, it should show all from both
mk -n42 get pod -l app=my-service
```

Then deploy loadbalancer for sending 100% of traffic to blue deployment 

```sh
mk apply -f v1/blue-green-service.yaml # load balancer 
```

Try accessing the (blue) service via

```sh
minikube -n42 svc my-service-loadbalancer # should always see 'blue'
```

Now switch the traffic to green deployment by patching the load balancer

```sh
mk -n42 patch svc my-service-loadbalancer -p '{"spec": {"selector": {"version": "green"}}}'
```

Try accessing the (green) service via

```sh
minikube -n42 svc my-service-loadbalancer # should always see 'green'
```

## 3. Secured Deployment

Create an [opaque secret](https://kubernetes.io/docs/concepts/configuration/secret/#opaque-secrets) (password)

```sh
mk -n42 create secret generic pass --from-literal=admin=passtest # replace with your wanted password
```

Check the created (opaque) secret

```sh
mk get secret pass -o jsonpath='{}' # render whole config (JSON)

mk get secret pass -o jsonpath='{.data}' # {"admin":"cGFzc3Rlc3Q="}

mk get secret pass -o jsonpath='{.data.*}' # "cGFzc3Rlc3Q="

mk get secret pass -o jsonpath='{.data.*}' | base64 -d # "passtest"
```

Test deploying pod which knows the secret for the service

```sh
mk apply -f v1/secured-deploy.yaml # this deployment knows secret
```

## Tear down

After use, do not forget to clear all deployment down

```sh
mk -n42 delete svc -l foo=bar
mk -n42 delete deploy -l foo=bar

minikube stop
```

## Licence

BSD