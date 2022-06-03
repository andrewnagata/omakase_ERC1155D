from brownie import accounts, config, network, Omakase
from brownie.network import web3
from scripts.helpers import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def deploy_omakase():

    _box_account = get_account(index=0)
    print(f"{bcolors.OKGREEN}Using account: {bcolors.BOLD}{_box_account}{bcolors.ENDC}")

    _baseURI = 'ipfs://QmbNRforX8dxj4ppYiDwhtGwW8sQ7aYMDXcFxQhfx1ny11'
    _contractURI = 'ipfs://QmbNRforX8dxj4ppYiDwhtGwW8sQ7aYMDXcFxQhfx1ny11'
    _box_contract = _box_account
    mock_nft = Omakase.deploy(
        _baseURI,
        _contractURI,
        _box_contract,
        {"from":_box_account}, publish_source=config["networks"][network.show_active()].get("verify"))

    print(f"{bcolors.OKGREEN}Mock NFT contract is deployed...{bcolors.ENDC}")
    start_tx = mock_nft.togglePublicSale({"from":_box_account})
    start_tx.wait(1)
    print(f"{bcolors.OKGREEN}Start the public sale for testing{bcolors.ENDC}")

    box_tx = mock_nft.mint(_box_account, {"from":_box_account, "value":web3.toWei(0.01, "ether")})
    box_tx.wait(1)
    print("Minted a mock nft")

    _account = get_account(index=1)
    print(f"{bcolors.OKGREEN}Using account: {bcolors.BOLD}{_account}{bcolors.ENDC}")
    box_tx = mock_nft.mint(_account, {"from":_account, "value":web3.toWei(0.01, "ether")})
    box_tx.wait(1)
    print("Minted a mock nft")

    _baseURI = 'ipfs://QmbNRforX8dxj4ppYiDwhtGwW8sQ7aYMDXcFxQhfx1ny11'
    _contractURI = 'ipfs://QmbNRforX8dxj4ppYiDwhtGwW8sQ7aYMDXcFxQhfx1ny11'
    _box_contract = mock_nft
    omakase = Omakase.deploy(
        _baseURI,
        _contractURI,
        _box_contract,
        {"from":_account}, publish_source=config["networks"][network.show_active()].get("verify"))

    print(f"{bcolors.OKGREEN}Omakase is deployed...{bcolors.ENDC}")

    pre_tx = omakase.togglePresale({"from": _account})
    pre_tx.wait(1)
    print(f"{bcolors.OKGREEN}Presale STARTED!{bcolors.ENDC}")

    eth = web3.toWei(0.01, "ether")
    mint_tx = omakase.presaleFreeMint(_account, {"from": _account, "value":eth})
    mint_tx.wait(1)
    print(f"{bcolors.OKGREEN}Token Minted for FREE at Presale{bcolors.ENDC}")

    eth = web3.toWei(0.01, "ether")
    mint_tx = omakase.presaleFreeMint(_box_account, {"from": _box_account, "value":eth})
    mint_tx.wait(1)
    print(f"{bcolors.OKGREEN}Token Minted for FREE at Presale{bcolors.ENDC}")

    try:
        mint_tx = omakase.presaleFreeMint(_box_account, {"from": _box_account, "value":eth})
        mint_tx.wait(1)
        print(f"{bcolors.FAIL}Second premint!! fail...{bcolors.ENDC}")
        exit(1)
    except:
        print(f"{bcolors.OKGREEN}Second Premint failed!! as expected, moving on...{bcolors.ENDC}")
        

    public_tx = omakase.togglePublicSale({"from": _account})
    public_tx.wait(1)
    print(f"{bcolors.OKGREEN}Public Sale STARTED!{bcolors.ENDC}")

    mint_tx = omakase.mint(_box_account, {"from": _box_account, "value":eth})
    mint_tx.wait(1)
    print(f"{bcolors.OKGREEN}second token minted{bcolors.ENDC}")

    mint_tx = omakase.mint(_account, {"from": _account, "value":eth})
    mint_tx.wait(1)
    print(f"{bcolors.OKGREEN}Minted token for _account{bcolors.ENDC}")

    _receiver = get_account(index=2)
    account_tokens = omakase.getWalletOfOwner(_account)
    print(f"{bcolors.OKGREEN}_account wallet: {bcolors.OKCYAN}{account_tokens}{bcolors.ENDC}")
    rec_tokens = omakase.getWalletOfOwner(_receiver)
    print(f"{bcolors.OKGREEN}receiver wallet: {bcolors.OKCYAN}{rec_tokens}{bcolors.ENDC}")

    transfer_token = omakase.getWalletOfOwner(_account)[0]
    trans_tx = omakase.safeTransferFrom(_account, _receiver, transfer_token, 1, "", {"from":_account})
    trans_tx.wait(1)
    print(f"{bcolors.OKGREEN}transfer of tokenID: {transfer_token} complete!{bcolors.ENDC}")

    person = get_account(index=3)
    batch = 10
    eth = web3.toWei(0.01, "ether") * batch
    mint_tx = omakase.mintBatch(person, batch, {"from": person, "value":eth})
    mint_tx.wait(1)

    acc_tokens = omakase.getWalletOfOwner(_account)
    rec_tokens = omakase.getWalletOfOwner(_receiver)
    p_wallet = omakase.getWalletOfOwner(person)
    box_tokens = omakase.getWalletOfOwner(_box_account)
    print(f"{bcolors.OKGREEN}Box owner wallet: {bcolors.OKCYAN}{box_tokens}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Account wallet: {bcolors.OKCYAN}{acc_tokens}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}receiver wallet: {bcolors.OKCYAN}{rec_tokens}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Person Wallet: {bcolors.OKCYAN}{p_wallet}{bcolors.ENDC}")

def main():
    deploy_omakase()
