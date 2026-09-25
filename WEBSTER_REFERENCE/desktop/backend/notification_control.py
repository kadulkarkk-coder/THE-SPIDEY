"""B9 notification boundary."""
from __future__ import annotations
class NotificationControl:
    def notify(self,title,message):
        return f"Notification: {title} — {message}"