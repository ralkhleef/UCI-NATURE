# To-Do

### 1. Recursive Drive indexing
- Update `build_index.py` to crawl the **entire** Drive folder (including all subfolders), not just the top-level folder.
- Make sure the index includes all files + basic metadata.

### 2. Remove download cap + add resume
- Remove/increase `MAX_DOWNLOADS`.
- Add a **resume mechanism** so rerunning the script continues where it left off (no restarting).

### 3. Retry + failure logging
- Add retries for failed downloads.
- Log failures + skipped files.
- Pipeline should recover and continue from the last point without starting over.