#!/bin/bash

# docker run -p 127.0.0.1:8000:8000/tcp -it registry.digitalocean.com/sea/sendhybridgov-back:1.0 bash -c ./start.sh
export PYTHONPATH="./"
python3 app/start.py