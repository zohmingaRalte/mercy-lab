import webview
import os
import sys
import json
import random
from datetime import date

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from print.pdf_generator import generate_pdf

def generate_ref_no():
    return date.today().strftime('ML%Y%m%d') + str(random.randint(100, 999))


class API:
    def print_report(self, patient, sections):
        try:
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

    webview.start(on_shown, debug=False)