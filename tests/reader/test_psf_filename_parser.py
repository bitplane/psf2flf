import pytest

from psf2flf.reader.psf import _parse_psf_filename


@pytest.mark.parametrize(
    "filename,expected_name,expected_styles,expected_size",
    [
        ("Arabic-Fixed15.psf.gz", "Fixed", frozenset(["Arabic", "15"]), 15),
        ("Arabic-VGA28x16.psf.gz", "VGA", frozenset(["Arabic", "28x16"]), 28),
        ("CyrAsia-TerminusBold14.psf.gz", "Terminus", frozenset(["CyrAsia", "Bold", "14"]), 14),
        ("matrix.psf.gz", "matrix", frozenset(), None),
        ("Lat15-Fixed13.psf.gz", "Fixed", frozenset(["Lat15", "13"]), 13),
        ("Vietnamese-TerminusBold32x16.psf.gz", "Terminus", frozenset(["Vietnamese", "Bold", "32x16"]), 32),
        ("Uni2-Terminus12x6.psf.gz", "Terminus", frozenset(["Uni2", "12x6"]), 12),
        ("Greek-Fixed18.psf.gz", "Fixed", frozenset(["Greek", "18"]), 18),
        ("Lao-Fixed14.psf.gz", "Fixed", frozenset(["Lao", "14"]), 14),
        ("SomeFont.psf", "SomeFont", frozenset(), None),
        ("Another-Font-10x20.psf", "Font", frozenset(["Another", "10x20"]), 10),
        ("NoMatchHere.txt", "NoMatchHere", frozenset(), None),  # Should not match regex
    ],
)
def test_parse_psf_filename(filename, expected_name, expected_styles, expected_size):
    name, styles, size = _parse_psf_filename(filename)
    assert name == expected_name
    assert styles == expected_styles
    assert size == expected_size
