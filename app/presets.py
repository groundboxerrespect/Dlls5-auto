"""Style presets for the DLLS5 neural rendering engine."""

PRESETS: dict[str, dict] = {
    "photoreal": {
        "description": "Balanced photorealistic neural rendering look.",
        "intensity": 0.70, "bloom": 0.50, "warmth": 0.15,
        "sharpness": 0.40, "contrast": 0.25, "vignette": 0.20,
    },
    "cinematic": {
        "description": "Teal-orange blockbuster grade with deep shadows.",
        "intensity": 0.80, "bloom": 0.55, "warmth": 0.30,
        "sharpness": 0.45, "contrast": 0.40, "vignette": 0.45,
        "teal_orange": True,
    },
    "neon_night": {
        "description": "Cyberpunk neon glow with crushed blacks.",
        "intensity": 0.85, "bloom": 0.75, "warmth": -0.25,
        "sharpness": 0.50, "contrast": 0.55, "vignette": 0.35,
        "saturation_boost": 1.35,
    },
    "soft_skin": {
        "description": "Subsurface-scattering style softening for portraits.",
        "intensity": 0.60, "bloom": 0.35, "warmth": 0.20,
        "sharpness": 0.15, "contrast": 0.10, "vignette": 0.10,
        "soften": 0.5,
    },
    "golden_hour": {
        "description": "Warm sunset glow with long-lens haze.",
        "intensity": 0.75, "bloom": 0.65, "warmth": 0.55,
        "sharpness": 0.30, "contrast": 0.20, "vignette": 0.30,
    },
    "noir": {
        "description": "High-contrast black & white film look.",
        "intensity": 0.90, "bloom": 0.30, "warmth": 0.0,
        "sharpness": 0.60, "contrast": 0.70, "vignette": 0.60,
        "monochrome": True,
    },
}


def get_preset(name: str) -> dict:
    """Return preset params, falling back to 'photoreal'."""
    return dict(PRESETS.get(name, PRESETS["photoreal"]))
