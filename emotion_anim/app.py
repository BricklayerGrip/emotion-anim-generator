"""Bootstrap entry point for emotion-anim-generator.

Wires config -> backend -> core engine -> handlers and hands control to
the CLI shell. This is the only module allowed to touch sys.argv.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from emotion_anim.config.settings import load_settings
from emotion_anim.core.engine import AnimationEngine
from emotion_anim.handlers.cli_shell import CliShell
from emotion_anim.services.backend_loader import load_backend
from emotion_anim.utils.logger import get_logger

log = get_logger("app")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="emotion-anim",
        description="Generate animation clips from emotion labels.",
    )
    p.add_argument("--config", type=Path, default=None, help="path to settings.toml")
    p.add_argument("--backend", default="dummy", help="backend name (dummy|onnx)")
    p.add_argument("--demo", action="store_true", help="run a scripted demo clip")
    p.add_argument("--project", type=Path, default=None, help="open a .kf.json project")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings(args.config)
    backend = load_backend(args.backend, settings)
    engine = AnimationEngine(settings=settings, backend=backend)
    shell = CliShell(engine=engine, settings=settings)
    if args.demo:
        return shell.run_demo()
    if args.project is not None:
        return shell.open_project(args.project)
    return shell.run_interactive()


if __name__ == "__main__":
    sys.exit(main())