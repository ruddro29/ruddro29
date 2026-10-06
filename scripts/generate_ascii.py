from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import html


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_IMAGE = Path("assets/profile.jpg")
OUTPUT_FILE = Path("assets/new_ascii.svg")

ASCII_WIDTH = 90

# Dark → bright
CHARACTERS = "@%#*+=-:. "


# ==========================================
# LOAD IMAGE
# ==========================================

image = Image.open(INPUT_IMAGE).convert("RGB")


# ==========================================
# CROP IMAGE
# ==========================================

# Make the image square around the center.
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


# ==========================================
# GRAYSCALE
# ==========================================

image = ImageOps.grayscale(image)


# ==========================================
# CONTRAST
# ==========================================

contrast = ImageEnhance.Contrast(image)

image = contrast.enhance(1.5)


# ==========================================
# BRIGHTNESS
# ==========================================

brightness = ImageEnhance.Brightness(image)

image = brightness.enhance(1.05)


# ==========================================
# RESIZE
# ==========================================

aspect_ratio = image.height / image.width

ASCII_HEIGHT = int(
    ASCII_WIDTH
    * aspect_ratio
    * 0.5
)

image = image.resize(
    (
        ASCII_WIDTH,
        ASCII_HEIGHT
    )
)


# ==========================================
# PIXELS → ASCII
# ==========================================

pixels = image.load()

ascii_lines = []


for y in range(image.height):

    line = ""

    for x in range(image.width):

        brightness = pixels[x, y]

        index = int(
            brightness
            / 255
            * (len(CHARACTERS) - 1)
        )

        line += CHARACTERS[index]

    ascii_lines.append(line.rstrip())


# ==========================================
# SVG CONFIG
# ==========================================

FONT_SIZE = 10
LINE_HEIGHT = 12

SVG_WIDTH = 1000

SVG_HEIGHT = (
    len(ascii_lines)
    * LINE_HEIGHT
    + 60
)


# ==========================================
# SVG HEADER
# ==========================================

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
    fill: #58a6ff;
}}

</style>

<text
class="ascii"
x="20"
y="30">
"""


# ==========================================
# ADD ASCII LINES
# ==========================================

for i, line in enumerate(ascii_lines):

    y = 30 + i * LINE_HEIGHT

    safe_line = html.escape(line)

    svg += f"""
<tspan
x="20"
y="{y}">
{safe_line}
</tspan>
"""


# ==========================================
# CLOSE SVG
# ==========================================

svg += """

</text>

</svg>
"""


# ==========================================
# WRITE FILE
# ==========================================

OUTPUT_FILE.write_text(
    svg,
    encoding="utf-8"
)

print(
    f"Generated {OUTPUT_FILE}"
)
