import gzip
import struct
from pathlib import Path
from typing import List, Dict, Union


class PSFParseError(Exception):
    pass


class PSFFont:
    def __init__(self, data: bytes):
        self.glyphs: List[bytes] = []
        self.unicode_map: Dict[int, List[int]] = {}
        self.width: int = 8
        self.height: int = 0
        self._parse(data)

    def _parse(self, data: bytes):
        if data.startswith(b"\x36\x04"):
            self._parse_psf1(data)
        elif data.startswith(b"\x72\xb5\x4a\x86"):
            self._parse_psf2(data)
        else:
            raise PSFParseError("Unrecognized PSF magic")

    def _parse_psf1(self, data: bytes):
        mode = data[2]
        charsize = data[3]
        has_unicode_table = mode & 0x02 or mode & 0x04
        glyph_count = 512 if mode & 0x01 else 256
        self.height = charsize
        self.width = 8
        glyph_data = data[4 : 4 + glyph_count * charsize]
        self.glyphs = [glyph_data[i * charsize : (i + 1) * charsize] for i in range(glyph_count)]

        if has_unicode_table:
            table = data[4 + glyph_count * charsize :]
            self._parse_unicode_table_psf1(table, glyph_count)

    def _parse_psf2(self, data: bytes):
        if len(data) < 32:
            raise PSFParseError("PSF2 header too short")
        header = struct.unpack("<IIIIIIII", data[0:32])
        magic, version, headersize, flags, length, charsize, width, height = header
        if magic != 0x864AB572:
            raise PSFParseError("Bad PSF2 magic")
        glyph_data = data[headersize : headersize + length * charsize]
        self.glyphs = [glyph_data[i * charsize : (i + 1) * charsize] for i in range(length)]
        self.width = width
        self.height = height
        if flags & 0x01:
            table = data[headersize + length * charsize :]
            self._parse_unicode_table_psf2(table, length)

    def _parse_unicode_table_psf1(self, table: bytes, glyph_count: int):
        index = 0
        for glyph_index in range(glyph_count):
            codepoints = []
            while index < len(table):
                u = table[index] | (table[index + 1] << 8)
                index += 2
                if u == 0xFFFF:
                    break
                if u == 0xFFFE:
                    continue  # sequences not supported
                codepoints.append(u)
            self.unicode_map[glyph_index] = codepoints

    def _parse_unicode_table_psf2(self, table: bytes, glyph_count: int):
        index = 0
        for glyph_index in range(glyph_count):
            codepoints = []
            while index < len(table):
                first = table[index]
                index += 1
                if first == 0xFF:
                    break
                elif first == 0xFE:
                    continue  # sequences not supported
                else:
                    # Decode UTF-8 sequence
                    start = index - 1
                    while index < len(table) and table[index] & 0xC0 == 0x80:
                        index += 1
                    try:
                        cp = bytes([first] + list(table[start + 1 : index]))
                        u = cp.decode("utf-8")
                        codepoints.append(ord(u))
                    except Exception:
                        pass
            self.unicode_map[glyph_index] = codepoints


def load_psf_file(path: Union[str, Path]) -> PSFFont:
    path = Path(path)
    with gzip.open(path, "rb") if path.suffix == ".gz" else open(path, "rb") as f:
        data = f.read()
    return PSFFont(data)
