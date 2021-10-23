#! /bin/bash

set -euo pipefail

DOCKERFILE_PATH="infrastructure/docker/monolith/Dockerfile"
DATA_PATH="/.data"
IMAGE_NAME="ghcr.io/haydenjeune/lookalike-demo"
IMAGE_TAG=$(git rev-parse HEAD)$(git diff --quiet || echo '.uncommitted')

echo "$DOCKERFILE_PATH"
echo "$DATA_PATH"
echo "$IMAGE_NAME"
echo "$IMAGE_TAG"

#docker build -f "$DOCKERFILE_PATH" --build-arg IMAGE_ROOT="$DATA_PATH" -t "$IMAGE_NAME:$IMAGE_TAG" .

#docker login ghcr.io -u haydenjeune --password-stdin
#docker push ghcr.io/haydenjeune/lookalike:latest
