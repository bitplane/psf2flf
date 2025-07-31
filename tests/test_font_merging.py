import pytest
from pathlib import Path

from psf2flf.font import Font, FontDir, TypeFace
from psf2flf.reader import read


class TestFontMerging:
    """Test Font merging functionality."""

    def test_font_equality_same_font(self):
        """Test that identical fonts are equal."""
        font1 = Font()
        font1.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font1.glyphs = {chr(65): ((True, False), (False, True))}

        font2 = Font()
        font2.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font2.glyphs = {chr(65): ((True, False), (False, True))}

        assert font1 == font2

    def test_font_equality_different_glyphs(self):
        """Test that fonts with different glyphs are not equal."""
        font1 = Font()
        font1.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font1.glyphs = {chr(65): ((True, False), (False, True))}

        font2 = Font()
        font2.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font2.glyphs = {chr(65): ((False, True), (True, False))}

        assert font1 != font2

    def test_font_merge_compatible(self):
        """Test merging compatible fonts."""
        font1 = Font()
        font1.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16, "charset": "Uni1"}
        font1.glyphs = {chr(65): ((True, False), (False, True))}

        font2 = Font()
        font2.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16, "charset": "Uni2"}
        font2.glyphs = {chr(66): ((False, True), (True, False))}

        font1 += font2

        assert len(font1.glyphs) == 2
        assert chr(65) in font1.glyphs
        assert chr(66) in font1.glyphs
        assert font1.meta["charset"] == "Uni1+Uni2"

    def test_font_merge_incompatible_name(self):
        """Test that merging fonts with different names fails."""
        font1 = Font()
        font1.meta = {"name": "Test1", "styles": frozenset({"Bold"}), "width": 8, "height": 16}

        font2 = Font()
        font2.meta = {"name": "Test2", "styles": frozenset({"Bold"}), "width": 8, "height": 16}

        with pytest.raises(ValueError, match="Cannot merge incompatible fonts"):
            font1 += font2

    def test_font_merge_conflicting_glyphs(self):
        """Test that merging fonts with conflicting glyphs skips conflicts (gap-fill only)."""
        font1 = Font()
        font1.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font1.glyphs = {chr(65): ((True, False), (False, True))}

        font2 = Font()
        font2.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font2.glyphs = {chr(65): ((False, True), (True, False)), chr(66): ((True, True), (False, False))}

        font1 += font2

        # Should keep original glyph for A and add new glyph for B
        assert len(font1.glyphs) == 2
        assert font1.glyphs[chr(65)] == ((True, False), (False, True))  # Original kept
        assert font1.glyphs[chr(66)] == ((True, True), (False, False))  # New added


class TestTypeFace:
    """Test TypeFace functionality."""

    def test_typeface_add_font(self):
        """Test adding a font to a typeface."""
        typeface = TypeFace(name="Test")

        font = Font()
        font.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font.glyphs = {chr(65): ((True, False), (False, True))}

        typeface += font

        assert frozenset({"Bold"}) in typeface.styles
        assert 16 in typeface.styles[frozenset({"Bold"})]
        assert typeface.styles[frozenset({"Bold"})][16] == font

    def test_typeface_add_incompatible_font(self):
        """Test that adding incompatible font to typeface fails."""
        typeface = TypeFace(name="Test")

        font = Font()
        font.meta = {"name": "Different", "styles": frozenset({"Bold"}), "width": 8, "height": 16}

        with pytest.raises(ValueError, match="family name mismatch"):
            typeface += font


class TestFontDir:
    """Test FontDir functionality."""

    def test_fontdir_add_font(self):
        """Test adding a font to a font directory."""
        fontdir = FontDir()

        font = Font()
        font.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font.glyphs = {chr(65): ((True, False), (False, True))}

        fontdir += font

        assert "Test" in fontdir.typefaces
        assert fontdir.typefaces["Test"].name == "Test"

    def test_fontdir_add_typeface(self):
        """Test adding a typeface to a font directory."""
        fontdir = FontDir()
        typeface = TypeFace(name="Test")

        font = Font()
        font.meta = {"name": "Test", "styles": frozenset({"Bold"}), "width": 8, "height": 16}
        font.glyphs = {chr(65): ((True, False), (False, True))}

        typeface += font
        fontdir += typeface

        assert "Test" in fontdir.typefaces
        assert fontdir.typefaces["Test"] == typeface


class TestRealFonts:
    """Test with real PSF files."""

    def test_load_psf1_font(self):
        """Test loading a PSF1 font."""
        font_path = Path("tests/data/psf1/Uni1-VGA8.psf.gz")
        if font_path.exists():
            font = read(font_path)
            assert font.name == "VGA"
            assert font.width == 8
            assert font.height == 8
            assert len(font.glyphs) > 0

    def test_load_psf2_font(self):
        """Test loading a PSF2 font."""
        font_path = Path("tests/data/psf2/Arabic-VGA32x16.psf.gz")
        if font_path.exists():
            font = read(font_path)
            assert font.name == "VGA"
            assert font.width == 16
            assert font.height == 32
            assert len(font.glyphs) > 0

    @pytest.mark.skipif(
        not Path("/usr/share/consolefonts/Uni1-Fixed15.psf.gz").exists(), reason="System fonts not available"
    )
    def test_merge_real_fonts(self):
        """Test merging real system fonts."""
        font1 = read(Path("/usr/share/consolefonts/Uni1-Fixed15.psf.gz"))
        font2 = read(Path("/usr/share/consolefonts/Uni2-Fixed15.psf.gz"))

        initial_glyph_count = len(font1.glyphs)
        font1 += font2

        # Should have more glyphs after merging
        assert len(font1.glyphs) >= initial_glyph_count
        assert font1.meta["charset"] == "Uni1+Uni2"
