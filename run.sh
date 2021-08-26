#!/bin/bash

set -e

exec python3 client.py &
exec python3 bot.py