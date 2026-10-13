"""Animation engine: orchestrates backend inference and keyframe assembly."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from emotion_anim.config.settings import Settings
from emotion_anim.core.emotion import Emotion
from emotion_anim.core.keyframe import Keyframe, KeyframeSet
from emotion_anim.services.backend_base import AnimationBackend
from emotion_anim.utils.logger import get_logger

log = get_logger("engine")


@dataclass(slots=True)
class Clip:
    fps: int
    frames: np.ndarray  # shape (n_frames, channels)


class AnimationEngine:
    """Turns an Emotion into a Clip via the configured backend."""

    def __init__(self, settings: Settings, backend: AnimationBackend) -> None:
        self.settings = settings
        self.backend = backend

    def generate(self, emotion: Emotion, duration_s: float | None = None) -> Clip:
        dur = duration_s or self.settings.render.duration_s
        fps = self.settings.render.fps
        n_frames = max(2, int(round(dur * fps)))
        log.info("generate emotion=%s frames=%d backend=%s", emotion.name, n_frames, self.backend.name)
        keys = self.backend.predict_keyframes(emotion.vector, n_frames=n_frames)
        ks = KeyframeSet(keys=keys, channels=self.backend.channels)
        times = np.linspace(0.0, dur, n_frames, endpoint=False)
        frames = np.stack([_sample_or_pose(ks, float(t)) for t in times])
        return Clip(fps=fps, frames=frames)

    def keyframes(self, emotion: Emotion, n: int = 6) -> KeyframeSet:
        keys = self.backend.predict_keyframes(emotion.vector, n_frames=n)
        return KeyframeSet(keys=keys, channels=self.backend.channels)


def _sample_or_pose(ks: KeyframeSet, t: float) -> np.ndarray:
    from emotion_anim.core.keyframe import sample

    return sample(ks, t)
</｜｜DSML｜｜ parameter>