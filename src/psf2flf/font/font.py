from dataclasses import dataclass, field


@dataclass
class Font:
    """A generic representation of a font."""

    meta: dict = field(default_factory=dict)
    glyphs: dict = field(default_factory=dict)

    @property
    def name(self) -> str:
        """Get the font name from metadata."""
        return self.meta.get("name", "")

    @property
    def style(self) -> frozenset[str]:
        """Get the font style from metadata."""
        return self.meta.get("styles", frozenset())

    @property
    def width(self) -> int:
        """Get the font width from metadata."""
        return self.meta.get("width", 0)

    @property
    def height(self) -> int:
        """Get the font height from metadata."""
        return self.meta.get("height", 0)

    def __eq__(self, other) -> bool:
        """Two fonts are equal if name, style, width, height match and overlapping ASCII glyphs are identical."""
        if not isinstance(other, Font):
            return False

        # Check basic properties
        if (
            self.name != other.name
            or self.style != other.style
            or self.width != other.width
            or self.height != other.height
        ):
            return False

        # Get ASCII printable characters that exist in both fonts
        ascii_chars = set(chr(i) for i in range(32, 128))
        self_chars = set(self.glyphs.keys())
        other_chars = set(other.glyphs.keys())
        common_ascii = ascii_chars & self_chars & other_chars

        # Check that common ASCII glyphs are identical
        for char in common_ascii:
            if self.glyphs[char] != other.glyphs[char]:
                return False

        return True
