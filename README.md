# Read Me

### Description

Our Project is based on helping the users convert their artwork which is in the form of image or video into NFTs and minting it onto the blockchain according to their preference. The user interaction takes with the help of a discord bot that identifies any image or video file being sent in the chat and then asks from the user whether they want to proceed further for minting. If several images are being sent in one go then the bot even asks for one preference of the user among the sent files. If the bot gets confirmation from the user to proceed further then it redirects them to their DMs further for security reasons and from there continues further. It asks for a name and description of the file and the crypto-wallet address of the user (but not their private key) and then asks for their preference in a particular blockchain. After receiving proper information, it mints the NFT.

### Features of the Projects

1. File detection in discord chat
2. NFT minting from the detected files with help of REST API
3. Choice of blockchain between Ethereum testnet Goerli and Polygon mainnet for minting
4. ability to show all NFTs linked to a wallet with an interactive menu to navigate through the list.
5. Counter which counts how many NFTs the bot has minted so far. Visible in bot’s profile on discord

### Technologies Stack

1. Python 3 - programming language for the project
2. [discord.py](http://discord.py) library - API wrapper for interacting with discord through python
3. NFTport REST API - used for easy minting of the files onto blockchain. Free tier used for testing
4. OpenSea - for verifying the NFTs on blockchain
5. Metamask - crypto wallet

### Future Updates

- In future we would like to add the option to mint audio only NFTs as well
- We would like to implement the usage of several images given by the user and convert it into a small video with a few options given to the user to enhance the video such as duration of each image and their desired audio.
- We would like to add patreon integration and provide server credits which can be used only by members with a certain role and each mint uses up some of the credits. This is because the paid version of NFTport API costs money because minting NFTs costs gas fees. Free trial includes only 100 mints per blockchain per API key which we used for testing. This is the only way to make it a sustainable bot on a big scale.

### How to launch your own instance of this bot?

To set up your own instance of this bot:

1. Clone this repository
2. create a discord application from developer portal and create a bot
3. add the bot to a server
4. add a .env file and store your NFTport API key with name “minter_key” and discord bot token with name “token”
5. pip install discord.py
6. run the [main.py](http://main.py) file

### Bot commands and events:

1. The first one is the message listener which detects the image and video files and starts the minting process. It is the main attraction of our project.
2. a slash command called “/list” to list all NFTs linked to a crypto wallet which the bot gets from the wallet address provided by the user in input
3. a help command which can be access through a slash command called “/help” which acts as a guide to the bot
