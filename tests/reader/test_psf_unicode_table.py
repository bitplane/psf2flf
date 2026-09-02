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
