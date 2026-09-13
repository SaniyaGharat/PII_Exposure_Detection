"""
PII Exposure Detection - Scanned Document Simulator
Simulates realistic OCR scanner artifacts (rotation, gaussian noise, blur,
contrast shift, JPEG compression artifacts) using Pillow.
"""

import io
import random
from pathlib import Path
from typing import Union
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


def simulate_scanned_document(
    text_content: str,
    output_image_path: Union[str, Path],
    seed: int = 42,
) -> Path:
    """
    Renders text to an image canvas and applies mild, realistic scanner degradation.

    Degradation effects include:
    - Subtle paper background tint and texture
    - Slight rotation skew (±0.5° to ±1.5°)
    - Mild Gaussian noise
    - Slight blur
    - Reduced contrast / brightness variation
    - JPEG compression artifacts

    Args:
        text_content: The text content of the document.
        output_image_path: Path to save the resulting .png file.
        seed: Random seed for deterministic simulation.

    Returns:
        Path to the generated scanned image.
    """
    rng = random.Random(seed)
    output_path = Path(output_image_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Standard A4 / Letter proportion canvas at high DPI
    width, height = 1200, 1600

    # Slight off-white / scanner background tint
    bg_r = rng.randint(245, 252)
    bg_g = rng.randint(245, 252)
    bg_b = rng.randint(240, 248)
    image = Image.new("RGB", (width, height), color=(bg_r, bg_g, bg_b))
    draw = ImageDraw.Draw(image)

    # Load standard or fallback font
    font = None
    try:
        # Try common system monospace fonts
        for font_name in ["cour.ttf", "consola.ttf", "DejaVuSansMono.ttf", "arial.ttf"]:
            try:
                font = ImageFont.truetype(font_name, 20)
                break
            except (IOError, OSError):
                continue
    except Exception:
        font = None

    if font is None:
        font = ImageFont.load_default()

    # Draw text onto canvas
    margin_x = 70
    margin_y = 70
    line_spacing = 24
    curr_y = margin_y

    for line in text_content.split("\n"):
        if curr_y > height - margin_y:
            break
        # Slightly vary text ink density
        ink_shade = rng.randint(15, 35)
        draw.text((margin_x, curr_y), line, fill=(ink_shade, ink_shade, ink_shade), font=font)
        curr_y += line_spacing

    # 1. Subtle Rotation (Skew)
    angle = rng.uniform(-1.2, 1.2)
    image = image.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(bg_r, bg_g, bg_b))

    # 2. Add Mild Gaussian / Sensor Noise
    pixels = image.load()
    w, h = image.size
    # Sparse mild noise for speed and realistic appearance
    noise_density = 0.08
    for _ in range(int(w * h * noise_density)):
        nx = rng.randint(0, w - 1)
        ny = rng.randint(0, h - 1)
        noise = rng.randint(-25, 25)
        r, g, b = pixels[nx, ny]
        pixels[nx, ny] = (
            max(0, min(255, r + noise)),
            max(0, min(255, g + noise)),
            max(0, min(255, b + noise)),
        )

    # 3. Slight Gaussian Blur
    image = image.filter(ImageFilter.GaussianBlur(radius=rng.uniform(0.3, 0.6)))

    # 4. Contrast & Brightness Adjustment
    contrast_enhancer = ImageEnhance.Contrast(image)
    image = contrast_enhancer.enhance(rng.uniform(0.92, 1.05))

    brightness_enhancer = ImageEnhance.Brightness(image)
    image = brightness_enhancer.enhance(rng.uniform(0.95, 1.02))

    # 5. JPEG Compression Artifacts
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=rng.randint(72, 85))
    buffer.seek(0)
    degraded_image = Image.open(buffer)

    # Save as PNG
    degraded_image.save(output_path, format="PNG")
    return output_path
