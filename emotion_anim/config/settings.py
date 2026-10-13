"""Settings loader. Reads TOML, validates via pydantic, applies defaults."""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

if sys.version_info >= (3, 11):
    import tomllib
else:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]

from emotion_anim.utils.logger import get_logger

log = get_logger("config")

DEFAULT_CONFIG = Path(__file__).with_name("defaults.toml")


class RenderSettings(BaseModel):
    fps: int = Field(default=24, ge=1, le=120)
    width: int = Field(default=512, ge=64, le=4096)
    height: int = Field(default=512, ge=64, le=4096)
    duration_s: float = Field(default=2.0, gt=0, le=120)


class BackendSettings(BaseModel):
    name: str = "dummy"
    model_path: Path | None = None
    device: str = "cpu"


class Settings(BaseModel):
    render: RenderSettings = RenderSettings()
    backend: BackendSettings = BackendSettings()
    emotion_pack: str = "basic_v1"
    ffmpeg_path: Path | None = None


def load_settings(path: Path | None) -> Settings:
    src = path or DEFAULT_CONFIG
    if not src.exists():
        log.warning("config not found at %s, using built-in defaults", src)
        return Settings()
    with src.open("rb") as fh:
        raw: dict[str, Any] = tomllib.load(fh)
    return Settings.model_validate(raw)