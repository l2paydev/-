import os
from l2pay.settings import PRIVATE_KEY
from starknet_py.hash.utils import (
    private_to_stark_key,
)

from starknet_py.net.models.address import parse_address

ARGENTX_CLASS_HASH = (
    "0x029927C8AF6BCCF3F6FDA035981E765A7BDBF18A2DC0D630494F8758AA908E2B"
)
STARKNET_MODULUS = 2**251 + 17 * 2**192 + 1


def gen_account_address():
    from starknet_py.hash.address import compute_address
    from starknet_py.net.signer.stark_curve_signer import KeyPair

    key_pair = KeyPair.from_private_key(PRIVATE_KEY)
    starknet_publickey = private_to_stark_key(key_pair.private_key)

    # Generate a random salt
    salt = int.from_bytes(os.urandom(32), byteorder="big") % STARKNET_MODULUS

    # Compute an address
    address = compute_address(
        salt=salt,
        class_hash=parse_address(ARGENTX_CLASS_HASH),
        constructor_calldata=[starknet_publickey],
        deployer_address=0,
    )
    formatted_account_address = f"0x{address:064x}"
    print(f"Computed formatted_account_address: {formatted_account_address}")
    return formatted_account_address
