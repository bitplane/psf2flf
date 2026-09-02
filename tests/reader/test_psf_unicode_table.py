import struct

from psf2flf.reader.psf import PSFReader


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
