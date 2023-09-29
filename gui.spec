# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['/Users/steve/PycharmProjects/automation_image_generation/model/gui.py', '/Users/steve/PycharmProjects/automation_image_generation/model/generator.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('model', 'model'), ('helpers', 'helpers'), ('data/wordlists/wordlists.json', 'data/wordlists')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
