import json
from pathlib import Path

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "shot_chart_data.json"
OUT_DIR = ROOT / "assets" / "plots"

WIDTH = 900
HEIGHT = 760
MARGIN_X = 90
MARGIN_TOP = 90
COURT_W = WIDTH - (MARGIN_X * 2)
COURT_H = 560

MAKE_COLOR = (88, 200, 110)
MISS_COLOR = (78, 78, 232)
LINE_COLOR = (59, 83, 118)
FLOOR_COLOR = (241, 234, 220)
TEXT_DARK = (35, 41, 53)
TEXT_MID = (86, 93, 112)
TEXT_LIGHT = (233, 237, 245)
TEXT_SOFT = (194, 202, 217)


def load_data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def court_xy(x, y):
    px = int(MARGIN_X + (x / 50.0) * COURT_W)
    py = int(MARGIN_TOP + (y / 47.0) * COURT_H)
    return px, py


def draw_court(canvas):
    left = MARGIN_X
    top = MARGIN_TOP
    right = left + COURT_W
    bottom = top + COURT_H

    canvas[:] = (18, 24, 36)
    cv2.rectangle(canvas, (left, top), (right, bottom), FLOOR_COLOR, -1)
    cv2.rectangle(canvas, (left, top), (right, bottom), LINE_COLOR, 4)

    hoop_x, hoop_y = court_xy(25, 2.4)
    backboard_y = court_xy(25, 4.2)[1]
    rim_r = 11

    cv2.line(canvas, (hoop_x - 30, backboard_y), (hoop_x + 30, backboard_y), LINE_COLOR, 4)
    cv2.circle(canvas, (hoop_x, hoop_y), rim_r, LINE_COLOR, 4)

    lane_left, lane_top = court_xy(17, 0)
    lane_right, lane_bottom = court_xy(33, 19)
    cv2.rectangle(canvas, (lane_left, lane_top), (lane_right, lane_bottom), LINE_COLOR, 4)

    cv2.ellipse(
        canvas,
        (hoop_x, lane_bottom),
        (int(COURT_W * 0.095), int(COURT_H * 0.095)),
        0,
        180,
        360,
        LINE_COLOR,
        4,
    )

    free_throw_center = (hoop_x, lane_bottom)
    free_throw_r = int(COURT_W * 0.095)
    cv2.ellipse(canvas, free_throw_center, (free_throw_r, free_throw_r), 0, 0, 180, LINE_COLOR, 4)

    restricted_r = int(COURT_W * 0.06)
    cv2.ellipse(canvas, (hoop_x, hoop_y + 6), (restricted_r, restricted_r), 0, 0, 180, LINE_COLOR, 4)

    corner_y = court_xy(0, 41.8)[1]
    arc_radius = int(COURT_W * 0.31)
    cv2.line(canvas, (left, top), (left, corner_y), LINE_COLOR, 4)
    cv2.line(canvas, (right, top), (right, corner_y), LINE_COLOR, 4)
    cv2.ellipse(canvas, (hoop_x, hoop_y + 6), (arc_radius, arc_radius), 0, 22, 158, LINE_COLOR, 4)

    half_arc_center = court_xy(25, 47)
    half_arc_r = int(COURT_W * 0.12)
    cv2.ellipse(canvas, half_arc_center, (half_arc_r, half_arc_r), 0, 180, 360, LINE_COLOR, 4)


def draw_legend(canvas):
    legend_y = 690

    cv2.circle(canvas, (130, legend_y), 12, MAKE_COLOR, -1)
    cv2.circle(canvas, (130, legend_y), 12, (255, 255, 255), 2)
    cv2.putText(canvas, "made shot", (152, legend_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_LIGHT, 2, cv2.LINE_AA)

    cv2.circle(canvas, (325, legend_y), 12, MISS_COLOR, -1)
    cv2.circle(canvas, (325, legend_y), 12, (255, 255, 255), 2)
    cv2.putText(canvas, "missed shot", (347, legend_y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, TEXT_LIGHT, 2, cv2.LINE_AA)


def draw_shots(canvas, shots):
    for shot in shots:
        px, py = court_xy(shot["x"], shot["y"])
        color = MAKE_COLOR if shot["result"] == "make" else MISS_COLOR
        cv2.circle(canvas, (px, py), 16, color, -1)
        cv2.circle(canvas, (px, py), 16, (255, 255, 255), 2)


def render_player(player_key, player_data):
    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    draw_court(canvas)
    draw_shots(canvas, player_data["shots"])
    draw_legend(canvas)

    makes = sum(1 for shot in player_data["shots"] if shot["result"] == "make")
    misses = sum(1 for shot in player_data["shots"] if shot["result"] == "miss")

    cv2.putText(canvas, player_data["display_name"], (90, 48), cv2.FONT_HERSHEY_SIMPLEX, 1.25, (242, 244, 248), 3, cv2.LINE_AA)
    cv2.putText(canvas, player_data["sample_note"], (90, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.72, (255, 183, 149), 2, cv2.LINE_AA)
    cv2.putText(
        canvas,
        f"sample: {makes} makes / {misses} misses",
        (530, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.72,
        (224, 229, 239),
        2,
        cv2.LINE_AA,
    )
    cv2.putText(
        canvas,
        "Three-game visible sample. Use as a coaching map, not official stats.",
        (90, 728),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        TEXT_SOFT,
        1,
        cv2.LINE_AA,
    )

    out_path = OUT_DIR / f"{player_key}.png"
    cv2.imwrite(str(out_path), canvas)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    for player_key, player_data in data["players"].items():
        render_player(player_key, player_data)


if __name__ == "__main__":
    main()
