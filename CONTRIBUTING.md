# Contributing to DLLS5-Service

1. Fork the repo and create a branch: `git checkout -b feat/my-feature`
2. Install deps: `pip install -r requirements.txt`
3. Run locally: `uvicorn app.main:app --reload`
4. Test your change, then open a PR against `main`

## Guidelines
- Keep the built-in engine dependency-light (Pillow + NumPy only)
- New presets go in `app/presets.py`
- New pipeline passes go in `app/engine.py` and must be optional/no-op at strength 0
