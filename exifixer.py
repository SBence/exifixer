import os
import re
from datetime import datetime
import piexif
import argparse

parser = argparse.ArgumentParser(description='Set EXIF timestamps of JPEG and WebP images based on file names')

parser.add_argument('directory', help='Path to the folder containing images')
parser.add_argument('--dry-run', action='store_true', help='Show updates without modifying files')
verbosity_group = parser.add_mutually_exclusive_group()
verbosity_group.add_argument('-q', '--quiet', '-s', '--silent', action='store_true', help='Suppress all output except errors')
verbosity_group.add_argument('-v', '--verbose', action='store_true', help='Show successful updates')

args = parser.parse_args()

pattern = re.compile(r"(?:\w{3}_)?(\d{8})_(\d{6})(?:_\d{3})?\.(?:jpe?g|webp)$", re.IGNORECASE)
summary_separator = "    "

count_success = 0
count_error = 0
count_skipped = 0

def log(message):
    if not args.quiet:
        print(message)

for root, _, files in os.walk(args.directory):
    for file_name in files:
        match = pattern.search(file_name)
        file_path = os.path.join(root, file_name)
        relative_path = os.path.relpath(file_path, args.directory)

        if match:
            date_str, time_str = match.groups()
            dt = datetime.strptime(date_str + time_str, "%Y%m%d%H%M%S")
            formatted_time = dt.strftime("%Y:%m:%d %H:%M:%S")

            try:
                if args.dry_run:
                    log(f"📝 Dry-run: {relative_path} -> {formatted_time}")

                else:
                    exif_dict = piexif.load(file_path)

                    encoded_time = formatted_time.encode("utf-8")
                    exif_dict["0th"][piexif.ImageIFD.DateTime] = encoded_time
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = encoded_time
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = encoded_time

                    exif_bytes = piexif.dump(exif_dict)
                    piexif.insert(exif_bytes, file_path)

                    count_success += 1

                    if args.verbose:
                        log(f"✅ Updated: {relative_path} -> {formatted_time}")

            except Exception as e:
                count_error += 1
                print(f"❌ Error updating: {relative_path}: {e}")

        else:
            count_skipped += 1
            log(f"⏭️  Skipped: {relative_path} (Unsupported file name, or not a JPEG or a WebP file)")

if args.dry_run:
    log(f"📝 Would update: {count_success}{summary_separator}⏭️  Skipped: {count_skipped}{summary_separator}❌ Errors: {count_error}")
else:
    log(f"✅ Updated: {count_success}{summary_separator}⏭️  Skipped: {count_skipped}{summary_separator}❌ Errors: {count_error}")
