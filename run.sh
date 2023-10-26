#!/usr/bin/env bash

set -a
source .env
set +a

./bin/python3 aggregatron-admin.py
