Date: Jan 17, 2026

# project goal
- address a backlog of 100,00+ unprocessed images stored in google drive
- build a functional data pipeline that:
    - retrieves images from google drive
    - classifies images as blank vs containing animals
    - create a structured spreadsheet with results 
- ML accuracy is secondary, the primary deliverable is a working pipeline

# folder structure
- secrets/
    - service account key
- scripts/
    - build_index.py 
        - lists files in the google drive test folder
        - saves drive metadata (file_id, name, size, time)
        - output result drive_index.csv
    - download_drive.py
        - downloads images from drive into data/staging
        - renames files as file_id_originalname to avoid dupes
        - logs successes/failures
        - output results download_log.csv
    - make_manifest.py
        - creates a map of downloaded files
        - links drive IDs to local file paths
        - output result manifest.csv
    - extract_metadata.py
        - reads image EXIF data (date/time) and image size
        - output results metadata.csv
    - make_output.py
        - merges drive metadata,local file info, EXIF metadata
        - might add placeholder columns for ML (like has_animal or condfidence levels)
        - output results output.csv
    - run_pipeline.py
        - runs all scripts in order
        - output results output.csv
- data/staging/
    - temp local image downloads
- data/outputs/
    - drive_index.csv
        - lists everything in the test folder
    - download_log.csv
        - log of each download attempt
    - manifest.csv
        - map of downloaded files local
    - metadata.csv
    -   image info pulled from the jpg file
    - output.csv
        - merges drive metadata, local file info and image metadata

# dependencies
- python 3.10+
- googledrive api enabled
- service account key in secrets/inf191a-uci-nature-sa.json
- python packages needed(also listed in requirments.txt):
    - google-api-python-client
    - google-auth
    - pillow 
    - exilfread

# install w/
- pip install google-api-python-client google-auth pillow exifread

# how to run
- python scripts/run_pipeline.py
    - or python scripts/<filename>.py

# current status 1/17
- google drive api works
- pulls images from google drive, avoids duplicate file names and exports metadata into CSVs
- it doesn’t do any animal detection yet

# what still needs work
- does NOT 
    - detect animals
    - classify species
    - separate blank vs animal images
- implement a rerun function to avoid redownloading too much
- add helpers
