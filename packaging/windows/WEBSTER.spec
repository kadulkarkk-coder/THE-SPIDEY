# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

ROOT = Path(SPEC).resolve().parents[2]
REFERENCE = ROOT / "WEBSTER_REFERENCE"

hiddenimports = collect_submodules("core") + collect_submodules("intelligence") + collect_submodules("memory") + collect_submodules("agents") + collect_submodules("tools") + collect_submodules("automation") + collect_submodules("browser") + collect_submodules("desktop") + collect_submodules("voice") + collect_submodules("vision") + collect_submodules("gesture") + collect_submodules("orb") + collect_submodules("widgets") + collect_submodules("ui") + collect_submodules("security") + collect_submodules("plugins") + collect_submodules("evolution") + collect_submodules("testing") + collect_submodules("integration")

analysis = Analysis(
    [str(ROOT / "packaging" / "windows" / "launcher.py")],
    pathex=[str(REFERENCE)],
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
)
