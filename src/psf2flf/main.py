import argparse
from pathlib import Path
from psf2flf import load_psf_file, convert_psf_to_flf


def convert_single(source: Path, dest: Path):
    font = load_psf_file(source)
    name = source.stem.replace(".psf", "").replace(".gz", "")
    out_path = convert_psf_to_flf(font, name, dest)
    print(f"Converted {source} → {out_path}")


def convert_all(source_dir: Path, dest_dir: Path):
    psf_files = list(source_dir.glob("*.psf")) + list(source_dir.glob("*.psf.gz"))
    for path in psf_files:
        try:
            convert_single(path, dest_dir)
        except Exception as e:
            print(f"Failed to convert {path.name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert PSF fonts to FLF (FIGlet) format.")
    parser.add_argument("source", nargs="?", help="PSF font file or input directory")
    parser.add_argument("dest", nargs="?", help="Output directory for FLF fonts")
    parser.add_argument("--all", action="store_true", help="Convert all PSF fonts in a directory")

    args = parser.parse_args()

    if args.all:
        if not args.source or not args.dest:
            parser.error("You must provide source and dest directories when using --all.")
        convert_all(Path(args.source), Path(args.dest))
    else:
        if not args.source or not args.dest:
            parser.error("You must provide a source PSF file and dest directory.")
        convert_single(Path(args.source), Path(args.dest))


if __name__ == "__main__":
    main()
