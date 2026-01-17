# makes a CSV index of everything inside the Drive test folder (ids + basic metadata)

import csv
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "secrets/inf191a-uci-nature-sa.json"
FOLDER_ID = "1MLRCj2kQrKnlwRPto4Z5eFka5HgDaLOv"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

OUT_CSV = Path("data/outputs/drive_index.csv")

FIELDS = ["file_name", "file_id", "drive_folder_id", "mimeType", "modifiedTime", "size"]


def main():
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive = build("drive", "v3", credentials=creds)
    query = f"'{FOLDER_ID}' in parents and trashed = false"

    rows = []
    page_token = None

    while True:
        resp = drive.files().list(
            q=query,
            fields="nextPageToken, files(id,name,mimeType,modifiedTime,size,parents)",
            pageSize=1000,
            pageToken=page_token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()

        for item in resp.get("files", []):
            parents = item.get("parents") or [""]

            rows.append({
                "file_name": item.get("name", ""),
                "file_id": item.get("id", ""),
                "drive_folder_id": parents[0],
                "mimeType": item.get("mimeType", ""),
                "modifiedTime": item.get("modifiedTime", ""),
                "size": item.get("size", ""),
            })

        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    rows.sort(key=lambda r: r["file_name"])

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {len(rows)} rows -> {OUT_CSV}")
    if rows:
        print("Example:", rows[0]["file_name"], rows[0]["file_id"])


if __name__ == "__main__":
    main()