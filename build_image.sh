#!/usr/bin/bash

set -eu

podman build -f images/Containerfile.hello . -t hello:latest