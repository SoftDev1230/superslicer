#!/bin/bash

export PIPENV_VENV_IN_PROJECT=1

pipenv install
pipenv run python src/main.py
