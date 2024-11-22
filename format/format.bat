@echo off
setlocal enabledelayedexpansion

REM Format the 'backend' folder
isort backend
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place backend
isort backend
black --line-length 120 --exclude="venv/|\.venv/" backend

REM Format the 'recommendation' folder
isort recommendation
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place recommendation
isort recommendation
black --line-length 120 --exclude="venv/|\.venv/" recommendation
