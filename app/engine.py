"""DLLS5 neural rendering engine (built-in, CPU-friendly).

Multi-pass image pipeline inspired by generative neural rendering:
  1. Smart upscale (Lanczos)
  2. Soft-light / bloom diffusion
  3. Filmic tone mapping (Reinhard + contrast curve)
  4. Color grading (warmth, teal-orange, saturation, monochrome)
  5. Adaptive unsharp masking (detail preservation)
  6. Vignette finish
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance


def _to_array(img: Image.Image) -> np.ndarray:
    return np.asarray(img.convert("RGB"), dtype=np.float32) / 255.0


def _to_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGB")


def smart_upscale(img: Image.Image, scale: float) -> Image.Image:
    if scale <= 1.0:
        return img
    w, h = img.size
    return img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)


def bloom_pass(img: Image.Image, strength: float) -> Image.Image:
    """Screen-blend a heavily blurred, brightened copy of the image."""
    if strength <= 0:
        return img
    glow = img.filter(ImageFilter.GaussianBlur(radius=max(4, img.width // 60)))
    glow = ImageEnhance.Brightness(glow).enhance(1.0 + strength)
    return Image.blend(img, Image.composite(
        Image.new("RGB", img.size, (255, 255, 255)), glow, glow.convert("L")
    ).point(lambda p: min(255, p)), strength * 0.5) if False else _screen_blend(img, glow, strength * 0.45)


def _screen_blend(a: Image.Image, b: Image.Image, t: float) -> Image.Image:
    aa, bb = _to_array(a), _to_array(b)
    out = 1.0 - (1.0 - aa) * (1.0 - bb)
    return _to_image(aa * (1 - t) + out * t)


def filmic_tone_map(img: Image.Image, contrast: float) -> Image.Image:
    """Reinhard tone mapping + S-curve for cinematic contrast."""
    x = _to_array(img)
    x = x / (1.0 + x)                      # Reinhard
    x = np.clip(x, 0, 1)
    # S-curve around 0.5
    x = x + contrast * (x - x**2) * (2 * x - 1) * -1.2
    return _to_image(x)


def color_grade(img: Image.Image, warmth: float = 0.0,
                saturation: float = 1.0, teal_orange: bool = False,
                monochrome: bool = False) -> Image.Image:
    arr = _to_array(img)
    # Warmth: shift R up, B down
    arr[..., 0] *= 1.0 + 0.15 * warmth
    arr[..., 2] *= 1.0 - 0.15 * warmth
    img = _to_image(arr)
    img = ImageEnhance.Color(img).enhance(0.0 if monochrome else saturation)
    if teal_orange and not monochrome:
        a = _to_array(img)
        lum = a.mean(axis=2)
        a[..., 0] = np.clip(a[..., 0] + (lum - 0.5) * 0.25, 0, 1)   # orange highlights
        a[..., 2] = np.clip(a[..., 2] + (0.5 - lum) * 0.20, 0, 1)   # teal shadows
        img = _to_image(a)
    return img


def adaptive_sharpen(img: Image.Image, amount: float) -> Image.Image:
    if amount <= 0:
        return img
    return img.filter(ImageFilter.UnsharpMask(radius=2, percent=int(180 * amount), threshold=2))


def vignette(img: Image.Image, strength: float) -> Image.Image:
    if strength <= 0:
        return img
    w, h = img.size
    y, x = np.ogrid[:h, :w]
    cx, cy = w / 2, h / 2
    dist = np.sqrt(((x - cx) / cx) ** 2 + ((y - cy) / cy) ** 2)
    mask = np.clip(1.0 - strength * np.clip(dist - 0.6, 0, None) ** 2, 0, 1)
    arr = _to_array(img) * mask[..., None]
    return _to_image(arr)


def soft_pass(img: Image.Image, amount: float) -> Image.Image:
    """Subsurface-scattering style softening for skin presets."""
    if amount <= 0:
        return img
    blurred = img.filter(ImageFilter.GaussianBlur(radius=3))
    return Image.blend(img, blurred, amount * 0.6)


def render(img: Image.Image, params: dict) -> Image.Image:
    """Run the full DLLS5 neural rendering pipeline."""
    img = smart_upscale(img, params.get("scale", 1.0))
    img = bloom_pass(img, params.get("bloom", 0.5) * params.get("intensity", 0.7))
    img = soft_pass(img, params.get("soften", 0.0) * params.get("intensity", 0.7))
    img = filmic_tone_map(img, params.get("contrast", 0.25))
    img = color_grade(
        img,
        warmth=params.get("warmth", 0.15),
        saturation=params.get("saturation_boost", 1.0),
        teal_orange=params.get("teal_orange", False),
        monochrome=params.get("monochrome", False),
    )
    img = adaptive_sharpen(img, params.get("sharpness", 0.4))
    img = vignette(img, params.get("vignette", 0.2))
    return img
