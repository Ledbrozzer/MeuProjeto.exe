# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Server.py'],
    pathex=[],
    binaries=[],
    datas=[('../view/index.html', 'view'), ('../view/App.html', 'view'), ('../view/css/log_style.css', 'view/css'), ('../view/css/reset.css', 'view/css'), ('../view/css/responsive.css', 'view/css'), ('../view/css/style.css', 'view/css'), ('../view/js/script.js', 'view/js'), ('../model/StreamLit_App.py', 'model')],
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
    name='MeuProjeto',
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
