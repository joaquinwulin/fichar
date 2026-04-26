#!/usr/bin/env python3
"""Runs every Saturday. Adds Friday's 17:00–21:00 entry in Holded Control Horario.
Only fires for Fridays between 2026-04-24 and 2026-06-26.
"""

import subprocess
import sys
import datetime
from config import START, END, SKIP

def yesterday_friday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    if yesterday.weekday() == 4 and START <= yesterday <= END and yesterday not in SKIP:
        return yesterday
    return None

ADD_ENTRY_JS = """
(function(dateStr) {
    function setReactInput(el, value) {
        var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, value);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }

    // Navigate to Control horario tab first
    var ctrlTab = Array.from(document.querySelectorAll('button')).find(function(b) {
        return b.innerText.trim() === 'Control horario' && b.offsetParent !== null;
    });
    if (ctrlTab) ctrlTab.click();

    setTimeout(function() {
        var addBtn = Array.from(document.querySelectorAll('button')).find(function(b) {
            return b.innerText.trim() === 'Añadir fichaje' && b.offsetParent !== null;
        });
        if (!addBtn) { window._ficharResult = 'error: Añadir fichaje not found'; return; }
        addBtn.click();

        setTimeout(function() {
            var inputs = Array.from(document.querySelectorAll('input')).filter(function(el) {
                return el.offsetParent !== null;
            });
            var dateInput = inputs.find(function(el) {
                return el.type === 'text' && (el.value.indexOf('/') !== -1 || el.value.indexOf('-') !== -1);
            });
            if (dateInput) setReactInput(dateInput, dateStr);

            var timeInputs = inputs.filter(function(el) { return el.placeholder === '00:00'; });
            if (timeInputs[0]) setReactInput(timeInputs[0], '17:00');
            if (timeInputs[1]) setReactInput(timeInputs[1], '21:00');

            setTimeout(function() {
                var aceptar = Array.from(document.querySelectorAll('button')).find(function(b) {
                    return b.innerText.trim() === 'Aceptar' && b.offsetParent !== null;
                });
                if (aceptar) { aceptar.click(); window._ficharResult = 'saved:' + dateStr; }
                else { window._ficharResult = 'error: Aceptar not found'; }
            }, 800);
        }, 1200);
    }, 1500);

    return 'started';
})('DATESTR')
"""

def run_js(js):
    with open('/tmp/holded_sabado.js', 'w') as f:
        f.write(js)
    script = '''
set jsCode to do shell script "cat /tmp/holded_sabado.js"
tell application "Google Chrome"
    tell active tab of front window
        execute javascript jsCode
    end tell
end tell
'''
    r = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=30)
    return r.stdout.strip()

def open_holded():
    script = f'''
tell application "Google Chrome"
    activate
    if (count windows) = 0 then make new window
    set newTab to make new tab at end of tabs of front window with properties {{URL:"https://app.holded.com"}}
    set active tab index of front window to (count tabs of front window)
    delay 12
end tell
'''
    subprocess.run(['osascript', '-e', script], check=True)

def check_result():
    r = subprocess.run(
        ['osascript', '-e', 'tell application "Google Chrome" to tell active tab of front window to execute javascript "window._ficharResult || \'pending\'"'],
        capture_output=True, text=True, timeout=10
    )
    return r.stdout.strip()

def main():
    friday = yesterday_friday()
    if not friday:
        print("Hoy no toca — ayer no fue un viernes en el rango.")
        sys.exit(0)

    date_str = friday.strftime("%d/%m/%Y")
    print(f"Añadiendo fichaje para el viernes {date_str} (17:00–21:00)...")

    open_holded()
    js = ADD_ENTRY_JS.replace('DATESTR', date_str)
    run_js(js)

    import time
    time.sleep(5)
    result = check_result()
    print(f"Resultado: {result}")

if __name__ == "__main__":
    main()
