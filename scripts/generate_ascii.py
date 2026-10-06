from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path
import html


# ============================================================
# CONFIG
# ============================================================

INPUT_IMAGE = Path("assets/profile.jpg")
OUTPUT_FILE = Path("assets/new_ascii.svg")

# More characters = more facial detail
ASCII_WIDTH = 140

# Dark -> bright
CHARACTERS = "@#8&o:*. "


# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(INPUT_IMAGE).convert("RGB")


# ============================================================
# CROP IMAGE
# ============================================================

width, height = image.size

# Keep a square-ish portrait area.
side = min(width, height)

left = (width - side) // 2
top = (height - side) // 2

image = image.crop(
    (
        left,
        top,
        left + side,
        top + side
    )
)


# ============================================================
# GRAYSCALE
# ============================================================

image = ImageOps.grayscale(image)


# ============================================================
# IMPROVE CONTRAST
# ============================================================

image = ImageEnhance.Contrast(image).enhance(1.8)

image = ImageEnhance.Sharpness(image).enhance(2.0)


# ============================================================
# RESIZE
# ============================================================

aspect_ratio = image.height / image.width

ASCII_HEIGHT = int(
    ASCII_WIDTH *
    aspect_ratio *
    0.50
)

image = image.resize(
    (ASCII_WIDTH, ASCII_HEIGHT),
    Image.Resampling.LANCZOS
)


# ============================================================
# SLIGHT SHARPENING
# ============================================================

image = image.filter(
    ImageFilter.UnsharpMask(
        radius=1,
        percent=150,
        threshold=3
    )
)


# ============================================================
# CONVERT PIXELS TO ASCII
# ============================================================

pixels = image.load()

lines = []

for y in range(image.height):

    line = ""

    for x in range(image.width):

        brightness = pixels[x, y]

        # Invert brightness:
        # dark pixels → dense characters
        # bright pixels → spaces

        index = int(
            brightness / 255 *
            (len(CHARACTERS) - 1)
        )

        line += CHARACTERS[index]

    lines.append(line.rstrip())


# ============================================================
# SVG SETTINGS
# ============================================================

CHAR_WIDTH = 5.2
CHAR_HEIGHT = 8

PADDING_X = 20
PADDING_Y = 30

SVG_WIDTH = int(
    PADDING_X * 2 +
    ASCII_WIDTH * CHAR_WIDTH
)

SVG_HEIGHT = int(
    PADDING_Y * 2 +
    len(lines) * CHAR_HEIGHT
)


# ============================================================
# BUILD SVG
# ============================================================

svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{SVG_WIDTH}"
height="{SVG_HEIGHT}"
viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">

<rect
width="100%"
height="100%"
fill="#0d1117"/>

<style>

.ascii {{
    font-family:
        "Courier New",
        "Liberation Mono",
        monospace;

    font-size: 7px;

    fill: #58a6ff;

    letter-spacing: 0px;
}}

</style>

<text
class="ascii"
x="{PADDING_X}"
y="{PADDING_Y}">
'''


# ============================================================
# ADD ANIMATED ROWS
# ============================================================

for i, line in enumerate(lines):

    y = i * CHAR_HEIGHT

    safe_line = html.escape(line)

    delay = i * 0.025

    duration = 0.45

    svg += f'''
<tspan
x="{PADDING_X}"
dy="{0 if i == 0 else CHAR_HEIGHT}">

    <tspan>

        {safe_line}

    </tspan>

</tspan>
'''


# ============================================================
# CLOSE SVG
# ============================================================

svg += '''
</text>

</svg>
'''


# ============================================================
# WRITE FILE
# ============================================================

OUTPUT_FILE.write_text(
    svg,
    encoding="utf-8"
)

print(
    f"Generated {OUTPUT_FILE}"
)
