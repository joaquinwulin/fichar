# Holded Fichar

Automates clock-in/clock-out on [Holded](https://app.holded.com) using your existing Chrome session. No API key needed.

## How it works

- **`/fichar`** — clocks you in or out instantly (detects current state automatically)
- **`fichar_sabado.py`** — runs every Saturday and adds the previous Friday's hours (17:00–21:00) to Control Horario

## Requirements

- macOS
- Google Chrome (logged in to Holded)
- Python 3

## Setup

### 1. Clone the repo

```bash
git clone git@github.com:joaquinwulin/fichar.git
cd fichar
```

### 2. Allow JavaScript from Apple Events in Chrome

In Chrome's menu bar: **View → Developer → Allow JavaScript from Apple Events** ✓

You only need to do this once.

### 3. Configure your schedule (for the Saturday automation)

```bash
cp config.example.py config.py
```

Edit `config.py` with your own date range and public holidays:

```python
START = datetime.date(2026, 1, 1)   # first Friday to cover
END   = datetime.date(2026, 6, 30)  # last Friday to cover
SKIP  = {
    datetime.date(2026, 5, 15),     # festivos
}
```

### 4. Add the Saturday cron job

```bash
(crontab -l; echo "0 9 * * 6 python3 $(pwd)/fichar_sabado.py >> $(pwd)/fichar_sabado.log 2>&1") | crontab -
```

This runs every Saturday at 9:00 and adds the previous Friday's entry automatically.

## Daily use

Run `/fichar` in Claude Code to clock in or out. Chrome must be open and on any page.

For manual use without Claude Code:

```bash
python3 fichar.py
```

## Notes

- Chrome must be open for both scripts to work
- The Saturday script only fires if yesterday was a Friday within your configured date range
- Logs are saved to `fichar.log` and `fichar_sabado.log` (gitignored)
