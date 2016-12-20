#!/bin/sh
source venv/bin/activate
touch temp/server.pid
python -m py.bin.start_webserver
