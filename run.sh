#/usr/bin/bash

set -eu

podman run --rm --device nvidia.com/gpu=all hello:latest