# Holded Fichar

Automates clock-in/clock-out on [Holded](https://app.holded.com) using your existing Chrome session. No API key needed.

## Requirements

- macOS
- Google Chrome (logged in to Holded)
- Python 3

## Setup

### 1. Clone the repo

```bash
git clone git@github.com:joaquinwulin/fichar.git
```

### 2. Allow JavaScript from Apple Events in Chrome

In Chrome's menu bar: **View → Developer → Allow JavaScript from Apple Events** ✓

You only need to do this once.

## Usage

```bash
python3 fichar.py
```

Run it when you arrive to clock in, run it again when you leave to clock out. It detects your current state automatically.

### With Claude Code

If you use Claude Code, just type `/fichar`.
