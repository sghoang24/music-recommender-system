#!/usr/bin/env bash

set -e
set -x

isort --force-single-line-imports backend
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place backend
isort backend

# Run black excluding the specified folder
black --line-length 120 --exclude="venv/|alembic/|\.venv/" .