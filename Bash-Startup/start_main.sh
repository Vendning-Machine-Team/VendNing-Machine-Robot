#!/bin/bash
# start_main.sh - launches main.py at boot

# Full path to your Python file
SCRIPT_PATH="/home/pi/main.py" # Update this path once we have it put into the pi

# Full path to Python interpreter (use `which python3` to confirm)
PYTHON="/usr/bin/python3" # Same here, update if needed

# Run the Python script
$PYTHON $SCRIPT_PATH

# Run this into the terminal to make it executable:
# chmod +x /home/pi/start_main.sh