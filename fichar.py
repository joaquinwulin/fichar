#!/usr/bin/env python3
"""Automatiza el fichaje en Holded usando Chrome real vía AppleScript + JS."""

import subprocess
import sys
import time
import datetime

HOLDED_URL = "https://app.holded.com"

# JS injected into Chrome to find and click the clock button.
# Writes the JS to a temp file to avoid AppleScript string-escaping hell.
FIND_CLICK_JS = r"""
(function() { try {
    var allBtns = Array.from(document.querySelectorAll('button'));
    var allEls  = Array.from(document.querySelectorAll('*'));

    function visibleBtn(b) { return b.offsetParent !== null && b.offsetWidth > 0; }

    // After clicking stop, polls for the "Sí, he terminado" confirmation popup
    function confirmIfNeeded() {
        var waited = 0;
        var poll = setInterval(function() {
            waited += 200;
            var confirmBtn = Array.from(document.querySelectorAll('button')).find(function(b) {
                return b.innerText.trim().indexOf('terminado') !== -1 && b.offsetParent !== null;
            });
            if (confirmBtn) { clearInterval(poll); confirmBtn.click(); }
            if (waited > 5000) clearInterval(poll);
        }, 200);
    }

    // 1. Text buttons
    var patterns = ['Fichar entrada','Fichar salida','Clock in','Clock out','Check in','Check out'];
    for (var i = 0; i < patterns.length; i++) {
        var btn = allBtns.find(function(b) { return b.innerText.trim() === patterns[i]; });
        if (btn && visibleBtn(btn)) { btn.click(); confirmIfNeeded(); return 'clicked:' + patterns[i]; }
    }

    // 2. Find element with connection status text (flexible)
    var statusEl = allEls.find(function(el) {
        var t = el.innerText ? el.innerText.trim() : '';
        return (t === 'Desconectado' || t === 'Conectado') && visibleBtn(el);
    });
    if (!statusEl) {
        statusEl = allEls.find(function(el) {
            var t = el.textContent.trim();
            return el.children.length <= 1 && (t.indexOf('Desconectado') !== -1 || t.indexOf('Conectado') !== -1);
        });
    }
    if (statusEl) {
        var par = statusEl.parentElement;
        for (var j = 0; j < 8; j++) {
            if (!par) break;
            var b = par.querySelector('button');
            if (b && visibleBtn(b)) {
                b.click(); confirmIfNeeded();
                return 'clicked:timer:' + statusEl.textContent.trim().substring(0, 20);
            }
            par = par.parentElement;
        }
    }

    // 3. Find timer by time pattern (e.g. "00h 00m 00s")
    var timeEl = allEls.find(function(el) {
        return el.children.length === 0 && /\d+h\s*\d+m/.test(el.textContent.trim());
    });
    if (timeEl) {
        var par2 = timeEl.parentElement;
        for (var k = 0; k < 8; k++) {
            if (!par2) break;
            var b2 = par2.querySelector('button');
            if (b2 && visibleBtn(b2)) {
                b2.click(); confirmIfNeeded();
                return 'clicked:timer-time:' + timeEl.textContent.trim().substring(0, 20);
            }
            par2 = par2.parentElement;
        }
    }

    // 4. Debug dump
    var vis = allBtns
        .filter(visibleBtn)
        .map(function(b, idx) {
            return idx + '|' + (b.innerText.trim() || b.title || b.getAttribute('aria-label') || '(icon)') + '|' + b.className.split(' ')[1];
        });
    return 'not_found|' + vis.join('||');
} catch(e) { return 'js_error:' + e.toString(); } })()
"""


JS_TMP = "/tmp/holded_fichar.js"


def run_js_in_chrome(js: str) -> str:
    """Write JS to a fixed temp path and execute it in Chrome's active tab."""
    with open(JS_TMP, 'w') as f:
        f.write(js)
    script = f'''
set jsCode to do shell script "cat {JS_TMP}"
tell application "Google Chrome"
    tell active tab of front window
        execute javascript jsCode
    end tell
end tell
'''
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"AppleScript stderr: {result.stderr.strip()}")
    return result.stdout.strip()


def open_holded_tab():
    """Open a new Holded tab in Chrome, make it active, wait for load inside AppleScript."""
    script = f'''
tell application "Google Chrome"
    activate
    if (count windows) = 0 then make new window
    set newTab to make new tab at end of tabs of front window with properties {{URL:"{HOLDED_URL}"}}
    set active tab index of front window to (count tabs of front window)
    delay 12
end tell
'''
    print("Esperando que cargue Holded (12s)...")
    subprocess.run(['osascript', '-e', script], check=True)


def main():
    print("Abriendo Holded en Chrome...")
    open_holded_tab()

    print("Buscando botón de fichaje...")
    result = run_js_in_chrome(FIND_CLICK_JS)

    if result.startswith('clicked:'):
        action = result[len('clicked:'):]
        hora = datetime.datetime.now().strftime("%H:%M")
        if 'entrada' in action.lower() or 'in' in action.lower() or 'Desconectado' in action:
            tipo = "ENTRADA"
        else:
            tipo = "SALIDA"
        time.sleep(3)  # wait for confirmation popup to be clicked before closing
        print(f"Fichaje de {tipo} registrado a las {hora}.")
    elif result.startswith('not_found'):
        parts = result.split('|')
        print("No se encontró el botón de fichaje.")
        print("Botones visibles:")
        for p in parts[1:]:
            if p:
                print(f"  {p}")
        sys.exit(1)
    else:
        print(f"Resultado inesperado: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
