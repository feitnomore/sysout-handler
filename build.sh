#!/bin/sh
# Build and Exec
# I am too tired of doing this by hand

docker rm sysout-handler 
docker rmi sysout-handler --force
docker build -t sysout-handler .

# Pushing to remote repository
export MY_REPO="my-local-registry:80"
docker tag sysout-handler:latest $MY_REPO/sysout-handler:latest
docker push $MY_REPO/sysout-handler:latest
