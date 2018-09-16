# sysout-handler


**Maintainers:** [feitnomore](https://github.com/feitnomore/)

This is a hack to implement a sidecar container that will run within a Pod in [Kubernetes](https://kubernetes.io) and will read the sysout of the main Pod's container.

This hack takes advantage of [Kubernetes Python Client](https://github.com/kubernetes-client/python) to find the name of the container that we'll be reading the sysout as well as to actually read the sysout from it.

*WARNING:* Use it at your own risk.

## INTRODUCTION

The idea here is to be able to read the sysout of the application running on the Pod and process the output in any sort of method. The application would log everything that it has on the standard output/standard error, and the sidecar would read its logs and process it, for example, pushing it to a Logstash or to a Kafka Topic.  
This approach would be interesting because it would allow the application to use any library it wants and any technology it wants, as far as it outputs the information to standard out/standard error, this way, you would not need to enforce any library usage or any technology usage by the application.  

*Note:* Don't think only about logging, but imagine you can use it for event handling as well.

## RBAC

In order for this to work, we need to create a `ServiceAccount`, a `ClusterRole` and a `ClusterRoleBinding`. We'll be granting `get`, `watch` and `list` to resources `pods` and `pods/logs`.

```
$ kubectl apply -f https://raw.githubusercontent.com/feitnomore/sysout-handler/master/examples/sysout-handler_ServiceAccount.yaml
$ kubectl apply -f https://raw.githubusercontent.com/feitnomore/sysout-handler/master/examples/sysout-handler_ClusterRole.yaml
$ kubectl apply -f https://raw.githubusercontent.com/feitnomore/sysout-handler/master/examples/sysout-handler_ClusterRoleBinding.yaml
```

*Note:* The ServiceAccount will be created in `test` Namespace.


## HOW TO BUILD IT

### Clone the Repository
```
git clone https://github.com/feitnomore/sysout-handler.git
```

### Make your changes

1. **Container Names**  
The application will look for the first container on the `Pod` that doesn't match `istio-proxy` (Istio's sidecar) or `sysout-handler` (ourselves). If you have more containers that you want to ignore, you should adjust your code in the `helpers/kubeclient.py` on `getContainerName`.

2. **Handling Logic**  
This code will only print the lines it reads. The handling of the line, and actual actions needs to be coded. For example, I have a code here that parses the lines and send them to a Kafka Topic. This handling would have to be called from `helpers/kubeclient.py` on `readSysout`.

3. **Environment**  
I encourage you to read all the configuration from the environment. We are already doing it for the Pod `name`, and Pod `Namespace`. So, for example, if you plan on sending data to a Kafka Topic, add some environment variables on the YAML of the Sidecar (see examples) for the `server`, `port` and `topic`. After that, make sure you read and test them on `sysout-handler.py` initialization.

4. **Exception**  
There is pretty much no exception handling here. Make sure you test it well, and add proper exception handling to your cases, specially if you are working with standardized outputs.

5. **Dockerfile**  
Make sure you edit `Dockerfile` according to your changes. If you add any libs, modules or files, make sure to add valid pip commands and copy commands on the `Dockerfile` so that your changes are saved on the image.

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
*Note:* Remember to set `MY_REPO` to your Docker Hub repository or your local repository.

### Add the Sidecar to your Pod
Add the sidecar to your Pod. Under the `containers` specification, add the follwing `container`:
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
```
*Note:* Remember to set the `image` to the repository you used in the previous step.  
*Note:* Remember this will only work in `test` Namespace, because the `ServiceAccount` was created on `test` Namespace.  
*Note:* If you changed your code and need to add more environment variables, this is the place where you would add them.  
*Note:* You can think about adding this to your automation pipeline so that you have the sidecar added automatically when deploying your Pods.  


## REFERENCES AND IDEAS

1. [Kubernetes](https://kubernetes.io/)
2. [Python 2.7](https://www.python.org/)
3. [Kubernetes Python Client](https://github.com/kubernetes-client/python)

## DOCUMENTATION

1. [Examples](https://github.com/feitnomore/sysout-handler/tree/master/examples)

