# sysout-handler - Main Controller Module
# This is where we instantiate everything.
#
# Marcelo Feitoza Parisi (marcelo@feitoza.com.br)

import sys
import os
from helpers import globalholders
from helpers import kubeclient

# Main :-)
def main():

    # Check if we can determine our namespace
    if(os.getenv("POD_NAMESPACE") == ""):
        print("Error reading POD_NAMESPACE")
        sys.exit(1)

    # Check if we can determine our pod name
    if(os.getenv("POD_NAME") == ""):
        print("Error reading POD_NAME")
        sys.exit(1)

    # Load Kubernetes API Configuration
    if(kubeclient.loadConfig() is False):
        print("Error loading Kubernetes Config")
        sys.exit(1)

    # Create Kubernetes API Connection
    if(kubeclient.connectApi() is False):
        print("Error connecting to Kubernetes API")
        sys.exit(1)

    # Check if we could determine the container name
    mycontainer = kubeclient.getContainerName(os.getenv("POD_NAME"), os.getenv("POD_NAMESPACE"))
    if(mycontainer is None):
        print("Error getting the Container Name")
        sys.exit(1)

    # Printing our startup information
    print("Starting the handler")
    print("Namespace: " + os.getenv("POD_NAMESPACE"))
    print("Pod: " + os.getenv("POD_NAME"))
    print("Container: " + mycontainer)
    print("------------------------------")

    # Start the Sysout Handler
    kubeclient.readSysout(os.getenv("POD_NAME"), os.getenv("POD_NAMESPACE"), mycontainer)
    

if __name__ == '__main__':
    main()
