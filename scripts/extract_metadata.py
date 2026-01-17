# reads manifest.csv and extract EXIF datetime and image width/height for each local file.

import csv
from pathlib import Path
from PIL import Image
import exifread

MANIFEST = Path("data/outputs/manifest.csv")
OUT_CSV = Path("data/outputs/metadata.csv")


def get_exif_datetime(path: Path) -> str:
    try:
        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)

        for key in ("EXIF DateTimeOriginal", "EXIF DateTimeDigitized", "Image DateTime"):
            if key in tags:
                return str(tags[key])
    except Exception:
        return ""

    return ""


def get_size(path: Path):
    try:
        with Image.open(path) as img:
            return img.width, img.height
    except Exception:
        return "", ""


def main():
    if not MANIFEST.exists():
        raise FileNotFoundError("manifest.csv not found. Run download and make_manifest first.")

    rows_out = []
    with open(MANIFEST, "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            path = Path(row["local_path"])
            exif_dt = get_exif_datetime(path)
            w, h = get_size(path)

            rows_out.append(
                {
                    "file_id": row["file_id"],
                    "file_name": row["file_name"],
                    "local_file_name": row["local_file_name"],
                    "exif_datetime": exif_dt,
                    "width": w,
                    "height": h,
                }
            )

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["file_id", "file_name", "local_file_name", "exif_datetime", "width", "height"],
        )
        w.writeheader()
        w.writerows(rows_out)

    print(f"wrote {len(rows_out)} rows -> {OUT_CSV}")


if __name__ == "__main__":
    main()