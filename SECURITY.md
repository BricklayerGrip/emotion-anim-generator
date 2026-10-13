# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.6.x   | yes       |
| 0.5.x   | yes       |
| < 0.5   | no        |

## Reporting a vulnerability

Email `security@emotion-anim-generator.dev` with a description, a repro
script, and the affected module. Do not open a public issue for anything
that allows arbitrary code execution via a loaded model or a crafted
`.kf.json`.

## Threat model

This is a **desktop tool that loads user-supplied model files and project
files**. Attack surface:

- `services/backend_loader.py` — dynamic import of third-party backends.
  Backends run in-process. Only load backends you trust.
- `handlers/project_io.py` — parses `.kf.json` and `.emopack` files.
  Malformed files must never crash the app; they must raise `ProjectError`.
- `services/ffmpeg_bridge.py` — shells out to `ffmpeg`. The binary path is
  read from `config/paths.toml` and is never taken from a project file.

## Non-goals

We do not sandbox backends. We do not sign model files. If you load a
model from a stranger, that is on you — this is a hobbyist tool.