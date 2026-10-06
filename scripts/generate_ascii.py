from PIL import Image, ImageOps
from pathlib import Path


# ==========================================
# CONFIGURATION
# ==========================================

INPUT_IMAGE = Path("assets/profile.jpg")
OUTPUT_FILE = Path("assets/new_ascii.svg")

WIDTH = 80

# Characters ordered from dark → bright
CHARACTERS = "@%#*+=-:. "


# ==========================================
# LOAD IMAGE
# ==========================================

image = Image.open(INPUT_IMAGE)

# Convert to grayscale
image = ImageOps.grayscale(image)


# ==========================================
# RESIZE IMAGE
# ==========================================

aspect_ratio = image.height / image.width

height = int(WIDTH * aspect_ratio * 0.5)

image = image.resize((WIDTH, height))


# ==========================================
# CONVERT PIXELS → ASCII
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

    ascii_lines.append(line)


# ==========================================
# GENERATE SVG
# ==========================================

line_height = 14

svg_height = len(ascii_lines) * line_height + 40

svg = f"""<svg
xmlns="http://www.w3.org/2000/svg"
width="900"
height="{svg_height}"
viewBox="0 0 900 {svg_height}">

<rect
width="900"
height="{svg_height}"
fill="#0d1117"/>

<style>

.ascii {{
    font-family: monospace;
    font-size: 12px;
    fill: #58a6ff;
}}

</style>

<text
x="20"
y="20"
class="ascii">
"""


# ==========================================
# ADD ASCII LINES
# ==========================================

for i, line in enumerate(ascii_lines):

    y = 20 + i * line_height

    # Escape XML-sensitive characters
    line = (
        line
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    svg += f"""
<tspan
x="20"
y="{y}">
{line}
</tspan>
"""


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
