# Contributing to emotion-anim-generator

Thanks for wanting to help the tater cook. This is a hobbyist desktop tool
that turns text emotion labels into keyframe-driven animation clips. It is
built by and for the open-source animation / AI-tooling crowd.

## Ground rules

- One feature per PR. Small diffs get merged fast.
- Every new emotion driver needs a unit test under `tests/`.
- Every new backend (ONNX, TorchScript, dummy) needs a smoke test that runs
  without a GPU.
- No hardcoded absolute paths. Use `config/paths.toml`.
- Type hints required on public functions. `mypy --strict` on `core/`.

## Dev setup

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m emotion_anim.app --demo
```

## Style

- `ruff` + `black`, line length 100.
- Logging via `emotion_anim.utils.logger.get_logger`, never `print`.
- No bare `except:`.

## Reporting bugs

Open an issue with the CLI command, the emotion label used, the backend,
and the full traceback. Attach the generated `*.kf.json` if the bug is
in the interpolation stage.

## Feature requests

Emotion packs, backend adapters, and export formats are all welcome.
Drop a proposal in `docs/` first if it touches the core engine.