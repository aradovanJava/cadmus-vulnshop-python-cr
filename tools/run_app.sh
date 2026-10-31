#!/usr/bin/env bash
# Starts the training application on 127.0.0.1:8080. Do not change the host.
cd "$(dirname "$0")/.." || exit 1
python3 app.py
