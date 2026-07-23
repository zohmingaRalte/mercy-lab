import webview
import os
import sys
import json
import random
import threading
import urllib.request
import shutil
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# ── Auto-updater ──────────────────────────────────────────────────────────────
GITHUB_RAW = "https://raw.githubusercontent.com/zohmingaRalte/mercy-lab/main"
UPDATE_FILES = [
    ("ui/index.html",        os.path.join(BASE_DIR, "ui", "index.html")),
    ("print/pdf_generator.py", os.path.join(BASE_DIR, "print", "pdf_generator.py")),
]

def check_and_update():
    """Silently fetch latest files from GitHub and replace local copies if changed."""
    try:
        for remote_path, local_path in UPDATE_FILES:
            url = f"{GITHUB_RAW}/{remote_path}"
            req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                remote_content = resp.read()

            # Only write if content has changed
            if os.path.exists(local_path):
                with open(local_path, "rb") as f:
                    local_content = f.read()
                if local_content == remote_content:
                    continue  # no change, skip

            # Write updated file
            tmp = local_path + ".tmp"
            with open(tmp, "wb") as f:
                f.write(remote_content)
            shutil.move(tmp, local_path)
            print(f"[updater] Updated: {remote_path}")

    except Exception as e:
        # Silent fail — no internet, private repo, etc.
        print(f"[updater] Skipped: {e}")

def run_updater():
    """Run updater in background thread so app starts instantly."""
    t = threading.Thread(target=check_and_update, daemon=True)
    t.start()
    return t

# ── PDF Generator (imported after potential update) ───────────────────────────
def generate_ref_no():
    return date.today().strftime('ML%Y%m%d') + str(random.randint(100, 999))


class API:
    def print_report(self, patient, sections):
        try:
            # Re-import pdf_generator each time so updates take effect
            import importlib
            import print.pdf_generator as pdf_mod
            importlib.reload(pdf_mod)
            out = os.path.join(BASE_DIR, '_temp_print.pdf')
            pdf_mod.generate_pdf(patient, sections, '', out)
            os.startfile(os.path.abspath(out))
            return {'ok': True}
        except Exception as e:
            return {'ok': False, 'error': str(e)}

    def get_ref_no(self):
        return generate_ref_no()

    def get_today(self):
        return date.today().strftime('%d-%m-%Y')


if __name__ == '__main__':
    # Run updater in background — app starts immediately, update happens silently
    updater_thread = run_updater()

    api = API()
    ui  = os.path.join(BASE_DIR, 'ui', 'index.html')

    window = webview.create_window(
        'Mercy Hospital — Lab Entry System',
        url=f'file:///{ui.replace(os.sep, "/")}',
        js_api=api,
        width=1280,
        height=800,
        min_size=(1024, 700)
    )

    def on_shown():
        window.maximize()
        # Wait for updater to finish, then reload UI if index.html was updated
        def reload_if_updated():
            updater_thread.join(timeout=10)
            # Reload the window so updated index.html takes effect
            window.load_url(f'file:///{ui.replace(os.sep, "/")}')
        t = threading.Thread(target=reload_if_updated, daemon=True)
        t.start()

    webview.start(on_shown, debug=False)