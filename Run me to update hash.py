#!/usr/bin/env python3
"""
update_hash.py -- Refresh the Content-Security-Policy script hash in
bible_converter.html after you edit its <script> block.
 
Usage:
    python3 update_hash.py                     # uses bible_converter.html in this folder
    python3 update_hash.py path/to/page.html   # or give a path (or drag the file onto this script)
 
The browser only runs an inline script if its SHA-256 hash is listed in the
page's Content-Security-Policy <meta> tag. Any change to the script text --
even a comment -- changes the hash, so run this after every edit.
"""
import base64
import hashlib
import re
import sys
 
path = sys.argv[1] if len(sys.argv) > 1 else "bible_converter.html"
 
with open(path, encoding="utf-8", newline="") as f:
    html = f.read()
 
m = re.search(r"<script>(.*?)</script>", html, re.S)
if not m:
    sys.exit("No inline <script>...</script> block found in " + path)
 
new_hash = base64.b64encode(hashlib.sha256(m.group(1).encode("utf-8")).digest()).decode()
 
csp = re.search(r"(script-src\s+'sha256-)([A-Za-z0-9+/=]+)(')", html)
if not csp:
    sys.exit(
        "No script-src 'sha256-...' found in the Content-Security-Policy tag.\n"
        "(If you deleted that tag, you don't need this script.)"
    )
 
if csp.group(2) == new_hash:
    print("Hash is already correct:", new_hash)
    sys.exit(0)
 
html = html[: csp.start(2)] + new_hash + html[csp.end(2):]
with open(path, "w", encoding="utf-8", newline="") as f:
    f.write(html)
 
print("Updated hash:")
print("  old:", csp.group(2))
print("  new:", new_hash)
 