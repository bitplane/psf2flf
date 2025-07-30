from pathlib import Path

from ..font import Font

GLYPHS = [chr(i) for i in range(32, 127)]
DEFAULT_CHAR = "?"


class FLFWriter:
    def __init__(self, font: Font, tall_mode: bool = False):
        self.font = font
        self.tall_mode = tall_mode

    def write(self, output_path: Path):
        height = self.font.meta["height"]
        width = self.font.meta["width"]
        fig_height, max_length, _ = self._calculate_flf_dimensions(width, height, self.tall_mode)

        hardblank = "$"
        layout = 0

        with output_path.open("w", encoding="utf-8") as f:
            f.write(f"flf2a{hardblank} {fig_height} {fig_height - 1} {max_length} 0 {layout} 0 0 {len(GLYPHS)}\n")
            for ch in GLYPHS:
                glyph = self.font.glyphs.get(ch, self.font.glyphs[DEFAULT_CHAR])
                rendered = self._render_block_glyph(glyph, width, height, self.tall_mode)

                while len(rendered) < fig_height:
                    rendered.append("")

                for i, line in enumerate(rendered):
                    padded_line = line.replace(" ", hardblank).ljust(max_length, hardblank)
                    terminator = "@" if i < len(rendered) - 1 else "@@"
                    f.write(padded_line + terminator + "\n")

    def _calculate_flf_dimensions(self, font_width: int, font_height: int, tall_mode: bool):
        if tall_mode:
            fig_height = font_height
            max_length = font_width
            display_width = font_width
        else:
            fig_height = (font_height + 1) // 2
            max_length = font_width
            display_width = font_width

        return fig_height, max_length, display_width

    def _render_block_glyph(self, pixel_array: list[list[bool]], width: int, height: int, tall_mode: bool) -> list[str]:
        if tall_mode:
            return self._render_full_pixels(pixel_array, width, height)
        else:
            return self._render_short_blocks(pixel_array, width, height)

    def _render_short_blocks(self, pixel_array: list[list[bool]], width: int, height: int) -> list[str]:
        lines = []
        for y in range(0, height, 2):
            line = ""
            for x in range(width):
                top_pixel = pixel_array[y][x] if y < height and x < width else False
                bottom_pixel = pixel_array[y + 1][x] if y + 1 < height and x < width else False

                if top_pixel and bottom_pixel:
                    line += "█"
                elif top_pixel:
                    line += "▀"
                elif bottom_pixel:
                    line += "▄"
                else:
                    line += " "
            lines.append(line)
        return lines

    def _render_full_pixels(self, pixel_array: list[list[bool]], width: int, height: int) -> list[str]:
        lines = []
        for y in range(height):
            line = ""
            for x in range(width):
                if pixel_array[y][x]:
                    line += "█"
                else:
                    line += " "
            lines.append(line)
        return lines
