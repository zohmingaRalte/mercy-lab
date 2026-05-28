# MercyLab — Source Recovery

Recovered from MercyLab.exe (PyInstaller bundle, Python 3.11).

## Project Structure
```
MercyLab_source/
├── main_web.py           # Entry point — pywebview app
├── requirements.txt      # pip dependencies
├── ui/
│   └── index.html        # Frontend UI
└── print/
    ├── __init__.py
    └── pdf_generator.py  # FPDF2-based PDF report generator
```

## Assets needed (copy from original .exe extraction or your project folder)
- assets_logo.jpg
- DejaVuSans.ttf / DejaVuSans-Bold.ttf / DejaVuSans-Oblique.ttf / DejaVuSans-BoldOblique.ttf
- fontawesome.ttf

## Run
```
pip install -r requirements.txt
python main_web.py
```

## Build .exe
```
pip install pyinstaller
pyinstaller --noconsole --onefile --add-data "ui;ui" --add-data "print;print" \
  --add-data "assets_logo.jpg;." --add-data "*.ttf;." main_web.py
```
