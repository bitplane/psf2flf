import subprocess
from pathlib import Path

import pytest
from pyfiglet import Figlet


@pytest.fixture
def psf_font_path():
    return Path(__file__).parent / "data" / "Uni1-VGA8.psf.gz"


def test_psf2flf_conversion_regression(psf_font_path, tmp_path):
    output_flf = tmp_path / "test_font.flf"

    result = subprocess.run(
        ["python", "-m", "psf2flf.main", str(psf_font_path), str(output_flf)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent / "src",
    )

    assert result.returncode == 0, f"Conversion failed: {result.stderr}"
    assert output_flf.exists(), "FLF file was not created"

    # Test that pyfiglet can load and use the font
    f = Figlet(font=str(output_flf).replace(".flf", ""), width=80)
    rendered_text = f.renderText("HELLO")

    # Store the expected output (pyfiglet adds trailing spaces)
    expected_output = (
        "██   ██ ▀██▀▀▀█ ▀██▀    ▀██▀    ▄█▀▀▀█▄ \n"
        "██▄▄▄██  ██▄█    ██      ██     ██   ██ \n"
        "██   ██  ██ ▀ ▄  ██  ▄█  ██  ▄█ ██   ██ \n"
        "▀▀   ▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀▀▀▀  ▀▀▀▀▀  \n"
    )

    assert rendered_text == expected_output


def test_psf2flf_tall_mode_regression(psf_font_path, tmp_path):
    output_flf = tmp_path / "test_font_tall.flf"

    result = subprocess.run(
        ["python", "-m", "psf2flf.main", "--tall", str(psf_font_path), str(output_flf)],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent / "src",
    )

    assert result.returncode == 0, f"Conversion failed: {result.stderr}"
    assert output_flf.exists(), "FLF file was not created"

    # Test that pyfiglet can load and use the font
    f = Figlet(font=str(output_flf).replace(".flf", ""), width=80)
    rendered_text = f.renderText("HELLO")

    # Tall mode should produce taller output (pyfiglet adds trailing spaces)
    expected_output = (
        "██   ██ ███████ ████    ████     █████  \n"
        "██   ██  ██   █  ██      ██     ██   ██ \n"
        "██   ██  ██ █    ██      ██     ██   ██ \n"
        "███████  ████    ██      ██     ██   ██ \n"
        "██   ██  ██ █    ██   █  ██   █ ██   ██ \n"
        "██   ██  ██   █  ██  ██  ██  ██ ██   ██ \n"
        "██   ██ ███████ ███████ ███████  █████  \n"
        "                                        \n"
    )

    assert rendered_text == expected_output
