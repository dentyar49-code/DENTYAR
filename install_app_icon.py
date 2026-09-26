#!/usr/bin/env python3
"""
Installs the real DENTYAR launcher icon into the freshly-generated
android/ project (created by `npx cap add android`), replacing
Capacitor's default placeholder icon.

Why this exists: without this step, Capacitor's default launcher icon
(dark/black square) ships in the APK instead of the DENTYAR logo, because
this project has no `resources/` folder for `@capacitor/assets` to use.

Run this AFTER `npx cap add android` / `npx cap sync android` and
BEFORE the Gradle build step.
"""
from pathlib import Path
import sys

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required (pip install Pillow)", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "android" / "app" / "src" / "main" / "res"
ANY_SRC = ROOT / "www" / "icon-512.png"
MASK_SRC = ROOT / "www" / "icon-512-maskable.png"

# Standard Android launcher icon sizes per density bucket.
DENSITIES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

ADAPTIVE_ICON_XML = (
    '<?xml version="1.0" encoding="utf-8"?>\n'
    '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
    '    <background android:drawable="@color/ic_launcher_background"/>\n'
    '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
    "</adaptive-icon>\n"
)

BRAND_TEAL = "#0f766e"


def main():
    if not ANY_SRC.exists() or not MASK_SRC.exists():
        print(f"ERROR: expected icon files not found:\n  {ANY_SRC}\n  {MASK_SRC}", file=sys.stderr)
        sys.exit(1)
    if not RES.exists():
        print(f"ERROR: Android res folder not found at {RES} "
              "(did you run 'npx cap add android' first?)", file=sys.stderr)
        sys.exit(1)

    any_img = Image.open(ANY_SRC).convert("RGBA")
    mask_img = Image.open(MASK_SRC).convert("RGBA")

    for folder, size in DENSITIES.items():
        d = RES / folder
        d.mkdir(parents=True, exist_ok=True)

        any_img.resize((size, size), Image.LANCZOS).save(d / "ic_launcher.png")
        any_img.resize((size, size), Image.LANCZOS).save(d / "ic_launcher_round.png")

        # Adaptive icon foreground canvas is larger than the legacy icon (108/72 ratio)
        fg_size = int(size * 108 / 72)
        mask_img.resize((fg_size, fg_size), Image.LANCZOS).save(d / "ic_launcher_foreground.png")

    anydpi = RES / "mipmap-anydpi-v26"
    anydpi.mkdir(parents=True, exist_ok=True)
    (anydpi / "ic_launcher.xml").write_text(ADAPTIVE_ICON_XML, encoding="utf-8")
    (anydpi / "ic_launcher_round.xml").write_text(ADAPTIVE_ICON_XML, encoding="utf-8")

    values = RES / "values"
    values.mkdir(parents=True, exist_ok=True)
    colors_path = values / "colors.xml"
    color_line = f'<color name="ic_launcher_background">{BRAND_TEAL}</color>'

    if colors_path.exists():
        content = colors_path.read_text(encoding="utf-8")
        if "ic_launcher_background" not in content:
            content = content.replace("</resources>", f"    {color_line}\n</resources>")
            colors_path.write_text(content, encoding="utf-8")
    else:
        colors_path.write_text(
            f'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    {color_line}\n</resources>\n',
            encoding="utf-8",
        )

    print("DENTYAR launcher icons installed for all densities.")


if __name__ == "__main__":
    main()
