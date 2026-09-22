from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile


@contextmanager
def atomic_output(path: Path):
    """Replace a destination only after its sibling temporary file is complete."""
    with NamedTemporaryFile(dir=path.parent, prefix=f".{path.name}.", delete=False) as temp:
        temporary = Path(temp.name)
    try:
        yield temporary
        if path.exists():
            temporary.chmod(path.stat().st_mode & 0o777)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def print_dict(data: dict, prefix: str = ""):
    """Recursively prints the key-value pairs of a dictionary."""
    for key, value in data.items():
        new_prefix = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            print_dict(value, new_prefix)
        else:
            print(f"{new_prefix}: {value}")
