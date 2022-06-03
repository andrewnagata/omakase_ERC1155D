# Order of Omakase
## NFT smart contracts

Using ERC1155D as a base for efficient gas savings. Minting costs are reduced, as well as transfer costs. However, the ability to pull an owners tokenIDs from the contract is an important component for future UX. So, the ability to track tokenIDs has been added back. Yes, this results in a considerable bump in gas costs at mint. The balance between gas efficiency and user experience is at play here. The idea that a frontend client would pull all 10k owners to parse tokeIDs for a given wallet is too extreme. Also, future composibility with other contracts that might use this feature is planned.

## Tech

- [Brownie] - Testing and deployment using python, cuz why not. More info on [Brownie](https://eth-brownie.readthedocs.io/en/stable/)

## ERC1155D
Info on ERC1155D is [here](https://medium.com/donkeverse/introducing-erc1155d-the-most-efficient-non-fungible-token-contract-in-existence-c1d0a62e30f1)