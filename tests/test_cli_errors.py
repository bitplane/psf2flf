from psf2flf.main import cli


def test_directory_conversion_fails_when_an_input_is_missing(tmp_path):
    result = cli([str(tmp_path / "missing.psf"), str(tmp_path / "output")])

    assert result == 1


def test_all_conversion_fails_when_input_directory_is_missing(tmp_path):
    result = cli(["--all", str(tmp_path / "missing"), str(tmp_path / "output")])

    assert result == 1
