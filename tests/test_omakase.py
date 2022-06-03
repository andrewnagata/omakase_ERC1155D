from brownie import accounts, config, network, Omakase
from brownie.network import web3
from scripts.helpers import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from typing import Tuple
import pytest

pytest.omakase_contract = None
pytest.box_contract = None

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

@pytest.fixture
def _accounts():
    accounts = {
        "box_account": get_account(index=0),
        "omakase_account": get_account(index=1)
    }

    return accounts

def test_setup_contracts(_accounts):
    
    _baseURI = 'ipfs://QmbNRforX8dxj4ppYiDwhtGwW8sQ7aYMDXcFxQhfx1ny11'
    _contractURI = 'ipfs://QmbNRforX8dxj4ppYiDwhtGwW8sQ7aYMDXcFxQhfx1ny11'
    
    box_deployed = Omakase.deploy(
        _baseURI,
        _contractURI,
        _accounts["box_account"],
        {"from":_accounts["box_account"]}, publish_source=config["networks"][network.show_active()].get("verify"))

    omakase_deployed = Omakase.deploy(
        _baseURI,
        _contractURI,
        box_deployed,
        {"from":_accounts["omakase_account"]}, publish_source=config["networks"][network.show_active()].get("verify"))

    pytest.box_contract = box_deployed
    pytest.omakase_contract = omakase_deployed

def test_intial_states(_accounts):

    box_contract = pytest.box_contract
    box_owner = _accounts["box_account"]

    start_tx = box_contract.togglePublicSale({"from":box_owner})
    start_tx.wait(1)
    print(f"{bcolors.OKGREEN}Start the public sale for testing{bcolors.ENDC}")
    box_tx = box_contract.mint(box_owner, {"from":box_owner, "value":web3.toWei(0.01, "ether")})
    box_tx.wait(1)

    expected_boxes = 1
    minted_boxes = box_contract.totalSupply()

    assert minted_boxes == expected_boxes

def test_presale(_accounts):

    box_owner = _accounts["box_account"]
    omakase_owner = _accounts["omakase_account"]
    omakase_contract = pytest.omakase_contract

    """check presale toggle"""
    presale_active = omakase_contract.presale_state()

    expected = False
    assert presale_active == expected

    """Try to mint before presale begins - should fail"""
    eth = web3.toWei(0.01, "ether")
    can_mint_presale = True
    try:
        mint_tx = omakase_contract.presaleFreeMint(box_owner, {"from":box_owner, "value":eth})
        mint_tx.wait(1)
    except:
        can_mint_presale = False

    expected = False
    assert can_mint_presale == expected

    """Turn on presale"""
    pre_tx = omakase_contract.togglePresale({"from":omakase_owner})
    pre_tx.wait(1)

    """Mint one in presale to box holder"""
    eth = web3.toWei(0.01, "ether")
    mint_tx = omakase_contract.presaleFreeMint(box_owner, {"from":box_owner, "value":eth})
    mint_tx.wait(1)

    total_omakase = omakase_contract.totalSupply()

    expected = 1
    assert total_omakase == expected

    """Try to mint a second one from same holder - should fail"""
    can_mint_two = True
    try:
        mint_tx = omakase_contract.presaleFreeMint(box_owner, {"from":box_owner, "value":eth})
        mint_tx.wait(1)
    except:
        can_mint_two = False

    expected = False
    assert can_mint_two == expected

def test_mint_many(_accounts):

    omakase_owner = _accounts["omakase_account"]

    start_count = len(pytest.omakase_contract.getWalletOfOwner(omakase_owner))

    eth = web3.toWei(0.01, "ether")
    count = 10
    value = eth * count

    mint_tx = pytest.omakase_contract.mintBatch(omakase_owner, count, {"from":omakase_owner, "value":value})
    mint_tx.wait(1)

    current_count = len(pytest.omakase_contract.getWalletOfOwner(omakase_owner))

    expected = start_count + count
    assert current_count == expected

    
