#!/bin/bash

for image in $*;do
    echo "Tag ${DOCKER_USER}/${image}:${DOCKER_TAG} as ${DOCKER_USER}/${image}:latest"
    docker tag "${DOCKER_USER}/${image}:${DOCKER_TAG}" "${DOCKER_USER}/${image}:latest"
    echo 'Push the new tags'
    docker push "${DOCKER_USER}/${image}:${DOCKER_TAG}"
    docker push "${DOCKER_USER}/${image}:latest"
done
