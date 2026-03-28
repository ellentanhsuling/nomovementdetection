#!/bin/bash
# Project Switcher Script
# Switches between non-movement detection and fall detection projects

PROJECT=$1

# Validate input
if [ -z "$PROJECT" ]; then
    echo "Usage: ./switch_project.sh [non_movement|fall_detection]"
    echo ""
    echo "Projects:"
    echo "  non_movement  - Non-movement detection (extended inactivity)"
    echo "  fall_detection - Fall detection (immediate emergencies)"
    exit 1
fi

if [ "$PROJECT" != "non_movement" ] && [ "$PROJECT" != "fall_detection" ]; then
    echo "Error: Invalid project. Must be 'non_movement' or 'fall_detection'"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Stop any currently running monitoring system
echo "Stopping any running monitoring systems..."
pkill -f "python.*main.py" || true
sleep 2

# Check if process is still running
if pgrep -f "python.*main.py" > /dev/null; then
    echo "Warning: Some processes may still be running. Force killing..."
    pkill -9 -f "python.*main.py" || true
    sleep 1
fi

# Start the selected project
echo ""
echo "Starting $PROJECT project..."
echo ""

cd "$PROJECT"

# Check if config exists
if [ ! -f "config.yaml" ]; then
    echo "Error: config.yaml not found in $PROJECT directory"
    exit 1
fi

# Run the project
python main.py
