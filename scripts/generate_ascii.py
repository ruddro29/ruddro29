from PIL import Image, ImageOps, ImageEnhance, ImageFilter
from pathlib import Path
import html


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_IMAGE = Path("assets/profile.jpg")
OUTPUT_FILE = Path("assets/new_ascii.svg")

# Higher = more detailed portrait
ASCII_WIDTH = 110

# Characters from DARK → BRIGHT
CHARACTERS = "@%#*+=-:. "

# GitHub blue
COLOR = "#58a6ff"

# Portrait contrast
CONTRAST = 2.0

# Brightness adjustment
BRIGHTNESS = 1.05

# How aggressively we remove the background
BACKGROUND_THRESHOLD = 205

# Animation
LINE_DURATION = 0.045
LINE_DELAY = 0.018


# ============================================================
# LOAD IMAGE
# ============================================================

image = Image.open(INPUT_IMAGE).convert("RGB")


# ============================================================
# CROP
# ============================================================

width, height = image.size

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
# AUTO CONTRAST
# ============================================================

image = ImageOps.autocontrast(
    image,
    cutoff=2
)


# ============================================================
# CONTRAST
# ============================================================

image = ImageEnhance.Contrast(
    image
).enhance(CONTRAST)


# ============================================================
# BRIGHTNESS
# ============================================================

image = ImageEnhance.Brightness(
    image
).enhance(BRIGHTNESS)


# ============================================================
# SLIGHT SHARPEN
# ============================================================

image = image.filter(
    ImageFilter.SHARPEN
)


# ============================================================
# RESIZE
# ============================================================

aspect_ratio = image.height / image.width

ASCII_HEIGHT = int(
    ASCII_WIDTH
    * aspect_ratio
    * 0.50
)

image = image.resize(
    (
        ASCII_WIDTH,
        ASCII_HEIGHT
    ),
    Image.Resampling.LANCZOS
)


# ============================================================
# BACKGROUND SUPPRESSION
# ============================================================

pixels = image.load()

for y in range(image.height):

    for x in range(image.width):

        value = pixels[x, y]

        # Very bright areas become empty space.
        if value >= BACKGROUND_THRESHOLD:

            pixels[x, y] = 255


# ============================================================
# PIXELS → ASCII
# ============================================================

pixels = image.load()

ascii_lines = []

for y in range(image.height):

    line = ""

    for x in range(image.width):

        value = pixels[x, y]

        index = int(
            value
            / 255
            * (len(CHARACTERS) - 1)
        )

        index = max(
            0,
            min(
                index,
                len(CHARACTERS) - 1
            )
        )

        line += CHARACTERS[index]

    # Remove useless trailing whitespace
    line = line.rstrip()

    ascii_lines.append(line)


# ============================================================
# REMOVE EMPTY LINES
# ============================================================

ascii_lines = [
    line
    for line in ascii_lines
    if line.strip()
]


# ============================================================
# SVG SETTINGS
# ============================================================

FONT_SIZE = 9
LINE_HEIGHT = 10

SVG_WIDTH = 1100

SVG_HEIGHT = (
    len(ascii_lines)
    * LINE_HEIGHT
    + 80
)


# ============================================================
# SVG HEADER
# ============================================================

svg = f"""<svg
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
    font-family: monospace;
    font-size: {FONT_SIZE}px;
    font-weight: 400;
    fill: {COLOR};
}}

.cursor {{
    fill: {COLOR};
}}

</style>
"""


# ============================================================
# GENERATE ANIMATED ASCII
# ============================================================

for i, line in enumerate(ascii_lines):

    y = 30 + i * LINE_HEIGHT

    safe_line = html.escape(line)

    start_time = (
        i * LINE_DELAY
    )

    line_width = max(
        len(line)
        * FONT_SIZE
        * 0.60,
        10
    )

    svg += f"""

<clipPath id="clip{i}">

    <rect
        x="20"
        y="{y - FONT_SIZE}"
        width="0"
        height="{LINE_HEIGHT}">

        <animate
            attributeName="width"
            from="0"
            to="{line_width}"
            dur="{LINE_DURATION}s"
            begin="{start_time}s"
            fill="freeze"/>

    </rect>

</clipPath>

<text
x="20"
y="{y}"
class="ascii"
clip-path="url(#clip{i})">

{safe_line}

</text>
"""


# ============================================================
# CURSOR
# ============================================================

total_animation_time = (
    len(ascii_lines) * LINE_DELAY
    + LINE_DURATION
)


svg += """

<rect
x="20"
y="20"
width="6"
height="10"
class="cursor">

<animate
attributeName="y"
values="
"""


for i in range(len(ascii_lines)):

    y = 30 + i * LINE_HEIGHT

    svg += f"{y - FONT_SIZE};"


svg += f"""
"
dur="{total_animation_time}s"
fill="freeze"/>

<animate
attributeName="opacity"
values="1;0;1"
dur="0.6s"
repeatCount="indefinite"/>

</rect>

</svg>
"""


# ============================================================
# WRITE SVG
# ============================================================

OUTPUT_FILE.write_text(
    svg,
    encoding="utf-8"
)

print(
    f"Generated {OUTPUT_FILE}"
)
