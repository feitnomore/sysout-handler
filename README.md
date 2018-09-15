# sysout-handler


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a hack to implement a sidecar container that will run within a POD in [Kubernetes](https://kubernetes.io) and will read the sysout of the main POD's container.

*WARNING:* Use it at your own risk.

## INTRODUCTION

The idea here is to be able to read the sysout of the application running on the POD and process the output in any sort of method. The application would log everything that it has on the standard output/standard error, and the sidecar would read its logs and process it, for example, pushing it to a Logstash or to a Kafka Topic.  
This approach would be interesting because it would allow the application to use any library it wants and any technology it wants, as far as it outputs the information to standard out/standard error, this way, you would not need to enforce any library usage or any technology usage by the application.

## RBAC

In order for this to work, we need to create a `ServiceAccount`, a `ClusterRole`, a `ClusterRoleBinding`. We'll be granting `get`, `watch` and `list` to resources `pods` and `pods/logs`.

```
$ kubectl apply -f https://raw.githubusercontent.com/feitnomore/sysout-handler/master/examples/sysout-handler_ServiceAccount.yaml
$ kubectl apply -f https://raw.githubusercontent.com/feitnomore/sysout-handler/master/examples/sysout-handler_ClusterRole.yaml
$ kubectl apply -f https://raw.githubusercontent.com/feitnomore/sysout-handler/master/examples/sysout-handler_ClusterRoleBinding.yaml
```

*Note:* The ServiceAccount will be created in `test` namespace.


## HOW TO BUILD IT

### Clone the Repository
```
git clone https://github.com/feitnomore/sysout-handler.git
```

### Make your changes

*Note:* Remember to edit `Dockerfile` according to your changes.

### Build the Image
```
cd sysout-handler
docker build -t sysout-handler .
```

### Push the image to the Repository
````
export MY_REPO="my_local_repository"
docker tag sysout-handler:latest $MY_REPO/sysout-handler:latest
docker push $MY_REPO/sysout-handler:latest
````
*Note:* Remember to set `MY_REPO`.

### Add the Sidecar to your Pod
Add the sidecar to your POD:
```
        - name: sysout-handler
          image: my_local_repository/sysout-handler:latest
          imagePullPolicy: Always
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
      serviceAccountName: sysout-handler
      restartPolicy: Always
```
*Note:* Remember to set the `image` to the repository you used in the last step.  
*Note:* Remember this will only work in `test` namespace.


## REFERENCES AND IDEAS

1. [Kubernetes](https://kubernetes.io/)
2. [Python 2.7](https://www.python.org/)
3. [Kubernetes Python Client](https://github.com/kubernetes-client/python)

## DOCUMENTATION

1. [Examples](https://github.com/feitnomore/sysout-handler/tree/master/examples)

