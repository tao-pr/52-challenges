
# Cloud Native PatternPlayground of Cloud native pattern in Kubernetes


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

mk create namespace 042 # create the test namespace
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
mk -n 042 get service # list the service
minikube -n 042 service my-service-api # open in browser (with the correct port)
```

Try restarting the deployment. This will apply the deployment policy.

```sh
mk -n 042 rollout restart deploy/my-service
```

## 2. Green-Blue Deployment

Deploy both green & blue

```sh
mk apply -f v1/blue-deploy.yaml
mk apply -f v1/green-deploy.yaml

# When checking pods with app=my-service, it should show all from both
mk -n042 get pod -l app=my-service
```

Then deploy loadbalancer for sending 100% of traffic to blue deployment 

```sh
mk apply -f v1/blue-green-service.yaml # load balancer 
```

Try accessing the (blue) service via

```sh
minikube -n 042 service my-service-loadbalancer # should always see 'blue'
```

Now switch the traffic to green deployment by patching the load balancer

```sh
mk -n 042 patch service my-service-loadbalancer -p '{"spec": {"selector": {"version": "green"}}}'
```

Try accessing the (green) service via

```sh
minikube -n 042 service my-service-loadbalancer # should always see 'green'
```

## Tear down

After use, do not forget to clear all deployment down

```sh
mk -n 042 delete service -l foo=bar
mk -n 042 delete deploy -l foo=bar

minikube stop
```

## Licence

BSD