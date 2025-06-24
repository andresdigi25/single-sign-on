#!/bin/bash

# Extract PIP_INDEX_URL from Jenkinsfile
export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain ichain-libs --domain-owner 687531504312 --region us-east-1 --query authorizationToken --output text`
export PIP_INDEX_URL=https://aws:$CODEARTIFACT_AUTH_TOKEN@ichain-libs-687531504312.d.codeartifact.us-east-1.amazonaws.com/pypi/ichain-python/simple/


# Check if PIP_INDEX_URL is set
if [ -z "$PIP_INDEX_URL" ]; then
  echo "PIP_INDEX_URL is not set in the Jenkinsfile."
  exit 1
fi

# Build the Docker image
docker build -t my-python-app --build-arg PIP_INDEX_URL=$PIP_INDEX_URL -f Dockerfile .

# Run the Docker container
docker run -e config_secret_manager=ichain-admin-sso-api -p 8000:8000 my-python-app