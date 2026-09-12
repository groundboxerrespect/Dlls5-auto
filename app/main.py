"""DLLS5-Service — FastAPI application."""

from __future__ import annotations

import io
import random
import zipfile

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image

from .engine import render
from .presets import PRESETS, get_preset

app = FastAPI(
    title="DLLS5-Service",
    description="Self-hosted neural rendering & image generation service "
                "inspired by DLSS 5. Not affiliated with NVIDIA.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

ALLOWED = {"image/png", "image/jpeg", "image/webp", "image/bmp"}


async def _read_image(upload: UploadFile) -> Image.Image:
    if upload.content_type not in ALLOWED:
        raise HTTPException(415, f"Unsupported type {upload.content_type}")
    try:
        return Image.open(io.BytesIO(await upload.read()))
    except Exception as exc:
        raise HTTPException(400, f"Could not decode image: {exc}") from exc


def _build_params(preset: str, intensity: float | None, bloom: float | None,
                  warmth: float | None, sharpness: float | None,
                  scale: float | None, seed: int | None) -> dict:
    random.seed(seed)
    params = get_preset(preset)
    params["scale"] = scale or 1.0
    if intensity is not None:
        params["intensity"] = intensity
    if bloom is not None:
        params["bloom"] = bloom
    if warmth is not None:
        params["warmth"] = warmth
    if sharpness is not None:
        params["sharpness"] = sharpness
    return params


def _png_bytes(img: Image.Image) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


@app.get("/api/presets")
async def presets():
    return {"presets": PRESETS}


@app.get("/health")
async def health():
    return {"status": "ok", "engine": "builtin"}


@app.post("/api/generate")
async def generate(
    file: UploadFile = File(...),
    preset: str = Form("photoreal"),
    intensity: float | None = Form(None),
    bloom: float | None = Form(None),
    warmth: float | None = Form(None),
    sharpness: float | None = Form(None),
    scale: float = Form(1.0),
    seed: int | None = Form(None),
    engine: str = Form("builtin"),
):
    """Enhance/generate an image with the neural rendering pipeline."""
    if engine != "builtin":
        raise HTTPException(501, f"Engine '{engine}' not installed. See docs/ENGINES.md.")
    img = await _read_image(file)
    params = _build_params(preset, intensity, bloom, warmth, sharpness, scale, seed)
    result = render(img, params)
    return Response(content=_png_bytes(result), media_type="image/png",
                    headers={"X-DLLS5-Preset": preset})


@app.post("/api/batch")
async def batch(
    file: UploadFile = File(...),
    preset: str = Form("photoreal"),
    intensity: float = Form(0.7),
    scale: float = Form(1.0),
):
    """Process every image inside an uploaded ZIP and return a ZIP of results."""
    try:
        zin = zipfile.ZipFile(io.BytesIO(await file.read()))
    except zipfile.BadZipFile as exc:
        raise HTTPException(400, "Upload must be a .zip archive") from exc

    buf = io.BytesIO()
    params = _build_params(preset, intensity, None, None, None, scale, None)
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            if name.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                try:
                    img = Image.open(io.BytesIO(zin.read(name)))
                    zout.writestr(f"dlls5_{name}", _png_bytes(render(img, params)))
                except Exception:
                    continue  # skip undecodable entries
    return Response(content=buf.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": 'attachment; filename="dlls5_results.zip"'})
