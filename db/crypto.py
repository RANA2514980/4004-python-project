import base64
import hashlib
import secrets
from pathlib import Path


class SimpleCrypto:
    def __init__(self, key_path="db/secret.key"):
        self.key_path = Path(key_path)
        self.key = self._load_or_create_key()

    def _load_or_create_key(self):
        if self.key_path.exists():
            return self.key_path.read_bytes()

        self.key_path.parent.mkdir(parents=True, exist_ok=True)
        key = secrets.token_bytes(32)
        self.key_path.write_bytes(key)
        return key

    def _keystream(self, nonce, length):
        blocks = []
        counter = 0

        while len(b"".join(blocks)) < length:
            counter_bytes = counter.to_bytes(4, "big")
            digest = hashlib.sha256(self.key + nonce + counter_bytes).digest()
            blocks.append(digest)
            counter += 1

        return b"".join(blocks)[:length]

    def encrypt(self, plaintext):
        if plaintext is None:
            return None

        data = plaintext.encode("utf-8")
        nonce = secrets.token_bytes(16)
        stream = self._keystream(nonce, len(data))
        cipher = bytes(a ^ b for a, b in zip(data, stream))
        blob = b"v1" + nonce + cipher
        return "enc:" + base64.b64encode(blob).decode("ascii")

    def decrypt(self, token):
        if token is None:
            return None

        if not isinstance(token, str) or not token.startswith("enc:"):
            return token

        try:
            blob = base64.b64decode(token[4:])
            if blob[:2] != b"v1":
                return token

            nonce = blob[2:18]
            cipher = blob[18:]
            stream = self._keystream(nonce, len(cipher))
            data = bytes(a ^ b for a, b in zip(cipher, stream))
            return data.decode("utf-8", errors="replace")
        except Exception:
            return token
