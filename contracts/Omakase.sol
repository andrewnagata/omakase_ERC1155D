// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ERC1155D.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

contract Omakase is ERC1155, Ownable {
    using Strings for uint256;

    uint256 public    totalSupply; // tokenID's
    uint256 public    mint_price = .01 ether;
    uint256 public    mint_max = 10;
    string  public    contract_uri;
    bool    public    presale_state = false;
    bool    public    publicsale_state = false;
    address private   box_contract;

    constructor(string memory _uri,
                string memory _contract_uri,
                address       _box_contract)
        ERC1155(_uri) {
            contract_uri = _contract_uri;
            box_contract = _box_contract;
        }

    function togglePresale() public onlyOwner {
        presale_state = !presale_state;
    }

    function togglePublicSale() public onlyOwner {
        publicsale_state = !publicsale_state;
    }

    function setMintPrice(uint256 price) public onlyOwner {
        mint_price = price;
    }

    function setContractUri(string memory _contract_uri) public onlyOwner {
        contract_uri = _contract_uri;
    }

    function setURI(string memory newuri) public {
        _setURI(newuri);
    }

    function presaleFreeMint(address to) public payable {
        require(presale_state == true, "Presale not active");
        require(Omakase(box_contract).getWalletOfOwner(to).length > 0, "Need to be an owner to qualify");
        require(_balances[to] < 1, "Already minted presale, Joe");

        _mint(to, totalSupply, 1, '');
        totalSupply++;
    }

    function mint(address to) public payable {
        require(publicsale_state == true, "Public sale not active");
        require(msg.value >= mint_price, "Not enough Ether, Joe");

        _mint(to, totalSupply, 1, '');
        totalSupply++;
    }

    function mintBatch(address to, uint256 amount) public payable {
        require(msg.value >= mint_price * amount, "Not enough Ether, Joe");
        require(amount <= mint_max, "Can't mint that many at once");

        uint256[] memory ids = new uint256[](amount);
        uint256[] memory amounts = new uint256[](amount);
        for (uint256 i = 0; i < amount; ++i) {
            ids[i] = totalSupply++;
            amounts[i] = 1;
        }
        _mintBatch(to, ids, amounts, '');
    }

    function getWalletOfOwner(address _address) public view returns(uint256[] memory) {
        uint256 tokenCount = _balances[_address];
        if (tokenCount == 0) return new uint256[](0);

        uint256[] memory owner_tokens = new uint256[](tokenCount);
        for (uint256 i; i < tokenCount; i++) {
            owner_tokens[i] = tokenOfOwnerByIndex(_address, i);
        }
        return owner_tokens;
    }

    function tokenOfOwnerByIndex(address owner, uint256 index) public view returns (uint256 tokenId) {
        require(index < _balances[owner], "Owner index out of bounds");

        uint count;
        for(uint i; i < _owners.length; i++){
            if(owner == _owners[i]){
                if(count == index) return i;
                else count++;
            }
        }

        revert("Owner index out of bounds");
    }

    function withdraw() external onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }
}