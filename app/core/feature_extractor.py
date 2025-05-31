import cv2
import numpy as np
from typing import Tuple


def compute_color_histogram(image_path: str, bins: Tuple[int, int, int] = (8, 8, 8)) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
    cv2.normalize(hist, hist)

    return hist.flatten()
