"""Explicit permission boundary for model operations."""
class ModelPermissions:
    READ="ai.model.read"; INFER="ai.model.infer"; LOAD="ai.model.load"
    def __init__(self): self._grants={"local":{self.READ,self.INFER,self.LOAD}}
    def allowed(self,principal,capability): return capability in self._grants.get(principal,set())
    def grant(self,principal,capability): self._grants.setdefault(principal,set()).add(capability)
    def revoke(self,principal,capability): self._grants.get(principal,set()).discard(capability)
