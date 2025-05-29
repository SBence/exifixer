# EXIFixer

A Python script to set EXIF timestamps of JPG images based on file names

## Installation

```sh
pip install -r requirements.txt
```

## Usage

```sh
python exifixer.py [options] <path to image folder>
```

### Options

- `--dry-run`: Show updates without modifying files
- `-q`, `--quiet`, `-s`, `--silent`: Suppress all output except errors
- `-v`, `--verbose`: Show successful updates

### Example

```sh
python exifixer.py --verbose Pictures
```
