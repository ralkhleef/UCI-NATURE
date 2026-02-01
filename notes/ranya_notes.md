**Last updated:** Feb 2026  
---

## Project Goal

- Process **100,000+ unprocessed wildlife images** in Google Drive
- Build a **reliable, low-cost pipeline**
- Output a **usable spreadsheet** for non-technical users

**Key constraints**
- ML accuracy is secondary
- Pipeline correctness > model performance
- Species classification is future work

---

## Pipeline Overview

index → download → parse → merge → export


- **Index:** collect image file IDs + full Drive paths  
- **Download:** download by file ID, preserve folder structure  
- **Parse:** extract EXIF metadata (date/time)  
- **Merge:** combine metadata + ML placeholders  
- **Export:** output final CSV

---

## Repository Structure

secrets/
service_account.json

scripts/
build_index.py
download_drive.py
extract_metadata.py
make_output.py
run_pipeline.py

data/
images/ # mirrors Drive folders
outputs/
drive_index.csv
download_log.csv
metadata.csv
output.csv


---

## Script Responsibilities

### build_index.py
- Recursively scans Google Drive
- Images only (no folders, no spreadsheets)
- Captures:
  - file_id
  - file_name
  - mime_type
  - drive_path
- Output:
  - data/outputs/drive_index.csv

---

### download_drive.py
- Reads drive_index.csv
- Downloads images using file_id
- Saves to data/images/ using Drive path
- Avoids filename collisions
- Logs download results
- Output:
  - data/outputs/download_log.csv

---

### extract_metadata.py
- Reads downloaded images
- Extracts EXIF:
  - date
  - time
- Adds ML placeholder columns
- Output:
  - data/outputs/metadata.csv

---

### make_output.py
- Merges:
  - drive_index
  - local file paths
  - image metadata
  - ML placeholders
- Output:
  - data/outputs/output.csv

---

### run_pipeline.py
Runs scripts in order:
1. build_index  
2. download_drive  
3. extract_metadata  
4. make_output  

---

## Output Columns

**Current / Planned**
- image_id
- camera_name (from folder path)
- date
- time
- species (placeholder)
- count (placeholder)
- model_certainty (placeholder)

**Excluded**
- deployment dates
- processing time
- cloud metrics

---

## Dependencies

- Python 3.10+
- Google Drive API
- Service account key in secrets/

**Packages**
- google-api-python-client
- google-auth
- pillow
- exifread

---

## Run Commands

Full pipeline:
python scripts/run_pipeline.py


Single step:

python scripts/build_index.py
python scripts/download_drive.py

---

## Current Status

**Working**
- Drive indexing (recursive)
- File ID–based downloads
- Folder structure preserved
- Metadata extraction
- CSV outputs

**Missing**
- Blank vs animal detection
- Species classification
- Retry / resume logic
- Duplicate detection
- Long-term storage solution

---

## Next Steps

- Pilot on small image batch
- Validate output CSV with partner
- Add blank vs animal classification
- Improve reliability (resume, dedupe)
