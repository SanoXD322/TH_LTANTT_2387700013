import pytest
from securecrypto import hash_utils
from argon2.exceptions import VerifyMismatchError

def test_hash_password_and_verify():
    candidate = "" 
    hashed = hash_utils.hash_password_secure(candidate)
    assert hashed is not None

    from argon2 import PasswordHasher
    ph = PasswordHasher()
    try:
        ph.verify(hashed, candidate)
        verified = True
    except VerifyMismatchError:
        verified = False
    assert verified == True

def test_wrong_password_verification():
    candidate = "CorrectPass"
    other_candidate = "WrongPass"
    hashed = hash_utils.hash_password_secure(candidate)

    from argon2 import PasswordHasher
    ph = PasswordHasher()
    try:
        ph.verify(hashed, other_candidate)
        verified = True
    except VerifyMismatchError:
        verified = False
    assert verified == False
