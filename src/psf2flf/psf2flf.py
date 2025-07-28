from pathlib import Path
from psf import PSFFont  # assumes you saved the previous code in psf.py


# 2x2 Unicode block rendering map
BLOCKS = {
    0b0000: " ",
    0b0001: "▗",
    0b0010: "▖",
    0b0011: "▄",
    0b0100: "▝",
    0b0101: "▐",
    0b0110: "▞",
    0b0111: "▟",
    0b1000: "▘",
    0b1001: "▚",
    0b1010: "▌",
    0b1011: "▙",
    0b1100: "▀",
    0b1101: "▜",
    0b1110: "▛",
    0b1111: "█",
}

# Characters to export
GLYPHS = [chr(i) for i in range(32, 127)]
DEFAULT_CHAR = ord("?")


def render_block_glyph(bitmap: bytes, width: int, height: int) -> list[str]:
    lines = []
    for y in range(0, height, 2):
        line = ""
        for x in range(0, width, 2):
            bits = 0
            for dy in range(2):
                for dx in range(2):
                    px, py = x + dx, y + dy
                    if px < width and py < len(bitmap):
                        if bitmap[py] & (1 << (7 - px)):
                            bits |= 1 << (dy * 2 + dx)
            line += BLOCKS.get(bits, "?")
        lines.append(line.rstrip())
    return lines


def convert_psf_to_flf(font: PSFFont, name: str, output_dir: Path):
    height = font.height
    width = font.width
    fig_height = (height + 1) // 2  # for 2x2 block rendering
    hardblank = "$"
    layout = 0  # Full layout
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}-{width}x{height}.flf"

    with path.open("w", encoding="utf-8") as f:
        f.write(f"flf2a{hardblank} {fig_height} {fig_height - 1} {width // 2} 0 {layout} 0 0 {len(GLYPHS)}\n")

        for ch in GLYPHS:
            code = ord(ch)
            glyph = font.glyphs[code] if code < len(font.glyphs) else font.glyphs[DEFAULT_CHAR]
            rendered = render_block_glyph(glyph, font.width, font.height)
            for line in rendered[:-1]:
                f.write(line + "\n")
            f.write(rendered[-1] + "@\n")  # FIGlet end of glyph marker

    return path


# Example usage:
# from psf import load_psf_file
# font = load_psf_file("/usr/share/consolefonts/Lat7-Terminus32x16.psf.gz")
# convert_psf_to_flf(font, "terminus", Path("fonts/console"))
