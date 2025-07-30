import pytest

from psf2flf.reader.psf import _parse_psf_filename


@pytest.mark.parametrize(
    "filename,expected_name,expected_styles,expected_size,expected_charset",
    [
        ("Arabic-Fixed15.psf.gz", "Fixed", frozenset(["15"]), 15, "Arabic"),
        ("Arabic-VGA28x16.psf.gz", "VGA", frozenset(["28x16"]), 28, "Arabic"),
        ("CyrAsia-TerminusBold14.psf.gz", "Terminus", frozenset(["Bold", "14"]), 14, "CyrAsia"),
        ("matrix.psf.gz", "matrix", frozenset(), None, None),
        ("Lat15-Fixed13.psf.gz", "Fixed", frozenset(["13"]), 13, "Lat15"),
        ("Vietnamese-TerminusBold32x16.psf.gz", "Terminus", frozenset(["Bold", "32x16"]), 32, "Vietnamese"),
        ("Uni2-Terminus12x6.psf.gz", "Terminus", frozenset(["12x6"]), 12, "Uni2"),
        ("Greek-Fixed18.psf.gz", "Fixed", frozenset(["18"]), 18, "Greek"),
        ("Lao-Fixed14.psf.gz", "Fixed", frozenset(["14"]), 14, "Lao"),
        ("SomeFont.psf", "SomeFont", frozenset(), None, None),
        ("Another-Font-10x20.psf", "Font", frozenset(["10x20"]), 10, "Another"),
        ("NoMatchHere.txt", "NoMatchHere", frozenset(), None, None),  # Should not match regex
    ],
)
def test_parse_psf_filename(filename, expected_name, expected_styles, expected_size, expected_charset):
    name, styles, size, charset = _parse_psf_filename(filename)
    assert name == expected_name
    assert styles == expected_styles
    assert size == expected_size
    assert charset == expected_charset
