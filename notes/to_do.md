# to-do

1) Recursive Drive indexing
- Update `build_index.py` so it crawls the whole Drive folder (including all subfolders), not just recent files/uploads

2) Remove download cap and add resume
- Remove/increase `MAX_DOWNLOADS`
- Add a resume mechanism so rerunning the script continues downloading where it left off

3) Retry + failure logging
- Add retries for failed downloads.
- Log failures + skipped files.
- Pipeline should pick up where it stopped without restarting from the beginning