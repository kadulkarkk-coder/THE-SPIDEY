# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules
ROOT=Path(SPEC).resolve().parents[2]
analysis=Analysis(
 [str(ROOT/"packaging"/"windows"/"abc_launcher.py")],
 pathex=[str(ROOT)], binaries=[], datas=[],
 hiddenimports=collect_submodules("WEBSTER_REFERENCE.runtime")+collect_submodules("WEBSTER_REFERENCE.desktop")+collect_submodules("WEBSTER_REFERENCE.ai")+collect_submodules("WEBSTER_REFERENCE.intelligence")+collect_submodules("WEBSTER_REFERENCE.memory"),
 hookspath=[],hooksconfig={},runtime_hooks=[],
 excludes=["WEBSTER_REFERENCE.browser","WEBSTER_REFERENCE.automation","WEBSTER_REFERENCE.gesture","WEBSTER_REFERENCE.orb","WEBSTER_REFERENCE.ui","WEBSTER_REFERENCE.vision","WEBSTER_REFERENCE.voice","WEBSTER_REFERENCE.widgets","WEBSTER_REFERENCE.mobile","WEBSTER_REFERENCE.integration","WEBSTER_REFERENCE.plugins","WEBSTER_REFERENCE.evolution"],
 noarchive=False)
pyz=PYZ(analysis.pure)
exe=EXE(pyz,analysis.scripts,analysis.binaries,analysis.datas,[],name="WEBSTER_ABC",debug=False,bootloader_ignore_signals=False,strip=False,upx=False,console=True)
