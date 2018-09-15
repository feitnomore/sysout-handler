# kubeclient - Main API Handler
# Handles the interaction with Kubernetes.
# Here we do the Kubernetes magic.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

import urllib3
from helpers import globalholders
from kubernetes import client
from kubernetes import config

# Loads configuration
def loadConfig():
    try:
        # Disable SSL Warnings:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Load config from the Cluster (will use ServiceAccount)
        config.load_incluster_config()
        
        return True
        
    except Exception as e:
        print e
        print e.message
        return False

# Performs the API Connection
def connectApi():
    try:
        # Connects to Kubernetes API
        globalholders.coreApi = client.CoreV1Api()
        return True

    except Exception as e:
        print e
        print e.message
        return False

# Find Container Name
def getContainerName(podname, podnamespace):
    try:
        # Getting this POD Information
        myPod = globalholders.coreApi.read_namespaced_pod(podname, podnamespace)
        # Going through this POD's containers
        for container in myPod.spec.containers:
            # Looking for a container that is not ourserlf or istio-proxy
            if((container.name != "istio-proxy") and (container.name != "sysout-handler")):
                return container.name
        
    except Exception as e:
        print e
        print e.message
        return None

# Read Sysout Line
def readSysout(podname, podnamespace, containername):
    try:
        # Handle sysout line by line
        for sysoutLine in globalholders.coreApi.read_namespaced_pod_log(podname, podnamespace, container=containername, follow = True, pretty = "pretty_example", timestamps = False, _preload_content=False):

            # This is the place were you would
            # handle the sysout of the container
            # for example to publish a message to
            # Kafka/RabbitMQ, Logstash or Prometheus
            print("Message being handled: " + sysoutLine)

    except Exception as e:
        print e
        print e.message
        return False
