from typing import TYPE_CHECKING, TypedDict

from PIL import Image

if TYPE_CHECKING:
    from pathlib import Path

dpi = 600


class _DIM(TypedDict, total=False):
    left: float
    upper: float
    right: float
    lower: float


def crop(home: Path, raw_img: str, cropped_img: str, dim: _DIM) -> None:
    """Import image and export cropped image.

    Parameters
    ----------
    home : Path
        The path to the directory containing the image.
    raw_img : str
        The name of the raw image file to be cropped.
    cropped_img : str
        The name of the cropped image file to be saved.
    dim : TypedDict[...]
        A dictionary containing the cropping dimensions. The keys:
        - "left": The left coordinate of the cropping box (default is 0).
        - "upper": The upper coordinate of the cropping box (default is 0).
        - "right": The right coordinate of the cropping box (default is the width of the image).
        - "lower": The lower coordinate of the cropping box (default is the height of the image).

    """
    left = dim.get("left", 0)
    right = dim.get("right")
    upper = dim.get("upper", 0)
    lower = dim.get("lower")
    with Image.open(home / raw_img) as img:
        width, height = img.size
        right = width if (right is None) else right
        lower = height if (lower is None) else lower
        # print((left, upper, right, lower))
        cropped = img.crop(box=(left, upper, right, lower))
        cropped.save(home / cropped_img)
        cropped.close()
        print(cropped.size)
