"""Emotion vocabulary and blend helpers.

An Emotion is a named, unit-normalized vector over a fixed axis set:
valence, arousal, tension, warmth, energy. Blends are weighted means
followed by renormalization; the result is what the backend consumes.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

AXES: tuple[str, ...] = ("valence", "arousal", "tension", "warmth", "energy")


@dataclass(frozen=True, slots=True)
class Emotion:
    name: str
    vector: np.ndarray  # shape (5,), each in [0, 1]

    def __post_init__(self) -> None:
        if self.vector.shape != (len(AXES),):
            raise ValueError(f"emotion vector must be shape ({len(AXES)},)")


BASIC_PACK: dict[str, Emotion] = {
    "joy": Emotion("joy", np.array([0.92, 0.71, 0.10, 0.80, 0.85])),
    "calm": Emotion("calm", np.array([0.70, 0.20, 0.05, 0.75, 0.15])),
    "anger": Emotion("anger", np.array([0.15, 0.88, 0.95, 0.10, 0.90])),
    "sadness": Emotion("sadness", np.array([0.12, 0.22, 0.55, 0.30, 0.18])),
    "fear": Emotion("fear", np.array([0.10, 0.80, 0.90, 0.20, 0.70])),
    "surprise": Emotion("surprise", np.array([0.60, 0.90, 0.40, 0.45, 0.95])),
}


def blend(parts: dict[str, float], pack: dict[str, Emotion] | None = None) -> Emotion:
    """Weighted blend of named emotions. Weights are normalized to sum 1."""
    table = pack or BASIC_PACK
    acc = np.zeros(len(AXES), dtype=np.float64)
    total = 0.0
    for name, weight in parts.items():
        if name not in table:
            raise KeyError(f"unknown emotion {name!r}")
        if weight < 0:
            raise ValueError(f"weight for {name!r} must be >= 0")
        acc += table[name].vector * weight
        total += weight
    if total <= 0:
        raise ValueError("blend requires at least one positive weight")
    return Emotion("blend", np.clip(acc / total, 0.0, 1.0))