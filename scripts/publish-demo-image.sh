#! /bin/bash

set -euxo pipefail

DOCKERFILE_PATH="infrastructure/docker/monolith/Dockerfile"
DATA_PATH="./.data"
IMAGE_NAME="lookalike-demo"
IMAGE_REPO="ghcr.io/haydenjeune"
IMAGE_TAG="$(git rev-parse --short HEAD)$(git diff --quiet || echo '.uncommitted')"

docker build -f "$DOCKERFILE_PATH" --build-arg IMAGE_ROOT="$DATA_PATH" -t "$IMAGE_NAME:$IMAGE_TAG" .

# Need to auth with ghcr beforehand to push, enter a github Personal Access Token in the prompt
# docker login ghcr.io -u <username> --password-stdin

docker tag "$IMAGE_NAME:$IMAGE_TAG" "$IMAGE_REPO/$IMAGE_NAME:$IMAGE_TAG"
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$IMAGE_REPO/$IMAGE_NAME:latest"

docker push "$IMAGE_REPO/$IMAGE_NAME:$IMAGE_TAG"
docker push "$IMAGE_REPO/$IMAGE_NAME:latest"
