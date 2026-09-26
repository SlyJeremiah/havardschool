from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps

MAX_SIDE = 1600


def optimise_image(field, max_side=MAX_SIDE, quality=82):
    """Shrink a freshly uploaded ImageField file in place (saves B2 storage & bandwidth).

    Only acts on new, uncommitted uploads; returns silently on any problem.
    """
    if not field or getattr(field, "_committed", True):
        return
    f = field.file
    try:
        img = Image.open(f)
        img = ImageOps.exif_transpose(img)
        if max(img.size) <= max_side and img.format in ("JPEG", "WEBP"):
            f.seek(0)
            return
        img.thumbnail((max_side, max_side))
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        name = Path(field.name).stem + ".jpg"
        field.save(name, ContentFile(buf.getvalue()), save=False)
    except Exception:
        try:
            f.seek(0)
        except Exception:
            pass
