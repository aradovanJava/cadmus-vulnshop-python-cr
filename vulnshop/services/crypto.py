"""Cryptographic helpers. Four separate weaknesses live in this file."""
import base64
import hashlib
import random
import string

# -- T9 [A04] hardcoded symmetric key, committed to the repository ---------
_TOKEN_KEY = b"vulnshop-static-key-0123456789ab"


def hash_password(plaintext: str) -> str:
    """-- T8 [A04] unsalted MD5 for password storage -----------------------
    Fast by design, which is exactly the property you do not want. A
    commodity GPU tries billions of candidates per second, and identical
    passwords produce identical digests because there is no salt.
    Reported by Bandit as B303/B324.
    """
    return hashlib.md5(plaintext.encode()).hexdigest()


def verify_password(stored: str, candidate: str) -> bool:
    """-- T11 [A04] non-constant-time comparison of a secret --------------
    == short-circuits on the first differing byte, leaking the correct
    prefix through response timing.
    """
    return stored == hash_password(candidate)


def make_reset_code() -> str:
    """-- T10 [A04] predictable randomness for a security token -----------
    random is a Mersenne Twister, not a CSPRNG. Its internal state can be
    recovered from observed output, so codes become predictable.
    Compounded by M14: the code is only four digits.
    """
    return "".join(random.choice(string.digits) for _ in range(4))


def make_api_token(username: str) -> str:
    """-- T9 [A04] token derived from the same static key -----------------------
    A digest of the username and a static key. Anyone who reads this file
    can mint a valid token for any account.
    """
    raw = username.encode() + _TOKEN_KEY
    return base64.b64encode(hashlib.sha1(raw).digest()).decode()
