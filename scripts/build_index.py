## makes a CSV index of everything inside the Drive folder (ids + basic metadata)
# new: recursive + drive_path + parsed folder fields (site, deployment info)

import csv
import re
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build

SERVICE_ACCOUNT_FILE = "secrets/inf191a-uci-nature-sa.json"
FOLDER_ID = "0ACQBvZlfUN2CUk9PVA"
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

OUT_CSV = Path("data/outputs/drive_index.csv")

FIELDS = [
    "file_name", "file_id", "drive_folder_id", "mimeType", "modifiedTime", "size",
    "drive_path",
    "site", "deployment_folder", "deployment_id", "status",
]

FOLDER_MIMETYPE = "application/vnd.google-apps.folder"      # crawl folders

PRINT_EVERY = 500        # progress print
MAX_ROWS = 2000          # leave none for full run


def parse_drive_path(drive_path: str):
    parts = drive_path.split("/")
    site = parts[0] if parts else ""

    deployment_folder = parts[1] if len(parts) > 1 else ""
    deployment_id = ""
    status = ""

    m = re.match(r"^(\d{1,3})_", deployment_folder)
    if m:
        deployment_id = m.group(1)

    if deployment_folder.endswith("_DONE"):
        status = "DONE"

    return site, deployment_folder, deployment_id, status


def list_children(drive, folder_id: str):
    query = f"'{folder_id}' in parents and trashed = false"
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
            yield item

        page_token = resp.get("nextPageToken")
        if not page_token:
            break


def main():
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive = build("drive", "v3", credentials=creds)

    rows = []

    stack = [(FOLDER_ID, "")]      # start crawling from root
    seen = set()
    folders_done = 0

    while stack:
        current_folder_id, prefix = stack.pop()

        if current_folder_id in seen:
            continue
        seen.add(current_folder_id)

        folders_done += 1
        if folders_done % 25 == 0:
            print(f"folders visited: {folders_done}, rows so far: {len(rows)}")

        for item in list_children(drive, current_folder_id):
            name = item.get("name", "")
            drive_path = f"{prefix}/{name}" if prefix else name

            if item.get("mimeType") == FOLDER_MIMETYPE:
                stack.append((item["id"], drive_path))
                continue

            if not item.get("mimeType", "").startswith("image/"):
                continue

            parents = item.get("parents") or [current_folder_id]
            site, deployment_folder, deployment_id, status = parse_drive_path(drive_path)

            rows.append({
                "file_name": name,
                "file_id": item.get("id", ""),
                "drive_folder_id": parents[0],
                "mimeType": item.get("mimeType", ""),
                "modifiedTime": item.get("modifiedTime", ""),
                "size": item.get("size", ""),
                "drive_path": drive_path,
                "site": site,
                "deployment_folder": deployment_folder,
                "deployment_id": deployment_id,
                "status": status,
            })

            if len(rows) % PRINT_EVERY == 0:
                print(f"rows indexed: {len(rows)}")

            if MAX_ROWS is not None and len(rows) >= MAX_ROWS:
                print(f"stopping early at MAX_ROWS={MAX_ROWS}")
                stack.clear()
                break

    rows.sort(key=lambda r: r["drive_path"])

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    print(f"wrote {len(rows)} rows -> {OUT_CSV}")
    if rows:
        print("Example path:", rows[0]["drive_path"])


if __name__ == "__main__":
    main()