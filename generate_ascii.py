import math
from PIL import Image

def avatar_to_ascii(image_path, width=44):
    img = Image.open(image_path).convert('L')
    
    # Character aspect ratio correction
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)
    
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    bg_val = img.getpixel((0, 0)) # ~139
    
    # We want dark pixels (hair, clothes, eyes) to be prominent (#, %, @),
    # skin pixels to be medium (., :, -, =),
    # and background pixels (near bg_val) to be empty spaces (" ")!
    
    lines = []
    for y in range(height):
        line_chars = []
        for x in range(width):
            val = img.getpixel((x, y))
            
            # Distance from background color
            if abs(val - bg_val) < 18:
                line_chars.append(" ")
            elif val < bg_val - 18:
                # Darker than background (hair, dark features, clothes)
                # Map lower values to denser characters
                d_val = bg_val - val
                if d_val > 90:
                    line_chars.append("@")
                elif d_val > 70:
                    line_chars.append("%")
                elif d_val > 50:
                    line_chars.append("#")
                elif d_val > 30:
                    line_chars.append("*")
                else:
                    line_chars.append("+")
            else:
                # Brighter than background (skin/highlights)
                b_val = val - bg_val
                if b_val > 60:
                    line_chars.append("=")
                elif b_val > 40:
                    line_chars.append("-")
                elif b_val > 20:
                    line_chars.append(":")
                else:
                    line_chars.append(".")
        lines.append("".join(line_chars))
        
    return lines

lines = avatar_to_ascii("avatar.png", width=44)

classes = ["p1", "p2", "p3", "p4", "p5", "p6", "p7"]
output_svg_block = []

for idx, line in enumerate(lines):
    # keep lines even if spaces to maintain spacing
    c_class = classes[min(idx // (len(lines) // 6 + 1), len(classes) - 1)]
    safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    output_svg_block.append(f'      <tspan x="610" dy="6" class="{c_class}">{safe_line}</tspan>')

result = "\n".join(output_svg_block)

with open("ascii_output.txt", "w", encoding="utf-8") as f:
    f.write(result)

print(f"Generated {len(output_svg_block)} lines of ASCII art from avatar.png.")
