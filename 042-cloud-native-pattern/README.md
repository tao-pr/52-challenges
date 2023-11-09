
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

- Rolling deployment: `mk apply -f v1/rolling-deploy.yaml`
- TBD

## Tear down

After use, do not forget to clear all deployment down

```sh
minikube stop
```

## Licence

BSD