import struct

import pytest

from psf2flf.reader.psf import PSFParseError, PSFReader


def test_psf1_sequence_members_are_not_standalone_mappings():
    reader = PSFReader()
    reader.data = struct.pack("<5H", 0x00C5, 0x212B, 0xFFFE, 0x0041, 0x030A) + struct.pack("<H", 0xFFFF)

    unicode_map = reader._parse_unicode_table(0, 1, is_psf1=True)

    assert unicode_map == {0: [0x00C5, 0x212B]}


def test_psf2_sequence_members_are_not_standalone_mappings():
    reader = PSFReader()
    reader.data = "ÅÅ".encode() + b"\xfe" + "A\u030a".encode() + b"\xff"

    unicode_map = reader._parse_unicode_table(0, 1)

    assert unicode_map == {0: [0x00C5, 0x212B]}


def test_truncated_psf1_bitmap_is_rejected(tmp_path):
    path = tmp_path / "truncated.psf"
    path.write_bytes(b"\x36\x04\x00\x01")

    with pytest.raises(PSFParseError, match="Truncated bitmap data"):
        PSFReader().read(path)


def test_truncated_psf2_bitmap_is_rejected_before_allocating(tmp_path):
    path = tmp_path / "truncated.psf"
    header = b"\x72\xb5\x4a\x86" + struct.pack("<7I", 0, 32, 0, 0xFFFFFFFF, 1, 1, 1)
    path.write_bytes(header)

    with pytest.raises(PSFParseError, match="Truncated bitmap data"):
        PSFReader().read(path)


@pytest.mark.parametrize("psf1", [True, False])
def test_unmapped_slots_do_not_overwrite_unicode_mappings(tmp_path, psf1):
    path = tmp_path / "mapped.psf"
    if psf1:
        header = b"\x36\x04\x02\x01"
        bitmap = b"\x80" + bytes(255)
        table = struct.pack("<2H", 65, 0xFFFF) + b"\xff\xff" * 255
    else:
        header = b"\x72\xb5\x4a\x86" + struct.pack("<7I", 0, 32, 1, 66, 1, 1, 8)
        bitmap = b"\x80" + bytes(65)
        table = b"A\xff" + b"\xff" * 65
    path.write_bytes(header + bitmap + table)
    font = PSFReader().read(path)
    assert set(font.glyphs) == {"A"}
    assert font.glyphs["A"][0][0] is True
