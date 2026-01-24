# merges manifest.csv, metadata.csv, drive_index.csv into output.csv
import csv
from pathlib import Path

MANIFEST = Path("data/outputs/manifest.csv")
META = Path("data/outputs/metadata.csv")
DRIVE_INDEX = Path("data/outputs/drive_index.csv")
OUT = Path("data/outputs/output.csv")                  # keeping this for debugging
RESULTS = Path("data/outputs/results.csv")             # new


def load_csv_by_key(path: Path, key: str) -> dict:
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            k = row.get(key, "")
            if k:
                out[k] = row
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    if not MANIFEST.exists():
        raise FileNotFoundError("manifest.csv not found. Run make_manifest.py first.")
    if not META.exists():
        raise FileNotFoundError("metadata.csv not found. Run extract_metadata.py first.")
    if not DRIVE_INDEX.exists():
        raise FileNotFoundError("drive_index.csv not found. Run build_index.py first.")

    meta_by_id = load_csv_by_key(META, "file_id")
    drive_by_id = load_csv_by_key(DRIVE_INDEX, "file_id")

    out_rows = []

    with open(MANIFEST, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            file_id = row["file_id"]
            m = meta_by_id.get(file_id, {})
            d = drive_by_id.get(file_id, {})

            out_rows.append({
                "file_id": file_id,
                "file_name": row.get("file_name", ""),
                "local_file_name": row.get("local_file_name", ""),
                "local_path": row.get("local_path", ""),

                # local file info
                "size_bytes_local": row.get("size_bytes", ""),
                "modified_time_local": row.get("modified_time", ""),

                # extracted metadata
                "exif_datetime": m.get("exif_datetime", ""),
                "width": m.get("width", ""),
                "height": m.get("height", ""),

                # drive metadata
                "drive_folder_id": d.get("drive_folder_id", ""),
                "drive_modifiedTime": d.get("modifiedTime", ""),
                "drive_size": d.get("size", ""),
                "drive_mimeType": d.get("mimeType", ""),
            })

    out_rows.sort(key=lambda r: (r.get("file_name", ""), r.get("file_id", "")))

    write_csv(OUT, out_rows)
    print(f"wrote {len(out_rows)} rows -> {OUT}")

    results_rows = []
    for r in out_rows:
        timestamp = r.get("exif_datetime", "") or r.get("drive_modifiedTime", "")
        results_rows.append({
            "image_id": r.get("file_id", ""),
            "filename": r.get("file_name", ""),
            "local_path": r.get("local_path", ""),

            # will fill after we parse Drive folder paths
            "camera": "",
            "location": "",
            "deployment_id": "",

            "timestamp": timestamp,

            # fill later (ML)
            "species": "",
            "is_blank": "",
            "confidence": "",
            "uncertainty": "",
        })

    write_csv(RESULTS, results_rows)
    print(f"wrote {len(results_rows)} rows -> {RESULTS}")


if __name__ == "__main__":
    main()