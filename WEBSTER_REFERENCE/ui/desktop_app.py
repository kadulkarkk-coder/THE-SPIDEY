"""Native Windows desktop client for WEBSTER Mark D.

The client is intentionally lightweight: Tkinter provides the shell, OpenCV
provides optional live camera frames, and Windows Speech APIs provide voice
input/output without a permanently running microphone or camera loop.
"""
from __future__ import annotations

import os
import queue
import subprocess
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

try:
    import cv2
    from PIL import Image, ImageTk
except ImportError:  # Camera is an optional runtime capability.
    cv2 = None
    Image = ImageTk = None

from ..core.application import WebsterApplication


class WebsterDesktopApp:
    """Full desktop shell around the existing WEBSTER application services."""

    BG = "#08090d"
    PANEL = "#11141b"
    PANEL2 = "#171b24"
    RED = "#e31b23"
    TEXT = "#f3f4f6"
    MUTED = "#9aa3b2"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("WEBSTER — Mark D")
        self.root.geometry("1400x880")
        self.root.minsize(1050, 700)
        self.root.configure(bg=self.BG)
        self.app = WebsterApplication()
        self.app.start()
        self.camera = None
        self.camera_running = False
        self.camera_job = None
        self.voice_busy = False
        self.events: queue.Queue[tuple[str, str]] = queue.Queue()
        self._build()
        self._refresh_status()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _build(self) -> None:
        header = tk.Frame(self.root, bg=self.BG, height=72)
        header.pack(fill="x", padx=22, pady=(16, 8))
        tk.Label(header, text="WEBSTER", font=("Segoe UI", 25, "bold"), fg=self.TEXT, bg=self.BG).pack(side="left")
        tk.Label(header, text="  MARK D", font=("Segoe UI", 11, "bold"), fg=self.RED, bg=self.BG).pack(side="left", pady=(8, 0))
        self.status_label = tk.Label(header, text="● ONLINE", font=("Segoe UI", 10, "bold"), fg="#58d68d", bg=self.BG)
        self.status_label.pack(side="right", pady=10)

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True, padx=22, pady=8)
        sidebar = tk.Frame(body, bg=self.PANEL, width=220)
        sidebar.pack(side="left", fill="y", padx=(0, 12))
        sidebar.pack_propagate(False)
        for label, command in (
            ("⌂  Dashboard", self.show_dashboard),
            ("✦  Chat", self.focus_chat),
            ("◉  Camera", self.toggle_camera),
            ("◌  Voice", self.voice_input),
            ("⚙  System", self.show_system),
        ):
            tk.Button(sidebar, text=label, command=command, anchor="w", relief="flat", bd=0,
                      bg=self.PANEL, fg=self.TEXT, activebackground=self.PANEL2,
                      activeforeground=self.TEXT, font=("Segoe UI", 11), padx=18, pady=14).pack(fill="x", pady=2)
        tk.Label(sidebar, text="LOCAL-FIRST\nOFFLINE READY\n\nCAMERA: ON DEMAND\nVOICE: ON DEMAND", justify="left",
                 font=("Segoe UI", 9), fg=self.MUTED, bg=self.PANEL, padx=18, pady=20).pack(side="bottom", fill="x")

        content = tk.Frame(body, bg=self.BG)
        content.pack(side="left", fill="both", expand=True)
        self._build_chat(content)
        self._build_camera(content)
        self._build_system(content)

    def _build_chat(self, parent: tk.Frame) -> None:
        self.chat_panel = tk.Frame(parent, bg=self.PANEL)
        self.chat_panel.pack(fill="both", expand=True)
        tk.Label(self.chat_panel, text="Conversation", font=("Segoe UI", 17, "bold"), fg=self.TEXT, bg=self.PANEL).pack(anchor="w", padx=20, pady=(18, 4))
        self.chat = scrolledtext.ScrolledText(self.chat_panel, wrap="word", bg=self.PANEL, fg=self.TEXT,
                                              insertbackground=self.TEXT, relief="flat", bd=0,
                                              font=("Segoe UI", 11), padx=16, pady=12)
        self.chat.pack(fill="both", expand=True, padx=12, pady=8)
        self.chat.insert("end", "WEBSTER  ›  Online. Local-first intelligence ready.\n\n")
        self.chat.configure(state="disabled")
        bottom = tk.Frame(self.chat_panel, bg=self.PANEL)
        bottom.pack(fill="x", padx=12, pady=14)
        self.entry = tk.Entry(bottom, bg=self.PANEL2, fg=self.TEXT, insertbackground=self.TEXT,
                              relief="flat", font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 8))
        self.entry.bind("<Return>", lambda _e: self.send())
        tk.Button(bottom, text="Send", command=self.send, bg=self.RED, fg="white", relief="flat", bd=0,
                  font=("Segoe UI", 10, "bold"), padx=20, pady=10).pack(side="right")
        tk.Button(bottom, text="🎙 Voice", command=self.voice_input, bg=self.PANEL2, fg=self.TEXT,
                  relief="flat", bd=0, padx=12, pady=10).pack(side="right", padx=6)

    def _build_camera(self, parent: tk.Frame) -> None:
        self.camera_panel = tk.Frame(parent, bg=self.PANEL)
        self.camera_panel.pack_forget()
        top = tk.Frame(self.camera_panel, bg=self.PANEL)
        top.pack(fill="x", padx=20, pady=18)
        tk.Label(top, text="Vision / Camera", font=("Segoe UI", 17, "bold"), fg=self.TEXT, bg=self.PANEL).pack(side="left")
        tk.Button(top, text="Close camera", command=self.toggle_camera, bg=self.PANEL2, fg=self.TEXT, relief="flat", bd=0, padx=12, pady=8).pack(side="right")
        self.camera_view = tk.Label(self.camera_panel, text="Camera is off", bg="#050609", fg=self.MUTED, font=("Segoe UI", 13))
        self.camera_view.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.camera_info = tk.Label(self.camera_panel, text="Live frames are processed only while camera mode is active.", fg=self.MUTED, bg=self.PANEL)
        self.camera_info.pack(anchor="w", padx=20, pady=(0, 16))

    def _build_system(self, parent: tk.Frame) -> None:
        self.system_panel = tk.Frame(parent, bg=self.PANEL)
        self.system_panel.pack_forget()
        tk.Label(self.system_panel, text="System & WEBSTER Status", font=("Segoe UI", 17, "bold"), fg=self.TEXT, bg=self.PANEL).pack(anchor="w", padx=20, pady=18)
        self.system_text = scrolledtext.ScrolledText(self.system_panel, bg=self.PANEL, fg=self.TEXT, relief="flat", font=("Consolas", 10))
        self.system_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _hide_views(self) -> None:
        for panel in (self.chat_panel, self.camera_panel, self.system_panel):
            panel.pack_forget()

    def show_dashboard(self) -> None:
        self._hide_views(); self.chat_panel.pack(fill="both", expand=True)
        self._append("WEBSTER", "Dashboard ready. Use the sidebar to open Chat, Camera, Voice or System.")

    def focus_chat(self) -> None:
        self._hide_views(); self.chat_panel.pack(fill="both", expand=True); self.entry.focus_set()

    def show_system(self) -> None:
        self._hide_views(); self.system_panel.pack(fill="both", expand=True)
        status = self.app.status()
        self.system_text.delete("1.0", "end")
        self.system_text.insert("end", "WEBSTER MARK D\n" + "=" * 60 + "\n")
        for key, value in status.items():
            self.system_text.insert("end", f"{key:18} {value}\n")
        self.system_text.insert("end", "\nCapabilities wired into this client:\n• Core runtime\n• Intelligence / planning\n• Memory / knowledge\n• Agents / tools / automation\n• Browser / desktop contracts\n• Voice controls\n• Vision / camera\n• Gesture / floating orb / widgets\n• Plugins / evolution / security\n")

    def send(self) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, "end")
        self._append("YOU", text)
        threading.Thread(target=self._answer, args=(text,), daemon=True).start()

    def _answer(self, text: str) -> None:
        try:
            answer = self.app.command(text)
        except Exception as exc:
            answer = f"Error: {exc}"
        self.root.after(0, lambda: self._append("WEBSTER", answer))

    def _append(self, speaker: str, text: str) -> None:
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{speaker}  ›  {text}\n\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def toggle_camera(self) -> None:
        if self.camera_running:
            self.camera_running = False
            if self.camera_job:
                self.root.after_cancel(self.camera_job)
                self.camera_job = None
            if self.camera is not None:
                self.camera.release()
                self.camera = None
            self.show_dashboard()
            return
        self._hide_views(); self.camera_panel.pack(fill="both", expand=True)
        if cv2 is None or Image is None:
            self.camera_view.configure(text="Camera support is unavailable in this build.\nOpenCV/Pillow were not loaded.", image="")
            return
        self.camera = cv2.VideoCapture(0)
        if not self.camera.isOpened():
            self.camera.release(); self.camera = None
            self.camera_view.configure(text="Unable to open the default camera. Check Windows camera permissions.", image="")
            return
        self.camera_running = True
        self._camera_frame()

    def _camera_frame(self) -> None:
        if not self.camera_running or self.camera is None:
            return
        ok, frame = self.camera.read()
        if ok:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image.thumbnail((1100, 650))
            photo = ImageTk.PhotoImage(image=image)
            self.camera_view.configure(image=photo, text="")
            self.camera_view.image = photo
        self.camera_job = self.root.after(33, self._camera_frame)

    def voice_input(self) -> None:
        if self.voice_busy:
            return
        self.voice_busy = True
        self._append("WEBSTER", "Listening… speak a command. (Windows Speech Recognition)")
        threading.Thread(target=self._voice_worker, daemon=True).start()

    def _voice_worker(self) -> None:
        script = (
            "Add-Type -AssemblyName System.Speech; "
            "$r=New-Object System.Speech.Recognition.SpeechRecognitionEngine; "
            "$r.SetInputToDefaultAudioDevice(); "
            "$r.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar)); "
            "$x=$r.Recognize(); if($x){$x.Text}"
        )
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                                    capture_output=True, text=True, timeout=30, creationflags=0x08000000)
            text = result.stdout.strip()
            if not text:
                raise RuntimeError(result.stderr.strip() or "No speech was recognized")
            self.root.after(0, lambda: (self.entry.delete(0, "end"), self.entry.insert(0, text), self.send()))
        except Exception as exc:
            self.root.after(0, lambda: self._append("WEBSTER", f"Voice input unavailable: {exc}"))
        finally:
            self.root.after(0, self._voice_done)

    def _voice_done(self) -> None:
        self.voice_busy = False

    def _refresh_status(self) -> None:
        if self.app.status().get("healthy"):
            self.status_label.configure(text="● ONLINE", fg="#58d68d")
        else:
            self.status_label.configure(text="● DEGRADED", fg="#f4c542")
        self.root.after(3000, self._refresh_status)

    def close(self) -> None:
        self.camera_running = False
        if self.camera is not None:
            self.camera.release()
        self.app.stop()
        self.root.destroy()


def launch() -> None:
    root = tk.Tk()
    WebsterDesktopApp(root)
    root.mainloop()
