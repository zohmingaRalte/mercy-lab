# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_web.py'],
    pathex=[],
    binaries=[],
    datas=[('ui', 'ui'), ('print', 'print'), ('assets_logo.jpg', '.'), ('signature.jpg', '.'), ('DejaVuSans.ttf', '.'), ('DejaVuSans-Bold.ttf', '.'), ('DejaVuSans-Oblique.ttf', '.'), ('DejaVuSans-BoldOblique.ttf', '.'), ('fontawesome.ttf', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MercyLab',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
