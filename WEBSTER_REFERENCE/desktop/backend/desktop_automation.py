"""B17 bounded synchronous desktop automation."""
class DesktopAutomation:
    def __init__(self,controller): self.controller=controller
    def run(self,steps,approved=False):
        values=[x.strip() for x in steps.split(" then ") if x.strip()]
        if len(values)>8: raise ValueError("Automation is limited to 8 steps.")
        out=[]
        for step in values:
            r=self.controller.execute(step,approved=approved)
            if not r.ok: return False,out+[r.message]
            out.append(r.message)
        return True,out