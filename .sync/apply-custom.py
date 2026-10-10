#!/usr/bin/env python3
"""Re-apply local customizations onto the upstream ruleset_geodata run.yml.

Used by .github/workflows/sync.yml after a hard reset to upstream.
Idempotent.  Exits non-zero (loud failure) if an expected anchor is gone.
"""
import sys
import pathlib

path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".github/workflows/run.yml")
text = path.read_text(encoding="utf-8")

if "github.com/Yofk/domain-list-custom/releases/download/domains" in text:
    print("custom sources already present; nothing to do")
    sys.exit(0)

# 1. point the domain-list-custom release download at our fork
old_url = "domains_download_url=https://github.com/DustinWin/domain-list-custom/releases/download/domains"
new_url = "domains_download_url=https://github.com/Yofk/domain-list-custom/releases/download/domains"
if text.count(old_url) != 1:
    sys.stderr.write("ERROR: anchor not found exactly once: %s\n" % old_url)
    sys.exit(1)

# 2. checkout our fork as the `custom` source
old_repo = "repository: DustinWin/domain-list-custom\n"
new_repo = "repository: Yofk/domain-list-custom\n"
if text.count(old_repo) != 1:
    sys.stderr.write("ERROR: anchor not found exactly once: %r\n" % old_repo)
    sys.exit(1)

text = text.replace(old_url, new_url).replace(old_repo, new_repo)
path.write_text(text, encoding="utf-8")
print("custom sources re-applied to %s" % path)
