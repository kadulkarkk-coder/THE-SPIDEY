"""B13 allowlisted read-only shell commands."""
import subprocess
class SafeShell:
    ALLOWED={"whoami":["whoami"],"hostname":["hostname"],"where python":["where","python"],"python version":["python","--version"],"ipconfig":["ipconfig"]}
    def run(self,name):
        key=name.strip().casefold()
        if key not in self.ALLOWED: raise PermissionError("Shell command is not allowlisted.")
        r=subprocess.run(self.ALLOWED[key],capture_output=True,text=True,timeout=5,shell=False)
        return (r.stdout or r.stderr).strip()[:4000]