# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['AutoCR.py'],
    pathex=['C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\lib'],
    binaries=[],
    datas=[('.\\common.onnx', 'ddddocr'), ('.\\common_old.onnx', 'ddddocr')],
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
    name='AutoCR',
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
    version='versionfile.txt',
)
