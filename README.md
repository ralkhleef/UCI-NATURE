# Wildlife Camera Image Processing Pipeline

Automated data pipeline for processing 100,000+ wildlife camera images from UCI Campus Reserves.

## Problem

Current workflow relies on manual review by student interns. Images accumulate faster than they can be processed, creating a backlog of 100,000+ unprocessed images. No project funding available for cloud services.

## Solution

Automated pipeline that retrieves images from Google Drive, extracts metadata, detects duplicates, and classifies images as blank or containing animals.

## Pipeline Flow

```
Google Drive → Download → Metadata → Duplicate Detection → Classification → CSV Output
```

## Components

**Core Scripts:**
- `build_index.py` - Index Google Drive files
- `download_drive.py` - Download images (with resume)
- `make_manifest.py` - Create file manifest
- `extract_metadata.py` - Extract EXIF data
- `make_output.py` - Generate final CSV
- `run_pipeline.py` - Execute full pipeline

**Additional:**
- `detect_duplicates.py` - Perceptual hashing for duplicate detection
- `config.py` - Configuration settings

## Installation

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
pip install Pillow exifread imagehash
```

## Setup

1. Create service account at Google Cloud Console
2. Save credentials as `secrets/inf191a-uci-nature-sa.json`
3. Share Drive folder with service account email
4. Update `FOLDER_ID` in `config.py`

## Usage

**Full pipeline:**
```bash
python run_pipeline.py
```

**Individual steps:**
```bash
python build_index.py          # Index Drive
python download_drive.py        # Download images
python make_manifest.py         # Create manifest
python extract_metadata.py      # Extract EXIF
python detect_duplicates.py     # Find duplicates
python make_output.py           # Generate CSV
```

## Output

CSV files in `data/outputs/`:
- `drive_index.csv` - Drive file listing
- `download_log.csv` - Download status
- `manifest.csv` - Local file manifest
- `metadata.csv` - EXIF data
- `duplicate_report.csv` - Duplicate groups
- `output.csv` - Final merged data

## Project Structure

```
project/
├── scripts/
│   ├── build_index.py
│   ├── download_drive.py
│   ├── make_manifest.py
│   ├── extract_metadata.py
│   ├── make_output.py
│   ├── detect_duplicates.py
│   └── run_pipeline.py
├── data/
│   ├── staging/          # Downloaded images
│   └── outputs/          # CSV outputs
├── secrets/
│   └── inf191a-uci-nature-sa.json
└── config.py
```

## Team

- Ghadeer Al Jufout 
- Ranya A. Alkhleef 
- Andy Dao Hoang
- Jadon Tapp 
- Yifan Wu 

## Partner

Julie Ellen Coffey - UCI Campus Reserves Manager
