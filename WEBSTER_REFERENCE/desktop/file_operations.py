"""B8 bounded local file operations."""
from __future__ import annotations
from pathlib import Path
import shutil
class FileOperations:
    ALLOWED={".txt",".md",".py",".json",".csv",".log",".ini",".yaml",".yml",".xml",".html",".css",".js"}
    def path(self,value): return Path(value).expanduser().resolve()
    def read(self,value,limit=12000):
        p=self.path(value)
        if p.suffix.lower() not in self.ALLOWED: raise ValueError("Only approved text files can be read.")
        if not p.is_file(): raise FileNotFoundError(str(p))
        return p.read_text(encoding="utf-8",errors="replace")[:limit]
    def list_dir(self,value="."):
        p=self.path(value)
        if not p.is_dir(): raise NotADirectoryError(str(p))
        return tuple(x.name for x in sorted(p.iterdir(),key=lambda x:x.name.casefold())[:100])
    def copy(self,src,dst):
        s,d=self.path(src),self.path(dst)
        if not s.is_file(): raise FileNotFoundError(str(s))
        shutil.copy2(s,d); return f"Copied {s} to {d}"