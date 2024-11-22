#!/usr/bin/env bash

set -e
set -x

# Format the 'backend' folder
isort backend
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place backend
isort backend
black --line-length 120 --exclude="venv/|\.venv/" backend

# Format the 'recommendation' folder
isort recommendation
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place recommendation
isort recommendation
black --line-length 120 --exclude="venv/|\.venv/" recommendation
