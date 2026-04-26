# Holded Fichar

Automates clock-in and clock-out on Holded using your existing Chrome session. One command, no passwords, no API keys.

## Prerequisites

- macOS
- Google Chrome logged in to Holded
- Python 3 — check with `python3 --version` in Terminal. If missing, install from [python.org](https://www.python.org/downloads/)

No additional packages needed.

## Setup (one time)

### 1. Clone the repo

Open Terminal and run:

```bash
git clone git@github.com:joaquinwulin/fichar.git
cd fichar
```

### 2. Unlock Chrome for scripting

In Chrome's menu bar at the top of your screen:

**View → Developer → Allow JavaScript from Apple Events**

A checkmark will appear next to it. You only need to do this once.

## Usage

In Terminal, from the `fichar` folder:

```bash
python3 fichar.py
```

- Run it when you **arrive** → clocks you in
- Run it when you **leave** → clocks you out and confirms the popup

It detects your state automatically — same command either way.

### 3. (Optional) Create a `/fichar` shortcut in Claude Code

If you use Claude Code, you can run the script by just typing `/fichar` in the chat.

Create the file `~/.claude/commands/fichar.md`:

```bash
mkdir -p ~/.claude/commands
cat > ~/.claude/commands/fichar.md << 'EOF'
Run the Holded time-tracking automation script by executing this bash command:

```bash
python3 /path/to/fichar/fichar.py
```

Report the output to the user clearly. If there's an error, show the full message and suggest next steps.
EOF
```

Replace `/path/to/fichar` with the actual path where you cloned the repo (e.g. `~/fichar`). Then type `/fichar` in Claude Code to clock in or out.

## Troubleshooting

**"No se encontró el botón de fichaje"** — the page didn't load in time. Run it again.

**"Executing JavaScript through AppleScript is turned off"** — you need to enable the Chrome setting from Step 2.

**Chrome must be open** — the script controls your existing Chrome window. If Chrome is closed, open it and make sure you're logged in to Holded before running.
