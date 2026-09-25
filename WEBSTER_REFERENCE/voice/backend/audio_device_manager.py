"""Lightweight audio-device discovery and selection boundary."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AudioDevice:
    device_id: str
    name: str
    input_channels: int = 0
    output_channels: int = 0

class AudioDeviceManager:
    def __init__(self) -> None:
        self._devices: dict[str, AudioDevice] = {}
        self._selected_input: str | None = None
        self._selected_output: str | None = None

    def register(self, device: AudioDevice) -> None:
        if not device.device_id.strip() or not device.name.strip():
            raise ValueError("device_id and name are required")
        self._devices[device.device_id.strip()] = device

    def devices(self, *, input_only: bool = False, output_only: bool = False) -> tuple[AudioDevice, ...]:
        items = tuple(self._devices.values())
        if input_only:
            items = tuple(d for d in items if d.input_channels > 0)
        if output_only:
            items = tuple(d for d in items if d.output_channels > 0)
        return items

    def select_input(self, device_id: str) -> AudioDevice:
        device = self._devices[device_id.strip()]
        if device.input_channels < 1:
            raise ValueError("device has no input channel")
        self._selected_input = device.device_id
        return device

    def select_output(self, device_id: str) -> AudioDevice:
        device = self._devices[device_id.strip()]
        if device.output_channels < 1:
            raise ValueError("device has no output channel")
        self._selected_output = device.device_id
        return device

    def selected(self) -> tuple[AudioDevice | None, AudioDevice | None]:
        return self._devices.get(self._selected_input), self._devices.get(self._selected_output)
