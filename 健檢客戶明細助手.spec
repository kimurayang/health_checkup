# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['health_checkup_ui.py'],
    pathex=[],
    binaries=[],
    datas=[('msyh.ttf', '.'), ('translations_en.json', '.')],
    hiddenimports=['pandas', 'openpyxl', 'reportlab', 'reportlab.pdfbase', 'reportlab.lib', 'reportlab.platypus', 'json', 'threading'],
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
    [],
    exclude_binaries=True,
    name='健檢客戶明細助手',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='健檢客戶明細助手',
)
