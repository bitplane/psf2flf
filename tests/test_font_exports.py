import tarfile

import pytest

from psf2flf.font import Font, FontDir


def make_font(height, width=8, styles=frozenset()):
    return Font(
        meta={"name": "Fixed", "height": height, "width": width, "styles": styles},
        glyphs={"A": ((True,) * width,) * height},
    )


def test_compressed_height_variants_have_distinct_outputs(tmp_path):
    fonts = FontDir()
    fonts += make_font(15)
    fonts += make_font(16)
    fonts.write_directory(tmp_path / "fonts")
    names = {p.name for p in (tmp_path / "fonts").iterdir()}
    assert names == {"Fixed8x8-source15.flf", "Fixed8x8.flf"}
    fonts.write_tar(tmp_path / "fonts.tar")
    with tarfile.open(tmp_path / "fonts.tar") as archive:
        assert len(archive.getnames()) == 2
        assert set(archive.getnames()) == names


@pytest.mark.parametrize("archive", [False, True])
def test_duplicate_names_are_rejected_before_writing(tmp_path, archive):
    fonts = FontDir()
    fonts += make_font(16, styles=frozenset({"16"}))
    fonts += make_font(16, styles=frozenset({"16x8"}))
    destination = tmp_path / ("fonts.tar" if archive else "fonts")
    with pytest.raises(ValueError, match="Duplicate output filename"):
        (fonts.write_tar if archive else fonts.write_directory)(destination)
    assert not destination.exists()
