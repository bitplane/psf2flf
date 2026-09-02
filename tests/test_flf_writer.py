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
