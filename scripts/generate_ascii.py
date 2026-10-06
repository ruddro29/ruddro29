from PIL import Image, ImageOps, ImageEnhance
from pathlib import Path
import html


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_IMAGE = Path("assets/profile.jpg")
OUTPUT_FILE = Path("assets/ascii.svg")

ASCII_WIDTH = 100

# Dark → bright
CHARACTERS = "@#8&o:*. "


# ==========================================
# LOAD IMAGE
# ==========================================

image = Image.open(INPUT_IMAGE).convert("RGB")


# ==========================================
# RESIZE IMAGE
# ==========================================

original_width, original_height = image.size

aspect_ratio = original_height / original_width

# Terminal characters are taller than they are wide.
CHARACTER_ASPECT = 0.45

ascii_height = int(
    ASCII_WIDTH
    * aspect_ratio
    * CHARACTER_ASPECT
)

image = image.resize(
    (
        ASCII_WIDTH,
        ascii_height
    )
)


# ==========================================
# GRAYSCALE
# ==========================================

image = ImageOps.grayscale(image)


# ==========================================
# AUTOCONTRAST
# ==========================================

image = ImageOps.autocontrast(
    image,
    cutoff=2
)


# ==========================================
# CONTRAST
# ==========================================

contrast = ImageEnhance.Contrast(image)

image = contrast.enhance(1.8)


# ==========================================
# SHARPEN
# ==========================================

image = ImageEnhance.Sharpness(
    image
).enhance(1.4)


# ==========================================
# ASCII CONVERSION
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

    ascii_lines.append(
        line.rstrip()
    )


# ==========================================
# SVG CONFIGURATION
# ==========================================

FONT_SIZE = 10
LINE_HEIGHT = 12

SVG_WIDTH = 1100

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
# ADD ASCII
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
