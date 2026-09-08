# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

ROOT = Path(SPEC).resolve().parents[2]
REFERENCE = ROOT / "WEBSTER_REFERENCE"
ICON = ROOT / "packaging" / "windows" / "webster.ico"

PACKAGE = "WEBSTER_REFERENCE"
hiddenimports = collect_submodules(PACKAGE)

analysis = Analysis(
    [str(ROOT / "packaging" / "windows" / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[(str(REFERENCE), "WEBSTER_REFERENCE")],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(analysis.pure)
exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name="WEBSTER",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon=str(ICON),
)
