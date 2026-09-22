from psf2flf.font import Font
from psf2flf.writer.flf import FLFWriter


def test_header_counts_only_code_tagged_glyphs(tmp_path):
    font = Font(
        meta={"width": 1, "height": 1},
        glyphs={"A": ((True,),), "é": ((True,),)},
    )
    output = tmp_path / "font.flf"

    FLFWriter().write(font, output)

    header = output.read_text(encoding="utf-8").splitlines()[0]
    assert header.split()[-1] == "1"


def test_required_and_extended_glyphs_roundtrip(tmp_path):
    from pyfiglet import Figlet

    chars = "AÄÖÜäöüßéΩ" + "".join(map(chr, range(160, 166)))
    font = Font(meta={"width": 1, "height": 2}, glyphs={c: ((True,), (True,)) for c in chars})
    output = tmp_path / "unicode.flf"
    FLFWriter().write(font, output)
    loaded = Figlet(font=str(output.with_suffix(""))).Font
    for char in chars:
        assert loaded.chars[ord(char)] == ["█$"]
    assert int(output.read_text().splitlines()[0].split()[-1]) == 8
