#!/bin/bash

set -e

echo "Welcome to Prooster!"
exec python3 client.py &
exec python3 bot.py 
