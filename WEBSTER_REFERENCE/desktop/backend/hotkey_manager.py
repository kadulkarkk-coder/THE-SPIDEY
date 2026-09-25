"""B16 bounded hotkey sequences."""
from .keyboard_driver import KeyboardDriver
class HotkeyManager:
    def __init__(self): self.keyboard=KeyboardDriver()
    def execute(self,sequence):
        parts=[x.strip() for x in sequence.split(",") if x.strip()]
        if len(parts)>10: raise ValueError("Hotkey sequence limited to 10 actions.")
        out=[]
        for item in parts:
            t=item.replace("+"," ").split(); out.append(self.keyboard.press(t[-1],tuple(t[:-1])))
        return " | ".join(out)