from pathlib import Path

from PIL import Image

dpi = 600


def crop(
    home: Path,
    raw_img: str,
    cropped_img: str,
    right: float | None = None,
    lower: float | None = None,
    left: float = 0,
    upper: float = 0,
) -> None:
    with Image.open(home / raw_img) as img:
        width, height = img.size
        right = width if (right is None) else right
        lower = height if (lower is None) else lower
        # print((left, upper, right, lower))
        cropped = img.crop(box=(left, upper, right, lower))
        cropped.save(home / cropped_img)
        cropped.close()
        print(cropped.size)

