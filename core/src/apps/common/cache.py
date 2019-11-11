from trezor.crypto import random

if False:
    from typing import Optional

_cached_seed = None  # type: Optional[bytes]
_cached_seed_without_passphrase = None  # type: Optional[bytes]
_cached_passphrase = None  # type: Optional[str]
_cached_state = None  # type: Optional[str]
_cached_passphrase_fprint = b"\x00\x00\x00\x00"  # type: bytes


def get_state() -> Optional[bytes]:
    global _cached_state
    if not _cached_state:
        _cached_state = random.bytes(32)
        print("setting state to: ", _cached_state)
    else:
        print("retrieving state: ", _cached_state)
    return _cached_state
    #
    # if passphrase is None:
    #     if _cached_passphrase is None:
    #         return None  # we don't have any passphrase to compute the state
    #     else:
    #         passphrase = _cached_passphrase  # use cached passphrase
    # return _compute_state(salt, passphrase)


def get_seed() -> Optional[bytes]:
    return _cached_seed


def get_seed_without_passphrase() -> Optional[bytes]:
    return _cached_seed_without_passphrase


def get_passphrase() -> Optional[str]:
    return _cached_passphrase


def get_passphrase_fprint() -> bytes:
    return _cached_passphrase_fprint


def has_passphrase() -> bool:
    return _cached_passphrase is not None


def set_seed(seed: Optional[bytes]) -> None:
    global _cached_seed
    _cached_seed = seed


def set_seed_without_passphrase(seed: Optional[bytes]) -> None:
    global _cached_seed_without_passphrase
    _cached_seed_without_passphrase = seed


def set_passphrase(passphrase: Optional[str]) -> None:
    global _cached_passphrase, _cached_passphrase_fprint
    _cached_passphrase = passphrase
    print("setting passphrase in cache: ", passphrase)
    # _cached_passphrase_fprint = _compute_state(b"FPRINT", passphrase or "")[:4]  # TODO!


def clear() -> None:
    print("clearing state")
    global _cached_state
    _cached_state = None

    set_seed(None)
    set_seed_without_passphrase(None)
    set_passphrase(None)
