# 🔌 Pluggable Engines

The built-in engine (`engine=builtin`) is pure Pillow/NumPy. To use a real
diffusion model as a backend:

## Option A — ComfyUI bridge
1. Run ComfyUI locally (`--port 8188`)
2. Set `DLLS5_COMFY_URL=http://localhost:8188` and pass `engine=diffusion`
3. The service forwards the image to your workflow and returns the result

## Option B — diffusers
Install `diffusers` + `torch`, then set `DLLS5_ENGINE=diffusion`.
A ControlNet/img2img pipeline will be used for the "neural render" pass.
