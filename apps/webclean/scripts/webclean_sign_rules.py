#!/usr/bin/env python3
"""Sign the first-party WebClean rule payload for static GitHub Pages hosting.

The private key is supplied by CI only. This script never downloads or embeds third-party
filter lists and writes only the signed envelope requested by the workflow.
"""
import argparse
import base64
import datetime as dt
import json
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--key", required=True, help="base64 raw Ed25519 private key from CI secret")
    parser.add_argument("--key-id", required=True)
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    payload["createdAt"] = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    private = Ed25519PrivateKey.from_private_bytes(base64.b64decode(args.key))
    envelope = {
        "alg": "ed25519",
        "keyId": args.key_id,
        "payload": payload,
        "signature": base64.b64encode(private.sign(canonical(payload))).decode("ascii"),
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_bytes(canonical(envelope))


if __name__ == "__main__":
    main()
