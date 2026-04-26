#!/bin/bash
# Runs fichar.py only on Fridays between 2026-04-24 and 2026-06-26

TODAY=$(date +%Y%m%d)
START=20260424
END=20260626

if [ "$TODAY" -ge "$START" ] && [ "$TODAY" -le "$END" ]; then
    python3 /Users/joaquinwulin/Documents/Claude/automations/holded_fichar/fichar.py >> /Users/joaquinwulin/Documents/Claude/automations/holded_fichar/fichar.log 2>&1
fi
