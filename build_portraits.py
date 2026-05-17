from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "assets" / "portraits"

BG = (36, 42, 62)
BG_TOP = (24, 27, 38)
PANEL = (17, 20, 30)
LINE = (96, 104, 138)
ACCENT = (77, 124, 255)
TEXT = (241, 244, 249)
TEXT_MID = (184, 192, 214)
TEXT_ACCENT = (255, 124, 77)


PLAYERS = {
    "josh": {
        "name": "COLIN",
        "role": "LEAD GUARD",
        "jersey": "#4",
        "lines": [
            "Confirmed jersey: #4",
            "Primary point-of-attack creator",
            "User jersey map updated 2026-05-17",
        ],
    },
    "chad": {
        "name": "JOSH",
        "role": "SCORER / FINISHER",
        "jersey": "#1",
        "lines": [
            "Confirmed jersey: #1",
            "Off-ball scorer sample",
            "User jersey map updated 2026-05-17",
        ],
    },
    "elijah": {
        "name": "ELIJAH",
        "role": "INTERIOR FINISHER",
        "jersey": "#13",
        "lines": [
            "Confirmed jersey: #13",
            "Black jersey big / glass pressure",
            "User jersey map updated 2026-05-17",
        ],
    },
    "yeyo": {
        "name": "YEYO",
        "role": "SCREEN / REBOUND BIG",
        "jersey": "#77",
        "lines": [
            "Confirmed jersey: #77",
            "Big body screener sample",
            "User jersey map updated 2026-05-17",
        ],
    },
    "vince": {
        "name": "VINCE",
        "role": "VETERAN ORGANIZER",
        "jersey": "#14",
        "lines": [
            "Confirmed jersey: #14",
            "Veteran connector sample",
            "User jersey map updated 2026-05-17",
        ],
    },
    "ryan": {
        "name": "RYAN",
        "role": "PRESSURE PIECE",
        "jersey": "#40",
        "lines": [
            "Confirmed jersey: #40",
            "old-Ryan tracked as #7",
            "User jersey map updated 2026-05-17",
        ],
    },
}


def make_card(data):
    img = np.zeros((900, 900, 3), dtype=np.uint8)
    img[:] = BG
    cv2.rectangle(img, (0, 0), (900, 320), BG_TOP, -1)
    poly = np.array([[0, 620], [900, 320], [900, 900], [0, 900]], dtype=np.int32)
    cv2.fillPoly(img, [poly], (40, 46, 69))

    cv2.ellipse(img, (690, 250), (160, 170), 0, 0, 360, (246, 246, 246), 14)
    cv2.putText(img, data["jersey"], (610, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.65, (236, 239, 247), 5, cv2.LINE_AA)

    cv2.putText(img, data["name"], (82, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.7, TEXT, 4, cv2.LINE_AA)
    cv2.putText(img, data["role"], (85, 205), cv2.FONT_HERSHEY_SIMPLEX, 0.92, TEXT_ACCENT, 3, cv2.LINE_AA)

    cv2.rectangle(img, (80, 266), (820, 538), PANEL, -1)
    cv2.rectangle(img, (80, 266), (820, 538), LINE, 3)
    cv2.putText(img, "REFERENCE NOTES", (112, 328), cv2.FONT_HERSHEY_SIMPLEX, 1.1, TEXT, 3, cv2.LINE_AA)

    y = 384
    for line in data["lines"]:
        cv2.putText(img, f"- {line}", (120, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, TEXT_MID, 2, cv2.LINE_AA)
        y += 54

    cv2.rectangle(img, (80, 622), (820, 792), (255, 124, 77), -1)
    cv2.putText(img, "SCOUT BUILD", (110, 684), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (22, 22, 22), 3, cv2.LINE_AA)
    cv2.putText(img, "Built from video samples + user jersey map", (110, 738), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (22, 22, 22), 2, cv2.LINE_AA)

    return img


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for key, data in PLAYERS.items():
        out_path = OUT_DIR / f"{key}.png"
        cv2.imwrite(str(out_path), make_card(data))


if __name__ == "__main__":
    main()
