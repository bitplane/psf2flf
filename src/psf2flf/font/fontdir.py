from dataclasses import dataclass, field
from pathlib import Path
import tarfile
from typing import Union

from .font import Font
from .typeface import TypeFace


@dataclass
class FontDir:
    """A collection of typefaces, typically representing a font directory or archive."""

    typefaces: dict[str, TypeFace] = field(default_factory=dict)

    def __iadd__(self, other: Union[Font, TypeFace]):
        """Add a font or typeface to this directory."""
        if isinstance(other, Font):
            return self._add_font(other)
        elif isinstance(other, TypeFace):
            return self._add_typeface(other)
        else:
            raise TypeError(f"Cannot add {type(other).__name__} to FontDir")

    def _add_font(self, font: Font):
        """Add a font to the appropriate typeface."""
        family_name = font.name

        if family_name not in self.typefaces:
            # Create new typeface for this family
            self.typefaces[family_name] = TypeFace(name=family_name)

        # Add font to the typeface
        self.typefaces[family_name] += font
        return self

    def _add_typeface(self, typeface: TypeFace):
        """Add an entire typeface to this directory."""
        family_name = typeface.name

        if family_name not in self.typefaces:
            # Simply add the new typeface
            self.typefaces[family_name] = typeface
        else:
            # Merge with existing typeface by adding all fonts
            existing_typeface = self.typefaces[family_name]
            for style_group in typeface.styles.values():
                for font in style_group.values():
                    existing_typeface += font

        return self

    def _output_fonts(self, tall_mode: bool) -> dict[str, Font]:
        """Plan unique output names before opening any destination."""
        outputs = {}
        for family_name, typeface in self.typefaces.items():
            for style_group in typeface.styles.values():
                for font in style_group.values():
                    styles = sorted(s for s in font.style if not any(c.isdigit() for c in s))
                    if tall_mode and "Narrow" not in styles:
                        styles.append("Narrow")
                    height = font.height if tall_mode else (font.height + 1) // 2
                    # Odd and even source heights can have the same compressed height.
                    source = f"-source{font.height}" if not tall_mode and font.height % 2 else ""
                    filename = f"{family_name}{''.join(styles)}{height}x{font.width}{source}.flf"
                    if filename in outputs:
                        raise ValueError(f"Duplicate output filename: {filename}")
                    outputs[filename] = font
        return outputs

    def write_directory(self, output_dir: Path, tall_mode: bool = False):
        """Write all typefaces to a directory structure."""
        from ..writer import write

        outputs = self._output_fonts(tall_mode)
        output_dir.mkdir(parents=True, exist_ok=True)
        for filename, font in outputs.items():
            output_path = output_dir / filename
            write(font, output_path, tall_mode)
            print(f"Written: {output_path}")

    def write_tar(self, output_path: Path, tall_mode: bool = False):
        """Write all typefaces to a tar archive."""
        import tempfile
        from ..writer import write

        outputs = self._output_fonts(tall_mode)
        with tarfile.open(output_path, "w:gz") as tar:
            with tempfile.TemporaryDirectory() as temp_dir:
                for filename, font in outputs.items():
                    temp_file = Path(temp_dir) / filename
                    write(font, temp_file, tall_mode)
                    tar.add(temp_file, arcname=filename)
        print(f"Created archive: {output_path}")
