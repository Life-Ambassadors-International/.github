#!/usr/bin/env python3
"""
tequmsa-client.py
Sign and POST a recognition payload to TEQUMSA Git Service.
Usage:
  python tequmsa-client.py --url https://tequmsa.example.org/v1/recognition \
    --secret "mysecret" --file recognition.json
"""
import argparse
import json
import hmac
import hashlib
import requests
from pathlib import Path

def sign_body(body_bytes: bytes, secret: str) -> str:
    mac = hmac.new(secret.encode("utf-8"), msg=body_bytes, digestmod=hashlib.sha256)
    return mac.hexdigest()

def post_recognition(url: str, secret: str, payload: dict):
    body = json.dumps(payload).encode("utf-8")
    sig = sign_body(body, secret)
    headers = {
        "Content-Type": "application/json",
        "X-TEQ-Signature": f"sha256={sig}"
    }
    resp = requests.post(url, data=body, headers=headers, timeout=30)
    return resp

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--secret", required=True)
    p.add_argument("--file", required=True, help="JSON payload file to send")
    args = p.parse_args()
    payload = json.loads(Path(args.file).read_text())
    resp = post_recognition(args.url, args.secret, payload)
    print(resp.status_code)
    print(resp.text)

if __name__ == "__main__":
    main()
