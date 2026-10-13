"""Keyframe model and interpolation.

A KeyframeSet is an ordered list of (t, pose) pairs. Poses are dense
vectors over the rig's joint channels. Interpolation is cubic Hermite
between adjacent keys with zeroed tangents at the ends.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(slots=True)
class Keyframe:
    t: float  # seconds, monotonically increasing
    pose: np.ndarray  # shape (channels,)


@dataclass(slots=True)
class KeyframeSet:
    keys: list[Keyframe]
    channels: int

    def validate(self) -> None:
        if not self.keys:
            raise ValueError("empty keyframe set")
        last = -1.0
        for kf in self.keys:
            if kf.t <= last:
                raise ValueError("keyframe times must strictly increase")
            if kf.pose.shape != (self.channels,):
                raise ValueError(f"pose shape {kf.pose.shape} != ({self.channels},)")
            last = kf.t


def sample(ks: KeyframeSet, t: float) -> np.ndarray:
    """Sample the interpolated pose at time t (seconds)."""
    ks.validate()
    keys = ks.keys
    if t <= keys[0].t:
        return keys[0].pose.copy()
    if t >= keys[-1].t:
        return keys[-1].pose.copy()
    for i in range(len(keys) - 1):
        a, b = keys[i], keys[i + 1]
        if a.t <= t <= b.t:
            u = (t - a.t) / (b.t - a.t)
            h00 = 2 * u**3 - 3 * u**2 + 1
            h10 = u**3 - 2 * u**2 + u
            h01 = -2 * u**3 + 3 * u**2
            h11 = u**3 - u**2
            span = b.t - a.t
            return h00 * a.pose + h10 * span * _tangent(keys, i) + h01 * b.pose + h11 * span * _tangent(keys, i + 1)
    raise RuntimeError("unreachable")


def _tangent(keys: list[Keyframe], i: int) -> np.ndarray:
    if i == 0 or i == len(keys) - 1:
        return np.zeros_like(keys[i].pose)
    return (keys[i + 1].pose - keys[i - 1].pose) / (keys[i + 1].t - keys[i - 1].t)