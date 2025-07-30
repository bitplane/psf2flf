import gzip
import struct
from pathlib import Path

from ..font import Font


class PSFParseError(Exception):
    pass


class PSFLoader:
    def __init__(self, path: Path):
        self.path = path
        with gzip.open(path, "rb") if str(path).endswith(".gz") else open(path, "rb") as f:
            self.data = f.read()

    def load(self) -> Font:
        font = Font()
        font.meta["file_name"] = str(self.path)

        if self.data[0:2] == b"\x36\x04":
            self._parse_psf1(font)
        elif self.data[0:4] == b"\x72\xb5\x4a\x86":
            self._parse_psf2(font)
        else:
            raise PSFParseError("Not a PSF file")

        return font

    def _parse_psf1(self, font: Font):
        font.meta["format"] = "psf1"
        mode = self.data[2]
        height = self.data[3]

        if mode > 0x111:
            raise PSFParseError("Unknown mode")

        glyphs = 512 if mode & 0b001 else 256
        width = 8
        char_size = height
        bytes_per_row = 1

        font.meta["psf1"] = {
            "mode": mode,
        }
        font.meta["width"] = width
        font.meta["height"] = height
        font.meta["glyphs"] = glyphs
        font.meta["char_size"] = char_size

        raw_glyphs = self._read_glyphs(4, glyphs, height, width, char_size, bytes_per_row)

        for i, glyph_data in enumerate(raw_glyphs):
            font.glyphs[chr(i)] = glyph_data

    def _parse_psf2(self, font: Font):
        font.meta["format"] = "psf2"
        header = struct.unpack("<7I", self.data[4:32])  # Skip magic, read 7 values
        (
            version,
            header_size,
            flags,
            glyphs,
            char_size,
            height,
            width,
        ) = header

        if version != 0:
            raise PSFParseError("Unknown sub-version")
        if header_size != 32:
            raise PSFParseError("Unknown header size")

        bytes_per_row = (width + 7) // 8
        if char_size != height * bytes_per_row:
            raise PSFParseError("Mismatch in char byte size")

        font.meta["psf2"] = {
            "version": version,
            "header_size": header_size,
            "flags": flags,
        }
        font.meta["width"] = width
        font.meta["height"] = height
        font.meta["glyphs"] = glyphs
        font.meta["char_size"] = char_size

        raw_glyphs = self._read_glyphs(header_size, glyphs, height, width, char_size, bytes_per_row)

        unicode_map = {}
        if flags & 1:
            unicode_map = self._parse_unicode_table(header_size + glyphs * char_size, len(raw_glyphs))

        # Map glyphs to characters
        for i, glyph_data in enumerate(raw_glyphs):
            if i in unicode_map:
                for unicode_val in unicode_map[i]:
                    font.glyphs[chr(unicode_val)] = glyph_data
            else:
                # Fallback for glyphs not in the unicode map
                if i < 256:
                    font.glyphs[chr(i)] = glyph_data

    def _read_glyphs(
        self, offset: int, glyph_count: int, height: int, width: int, char_size: int, bytes_per_row: int
    ) -> list[list[list[bool]]]:
        """Read glyphs and return as a list of pixel arrays."""
        data_pos = offset
        all_glyphs = []

        for glyph_idx in range(glyph_count):
            glyph_pixels = []

            for y in range(height):
                row_pixels = []
                x = 0

                for byte_idx in range(bytes_per_row):
                    if data_pos < len(self.data):
                        byte_value = self.data[data_pos]
                        data_pos += 1
                    else:
                        byte_value = 0

                    for bit in range(8):
                        if x < width:
                            pixel_on = bool(byte_value & (1 << (7 - bit)))
                            row_pixels.append(pixel_on)
                            x += 1

                glyph_pixels.append(row_pixels)

            all_glyphs.append(glyph_pixels)
        return all_glyphs

    def _parse_unicode_table(self, offset: int, glyph_count: int) -> dict[int, list[int]]:
        """Parse PSF2 unicode mapping table and return a dictionary."""
        pos = offset
        glyph_index = 0
        unicode_map = {}

        while pos < len(self.data) and glyph_index < glyph_count:
            unicode_list = []

            while pos < len(self.data):
                if pos + 1 < len(self.data):
                    unicode_val = struct.unpack("<H", self.data[pos : pos + 2])[0]
                    pos += 2

                    if unicode_val == 0xFFFF:
                        break
                    elif unicode_val == 0xFFFE:
                        continue
                    else:
                        unicode_list.append(unicode_val)
                else:
                    break

            if unicode_list:
                unicode_map[glyph_index] = unicode_list

            glyph_index += 1
        return unicode_map
