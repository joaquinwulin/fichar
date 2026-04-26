#!/bin/bash
# Runs fichar.py only on Fridays between START and END dates.
# Edit START/END to match your schedule.

DIR="$(dirname "$0")"
TODAY=$(date +%Y%m%d)
START=20260424
END=20260626

if [ "$TODAY" -ge "$START" ] && [ "$TODAY" -le "$END" ]; then
    python3 "$DIR/fichar.py" >> "$DIR/fichar.log" 2>&1
fi
