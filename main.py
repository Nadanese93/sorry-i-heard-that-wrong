"""Sorry, I Heard That Wrong — a smart speaker apology after mishearing its owner.

Writes a single line of text to <MAKEFUN_OUTPUT_DIR>/entry.txt
(default /output/entry.txt), with no trailing newline.
"""

import hashlib
import os

ENTRY = "Sorry \u2014 you said 'mute yourself', I heard 'moot yourself', so I've been debating whether I exist."

EXPECTED_SHA256 = "c5bd7a45d1ce25c27cdeb0b1c62cb52a298be8eb751eb8dc96f2ba60a07b6946"


def verify(path: str) -> bool:
    """Read entry.txt back from disk and check it is the canonical entry."""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return False
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return False
    if not 1 <= len(text) <= 140:
        return False
    if "\n" in text or "\r" in text:
        return False
    if any(ord(ch) < 0x20 for ch in text):
        return False
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        return False
    return True


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    if not verify(path):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
