#!/usr/bin/env python3
"""Capture Rumbo Deporte screens and build ~60s promo MP4 for LinkedIn."""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PROMO = ROOT / "promo"
FRAMES = PROMO / "frames"
APP_URL = os.environ.get("RUMBO_PROMO_URL", "http://127.0.0.1:8502/")
LOGIN_NAME = "Deporte SA"
LOGIN_PIN = "2356"
BACKUP_JSON = ROOT / "pei-clase-deporte-sa.json"
PORTADA = Path.home() / "Desktop" / "rumbo_linkedin_portada.png"
OUT_VIDEO = PROMO / "rumbo_deporte_60s.mp4"

W, H = 1920, 1080
BRAND_GREEN = "#044A30"
BG_MAIN = "#D5E9E2"

MODULE_LABELS = [
    "1 · Organización",
    "2 · Tu primer PEI",
    "3 · Análisis DAFO",
    "4 · Visión, misión y valores",
    "5 · Prioridades y objetivos",
    "6 · Plan de acción",
    "7 · Indicadores (KPI)",
    "8 · Recursos humanos y voluntarios",
    "9 · Primer proyecto (opcional)",
    "10 · Resumen y exportación",
    "11 · Actividades de ejecución",
    "12 · Tablero de monitoreo",
]

# seconds per segment (total ~60)
DURATIONS: dict[str, float] = {
    "00_intro": 4.0,
    "01_panel_sidebar": 4.5,
}
for i, label in enumerate(MODULE_LABELS, start=2):
    key = f"{i:02d}_{label.split('·', 1)[-1].strip().lower().replace(' ', '_')[:28]}"
    DURATIONS[key] = 4.0 if i < 12 else 5.0
DURATIONS["99_cta"] = 4.5


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for path in candidates:
        p = Path(path)
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def make_intro_frame(path: Path) -> None:
    img = Image.new("RGB", (W, H), BRAND_GREEN)
    draw = ImageDraw.Draw(img)
    if PORTADA.exists():
        logo = Image.open(PORTADA).convert("RGBA")
        lw = min(900, int(W * 0.55))
        lh = int(lw * logo.height / logo.width)
        logo = logo.resize((lw, lh), Image.Resampling.LANCZOS)
        img.paste(logo, ((W - lw) // 2, int(H * 0.12)), logo)
        y_title = int(H * 0.12) + lh + 40
    else:
        y_title = int(H * 0.35)
    f1 = _font(96, bold=True)
    f2 = _font(42)
    title = "RUMBO DEPORTE"
    tw = draw.textlength(title, font=f1)
    draw.text(((W - tw) / 2, y_title), title, fill="white", font=f1)
    sub = "Plan estratégico · actividades · tablero de monitoreo"
    sw = draw.textlength(sub, font=f2)
    draw.text(((W - sw) / 2, y_title + 110), sub, fill="#E8F5EF", font=f2)
    img.save(path, "PNG")


def make_cta_frame(path: Path) -> None:
    img = Image.new("RGB", (W, H), BRAND_GREEN)
    draw = ImageDraw.Draw(img)
    f1 = _font(72, bold=True)
    f2 = _font(36)
    lines = [
        "RUMBO DEPORTE",
        "",
        "Para clubes, federaciones y asociaciones",
        "Observatorio de Inteligencia Artificial · UCCuyo",
    ]
    y = H * 0.28
    for i, line in enumerate(lines):
        if not line:
            y += 20
            continue
        font = f1 if i == 0 else f2
        fill = "white" if i == 0 else "#E8F5EF"
        tw = draw.textlength(line, font=font)
        draw.text(((W - tw) / 2, y), line, fill=fill, font=font)
        y += 90 if i == 0 else 52
    img.save(path, "PNG")


def add_caption_bar(src: Path, caption: str, dest: Path) -> None:
    base = Image.open(src).convert("RGB")
    bw, bh = base.size
    scale = min(W / bw, H / bh)
    nw, nh = int(bw * scale), int(bh * scale)
    base = base.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (W, H), BG_MAIN)
    canvas.paste(base, ((W - nw) // 2, (H - nh) // 2))
    draw = ImageDraw.Draw(canvas)
    bar_h = 72
    draw.rectangle([0, H - bar_h, W, H], fill=BRAND_GREEN)
    font = _font(32, bold=True)
    tw = draw.textlength(caption, font=font)
    draw.text(((W - tw) / 2, H - bar_h + 18), caption, fill="white", font=font)
    canvas.save(dest, "PNG")


def wait_app(page, extra_ms: int = 0) -> None:
    page.wait_for_timeout(1200 + extra_ms)
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass
    page.wait_for_timeout(800)


def login_and_open_plan(page) -> None:
    page.goto(APP_URL, wait_until="domcontentloaded", timeout=120000)
    wait_app(page, 3000)

    acceso = page.locator('button:has-text("Acceso organizaciones")')
    if acceso.count() and acceso.first.is_visible():
        acceso.first.click()
        wait_app(page)

    name_input = page.locator('input[type="text"]').first
    name_input.wait_for(state="visible", timeout=90000)
    name_input.fill(LOGIN_NAME)
    page.locator('input[type="password"]').first.fill(LOGIN_PIN)
    page.locator('button:has-text("Ingresar")').first.click()
    wait_app(page, 1500)

    if page.get_by_role("button", name="Editar").count() == 0:
        if BACKUP_JSON.exists() and page.locator('input[type="file"]').count():
            page.locator('input[type="file"]').set_input_files(str(BACKUP_JSON))
            wait_app(page, 500)
            imp = page.get_by_role("button", name="Importar PEI")
            if imp.is_visible():
                imp.click()
                wait_app(page, 2500)

    edit = page.get_by_role("button", name="Editar").first
    if not edit.is_visible():
        plan_row = page.locator('summary:has-text("Deporte SA")').first
        if plan_row.count() == 0:
            plan_row = page.locator('button:has-text("Deporte SA")').first
        plan_row.click()
        wait_app(page, 1000)
    edit.wait_for(state="visible", timeout=60000)
    edit.click()
    wait_app(page, 2000)


def capture_screens(page) -> list[tuple[str, str, Path]]:
    """Return list of (frame_key, caption, raw_shot_path)."""
    FRAMES.mkdir(parents=True, exist_ok=True)
    shots: list[tuple[str, str, Path]] = []

    # Sidebar + first module visible
    page.locator(f'label:has-text("{MODULE_LABELS[0]}")').first.click()
    wait_app(page, 1000)
    panel_path = FRAMES / "raw_panel.png"
    page.screenshot(path=str(panel_path), full_page=False)
    shots.append(("01_panel_sidebar", "Navegación y avance por módulo", panel_path))

    for label in MODULE_LABELS:
        page.locator(f'label:has-text("{label}")').first.click()
        wait_app(page, 1200 if "Tablero" in label else 800)
        safe = (
            label.split("·", 1)[-1]
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
        )[:40]
        raw = FRAMES / f"raw_{safe}.png"
        page.screenshot(path=str(raw), full_page=True)
        idx = MODULE_LABELS.index(label) + 2
        key = f"{idx:02d}_{safe}"
        shots.append((key, label, raw))
    return shots


def build_concat_list(frame_paths: list[tuple[str, float]]) -> Path:
    concat = PROMO / "concat.txt"
    lines: list[str] = []
    for path, dur in frame_paths:
        esc = str(path).replace("'", "'\\''")
        lines.append(f"file '{esc}'")
        lines.append(f"duration {dur}")
    if frame_paths:
        last = frame_paths[-1][0]
        esc = str(last).replace("'", "'\\''")
        lines.append(f"file '{esc}'")
    concat.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return concat


def encode_video(concat: Path, out: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat),
        "-vf",
        "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=0xD5E9E2",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        "-movflags",
        "+faststart",
        str(out),
    ]
    subprocess.run(cmd, check=True)


def main() -> int:
    FRAMES.mkdir(parents=True, exist_ok=True)
    intro = FRAMES / "00_intro.png"
    cta = FRAMES / "99_cta.png"
    make_intro_frame(intro)
    make_cta_frame(cta)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1600, "height": 1000},
            device_scale_factor=2,
        )
        page = context.new_page()
        try:
            login_and_open_plan(page)
            shots = capture_screens(page)
        finally:
            browser.close()

    timeline: list[tuple[Path, float]] = [(intro, DURATIONS["00_intro"])]

    for key, caption, raw in shots:
        if key == "01_panel_sidebar":
            out = FRAMES / f"{key}.png"
            add_caption_bar(raw, caption, out)
            timeline.append((out, DURATIONS.get(key, 4.5)))
            continue
        out = FRAMES / f"{key}.png"
        add_caption_bar(raw, caption, out)
        timeline.append((out, DURATIONS.get(key, 4.0)))

    timeline.append((cta, DURATIONS["99_cta"]))

    total = sum(d for _, d in timeline)
    print(f"Segments: {len(timeline)}, total duration ~{total:.1f}s")

    concat = build_concat_list(timeline)
    encode_video(concat, OUT_VIDEO)
    print(f"Video: {OUT_VIDEO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
