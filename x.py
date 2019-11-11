from trezorlib.client import get_default_client
from trezorlib.tools import parse_path
from trezorlib import btc


def get_address(client):
    # Get the first address of first BIP44 account
    # (should be the same address as shown in wallet.trezor.io)
    bip32_path = parse_path("44'/0'/0'/0/0")
    address = btc.get_address(client, "Bitcoin", bip32_path)
    assert address == "1FH6ehAd5ZFXCM1cLGzHxK1s4dGdq1JusM"


def main():
    client = get_default_client()

    state = client.features.state
    print("state: ", state[:5])
    get_address(client)

    client.init_device()
    get_address(client)




if __name__ == "__main__":
    main()
