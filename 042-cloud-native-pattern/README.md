
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

## Samples

Run a sample RESTful service deployment with:

```sh
# Rolling deployment
mk apply -f v1/rolling-deploy.yaml

# Service deployment
mk apply -f v1/service.yaml
```

Then you can get and access the service via

```sh
mk -n 042 get service # list the service

minikube -n 042 service my-service-api # open in browser
```

## Tear down

After use, do not forget to clear all deployment down

```sh
# Delete service & deployment
mk -n 042 delete service my-service-api
mk -n 042 delete deploy my-service

minikube stop
```

## Licence

BSD