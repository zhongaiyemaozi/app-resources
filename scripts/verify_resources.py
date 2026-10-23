"""Verify public resources before publishing; no private key needed."""
import base64
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

ROOT = Path(__file__).resolve().parent.parent

def check_file(path, digest, size=None):
    assert path.is_relative_to(ROOT) and path.is_file(), path
    data = path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == digest, path
    if size is not None:
        assert len(data) == size, path

kids = ROOT / "apps/kids-learning-park"
manifest = json.loads((kids / "manifest.json").read_text())
for pack in manifest["packs"]:
    check_file(kids / "packs" / (pack["id"] + ".json"), pack["sha256"], pack["sizeBytes"])
    assert pack["urls"] and all("/zhongaiyemaozi/app-resources" in url for url in pack["urls"].values())
leaf = ROOT / "apps/leafread"
voices = json.loads((leaf / "voices.json").read_text())["voices"]
for voice in voices:
    for file in voice["files"]:
        if "remoteURL" in file:
            assert file["remoteURL"] == "https://github.com/zhongaiyemaozi/app-resources/releases/download/resources-v1/" + file["name"]
        else:
            check_file(leaf / file["name"], file["sha256"], file["bytes"])
sparks = ROOT / "apps/sparks"
transport_hashes = json.loads((sparks / "transport-sha256.json").read_text())
for pack in json.loads((sparks / "manifest.json").read_text())["packs"]:
    for locale, name in pack["files"].items():
        check_file(sparks / name, transport_hashes[name])
envelope = json.loads((ROOT / "apps/webclean/webclean-rules.json").read_text())
assert envelope["alg"] == "ed25519" and envelope["keyId"] == "webclean-2026-09"
canonical = json.dumps(envelope["payload"], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
Ed25519PublicKey.from_public_bytes(base64.b64decode("v1d2C1VW/f5T+8Ds7gUb07zkQ9Np+xpxOH95oy7t8GA=")).verify(base64.b64decode(envelope["signature"]), canonical)
print(f"Verified {len(manifest['packs'])} kids packs, {len(voices)} voices, Sparks packs and WebClean signature")
