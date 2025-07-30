from pathlib import Path

import pytest
from pyfiglet import Figlet

from psf2flf.main import cli


@pytest.fixture
def psf1_font_path():
    return Path(__file__).parent / "data" / "psf1" / "Uni1-VGA8.psf.gz"


@pytest.fixture
def psf2_font_path():
    return Path(__file__).parent / "data" / "psf2" / "Arabic-VGA32x16.psf.gz"


def test_psf1_conversion_regression(psf1_font_path, tmp_path):
    output_flf = tmp_path / "test_font.flf"

    result = cli([str(psf1_font_path), str(output_flf)])
    assert result == 0, f"Conversion failed with exit code {result}"
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


def test_psf1_tall_mode_regression(psf1_font_path, tmp_path):
    output_flf = tmp_path / "test_font_tall.flf"

    result = cli(["--tall", str(psf1_font_path), str(output_flf)])
    assert result == 0, f"Conversion failed with exit code {result}"
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


def test_psf2_conversion_regression(psf2_font_path, tmp_path):
    output_flf = tmp_path / "test_font.flf"

    result = cli([str(psf2_font_path), str(output_flf)])

    assert result == 0, f"Conversion failed with exit code {result}"
    assert output_flf.exists(), "FLF file was not created"

    # Test that pyfiglet can load and use the font
    f = Figlet(font=str(output_flf).replace(".flf", ""), width=80)
    rendered_text = f.renderText("HELLO")

    # Store the expected output (pyfiglet adds trailing spaces) - This is a 32x16 font
    expected_output = (
        "                                                                \n"
        "                                                                \n"
        "████      ████  ██████████████  ████████        ████████        \n"
        "████      ████    ████    ████    ████            ████          \n"
        "████      ████    ████      ██    ████            ████          \n"
        "████      ████    ████  ██        ████            ████          \n"
        "██████████████    ████████        ████            ████          \n"
        "████      ████    ████  ██        ████            ████          \n"
        "████      ████    ████            ████            ████          \n"
        "████      ████    ████      ██    ████      ██    ████      ██  \n"
        "████      ████    ████    ████    ████    ████    ████    ████  \n"
        "████      ████  ██████████████  ██████████████  ██████████████  \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                \n"
        "                \n"
        "  ██████████    \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "  ██████████    \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
    )

    assert rendered_text == expected_output


def test_psf2_tall_mode_regression(psf2_font_path, tmp_path):
    output_flf = tmp_path / "test_font_tall.flf"

    result = cli(["--tall", str(psf2_font_path), str(output_flf)])

    assert result == 0, f"Conversion failed with exit code {result}"
    assert output_flf.exists(), "FLF file was not created"

    # Test that pyfiglet can load and use the font
    f = Figlet(font=str(output_flf).replace(".flf", ""), width=80)
    rendered_text = f.renderText("HELLO")

    # Tall mode should produce taller output (pyfiglet adds trailing spaces) - 32x16 font
    expected_output = (
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "████      ████  ██████████████  ████████        ████████        \n"
        "████      ████  ██████████████  ████████        ████████        \n"
        "████      ████    ████    ████    ████            ████          \n"
        "████      ████    ████    ████    ████            ████          \n"
        "████      ████    ████      ██    ████            ████          \n"
        "████      ████    ████      ██    ████            ████          \n"
        "████      ████    ████  ██        ████            ████          \n"
        "████      ████    ████  ██        ████            ████          \n"
        "██████████████    ████████        ████            ████          \n"
        "██████████████    ████████        ████            ████          \n"
        "████      ████    ████  ██        ████            ████          \n"
        "████      ████    ████  ██        ████            ████          \n"
        "████      ████    ████            ████            ████          \n"
        "████      ████    ████            ████            ████          \n"
        "████      ████    ████      ██    ████      ██    ████      ██  \n"
        "████      ████    ████      ██    ████      ██    ████      ██  \n"
        "████      ████    ████    ████    ████    ████    ████    ████  \n"
        "████      ████    ████    ████    ████    ████    ████    ████  \n"
        "████      ████  ██████████████  ██████████████  ██████████████  \n"
        "████      ████  ██████████████  ██████████████  ██████████████  \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                                                                \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
        "  ██████████    \n"
        "  ██████████    \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "████      ████  \n"
        "  ██████████    \n"
        "  ██████████    \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
        "                \n"
    )

    assert rendered_text == expected_output
