"""Bounded in-memory model response cache."""
from __future__ import annotations
from collections import OrderedDict
class ModelCache:
    def __init__(self,max_items=32): self.max_items=max_items; self._data=OrderedDict()
    def get(self,key):
        value=self._data.get(key)
        if value is not None:self._data.move_to_end(key)
        return value
    def put(self,key,value):
        self._data[key]=value; self._data.move_to_end(key)
        while len(self._data)>self.max_items:self._data.popitem(last=False)
    def clear(self): self._data.clear()
